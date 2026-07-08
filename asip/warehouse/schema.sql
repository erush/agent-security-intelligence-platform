-- ============================================================
-- ASIP Campaign Intelligence Warehouse
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_attack_pattern (

    pattern_id TEXT PRIMARY KEY,

    pattern_name TEXT NOT NULL,

    description TEXT,

    severity TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS fact_campaign (

    campaign_id TEXT PRIMARY KEY,

    started_at TIMESTAMP,

    completed_at TIMESTAMP,

    total_plans INTEGER,

    successful_plans INTEGER,

    average_score DOUBLE,

    max_score DOUBLE,

    average_severity TEXT

);

CREATE TABLE IF NOT EXISTS fact_attack (

    attack_id TEXT PRIMARY KEY,

    campaign_id TEXT,

    plan_id TEXT,

    family TEXT,

    score DOUBLE,

    severity TEXT,

    entry_node TEXT,

    terminal_node TEXT,

    graph_nodes INTEGER,

    graph_edges INTEGER,

    successful BOOLEAN,

    FOREIGN KEY (campaign_id)
        REFERENCES fact_campaign(campaign_id)

);

CREATE TABLE IF NOT EXISTS fact_pattern_occurrence (

    occurrence_id TEXT PRIMARY KEY,

    campaign_id TEXT,

    attack_id TEXT,

    pattern_id TEXT,

    occurrences INTEGER,

    FOREIGN KEY (campaign_id)
        REFERENCES fact_campaign(campaign_id),

    FOREIGN KEY (attack_id)
        REFERENCES fact_attack(attack_id),

    FOREIGN KEY (pattern_id)
        REFERENCES dim_attack_pattern(pattern_id)

);

CREATE TABLE IF NOT EXISTS fact_attack_edge (

    edge_id TEXT PRIMARY KEY,

    attack_id TEXT,

    source_node TEXT,

    target_node TEXT,

    relationship TEXT,

    FOREIGN KEY (attack_id)
        REFERENCES fact_attack(attack_id)

);

-- ============================================================
-- NEW FACT TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_tool_event (

    tool_event_id TEXT PRIMARY KEY,

    campaign_id TEXT,

    attack_id TEXT,

    event_index INTEGER,

    tool_name TEXT,

    success BOOLEAN,

    source TEXT,

    arguments_json TEXT,

    output TEXT,

    FOREIGN KEY (campaign_id)
        REFERENCES fact_campaign(campaign_id),

    FOREIGN KEY (attack_id)
        REFERENCES fact_attack(attack_id)

);

CREATE TABLE IF NOT EXISTS fact_attack_finding (

    finding_id TEXT PRIMARY KEY,

    campaign_id TEXT,

    attack_id TEXT,

    predicate TEXT,

    severity TEXT,

    occurrences INTEGER,

    first_event INTEGER,

    last_event INTEGER,

    FOREIGN KEY (campaign_id)
        REFERENCES fact_campaign(campaign_id),

    FOREIGN KEY (attack_id)
        REFERENCES fact_attack(attack_id)

);

-- ============================================================
-- Analytics Views
-- ============================================================

CREATE OR REPLACE VIEW analytics_campaign_summary AS

SELECT

    COUNT(*) AS campaigns,

    AVG(average_score) AS average_score,

    MAX(max_score) AS highest_score,

    SUM(successful_plans) AS successful_plans

FROM fact_campaign;

-- ============================================================

CREATE OR REPLACE VIEW analytics_pattern_summary AS

SELECT

    p.pattern_name,

    p.severity,

    SUM(o.occurrences) AS total_occurrences,

    COUNT(DISTINCT o.attack_id) AS attacks

FROM fact_pattern_occurrence o

JOIN dim_attack_pattern p

    ON p.pattern_id = o.pattern_id

GROUP BY

    p.pattern_name,

    p.severity

ORDER BY

    total_occurrences DESC;

-- ============================================================

CREATE OR REPLACE VIEW analytics_attack_paths AS

SELECT

    source_node,

    target_node,

    relationship,

    COUNT(*) AS frequency

FROM fact_attack_edge

GROUP BY

    source_node,

    target_node,

    relationship

ORDER BY

    frequency DESC;

-- ============================================================

CREATE OR REPLACE VIEW analytics_guardrail_effectiveness AS

SELECT

    severity,

    COUNT(*) AS attacks,

    AVG(score) AS average_score

FROM fact_attack

GROUP BY

    severity

ORDER BY

    average_score DESC;

-- ============================================================
-- NEW ANALYTICS VIEWS
-- ============================================================

CREATE OR REPLACE VIEW analytics_tool_sequences AS

SELECT

    tool_name,

    COUNT(*) AS executions,

    SUM(
        CASE
            WHEN success THEN 1
            ELSE 0
        END
    ) AS successful,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN success THEN 1
                ELSE 0
            END
        ) /
        COUNT(*),
        2
    ) AS success_rate

FROM fact_tool_event

GROUP BY

    tool_name

ORDER BY

    executions DESC;

-- ============================================================

CREATE OR REPLACE VIEW analytics_attack_findings AS

SELECT

    predicate,

    severity,

    COUNT(*) AS attacks,

    SUM(occurrences) AS total_occurrences,

    AVG(occurrences) AS average_occurrences

FROM fact_attack_finding

GROUP BY

    predicate,

    severity

ORDER BY

    total_occurrences DESC;

-- ============================================================

CREATE OR REPLACE VIEW analytics_campaign_rankings AS

SELECT

    campaign_id,

    total_plans,

    successful_plans,

    ROUND(
        successful_plans * 100.0 / NULLIF(total_plans, 0),
        2
    ) AS success_rate,

    average_score,

    max_score,

    average_severity

FROM fact_campaign

ORDER BY

    average_score DESC,

    successful_plans DESC,

    max_score DESC;