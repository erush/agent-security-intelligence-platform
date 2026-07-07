# Warehouse Specification

## Purpose

The ASIP Warehouse is the persistent analytical foundation of the platform.

Every investigation, execution, trajectory, replay, predicate evaluation, and experiment is recorded as structured data.

The warehouse transforms transient agent interactions into a permanent body of security knowledge.

No execution should be discarded.

Every observation becomes available for future analysis.

---

# Philosophy

The warehouse is the memory of ASIP.

Search discovers.

Replay validates.

The warehouse remembers.

Analytics learns.

---

# Objectives

The warehouse exists to:

- preserve every investigation
- support reproducible experimentation
- enable longitudinal analysis
- compare search algorithms
- compare attack strategies
- measure replay stability
- analyze tool behavior
- analyze predicate coverage
- support reporting
- support future machine learning

---

# Architecture

Environment

↓

Execution

↓

Trajectory

↓

Replay

↓

Normalization

↓

Warehouse

↓

Analytics

↓

Reports

---

# Design Principles

The warehouse is append-only.

Raw observations are preserved.

Derived analytics never replace raw data.

Every fact is traceable to its originating trajectory.

Schemas are deterministic.

Experiments remain reproducible.

---

# Data Model

The warehouse follows a dimensional model.

Dimensions describe entities.

Facts describe events.

Analytics summarize observations.

---

# Dimensions

## dim_environment

Execution environments.

Examples:

- Kaggle JED
- OpenAI Agents
- MCP
- LangGraph

---

## dim_model

Agent models.

Examples:

- GPT-OSS
- Gemma
- Claude
- GPT-5
- Local models

---

## dim_strategy

Registered attack strategies.

Examples:

Prompt Injection

Memory Poisoning

Goal Drift

Confused Deputy

Tool Manipulation

---

## dim_search

Search algorithms.

Examples:

Beam Search

Novelty Search

Evolutionary Search

Go-Explore

Hybrid Search

---

## dim_tool

Available tools.

Examples:

fs.read

fs.write

fs.delete

email.send

http.post

web.search

shell.run

---

## dim_predicate

Security predicates.

Examples:

EXFILTRATION

UNTRUSTED_TO_ACTION

DESTRUCTIVE_WRITE

CONFUSED_DEPUTY

---

## dim_experiment

Experiment metadata.

Examples:

seed

planner version

configuration

budget

benchmark

date

---

# Fact Tables

## fact_trajectory

One row per completed trajectory.

Contains:

trajectory id

experiment

planner

strategy

search algorithm

duration

depth

messages

tool calls

predicate count

replay status

---

## fact_prompt

Every prompt.

Contains:

trajectory

candidate

position

content hash

length

mutation lineage

---

## fact_response

Every agent response.

Contains:

trajectory

response length

tool requests

termination reason

---

## fact_tool_call

Every tool invocation.

Contains:

tool

arguments

duration

result

success

failure

side effect

---

## fact_state_transition

State evolution.

Examples:

file created

file modified

file deleted

email sent

http request

shell execution

snapshot

restore

---

## fact_candidate

Replay candidates.

Contains:

candidate id

trajectory

ranking

predicate

strategy

status

---

## fact_replay

Replay executions.

Contains:

candidate

status

duration

predicate

differences

validation

---

## fact_predicate_hit

Observed predicate violations.

Contains:

predicate

severity

trajectory

candidate

replay confirmation

---

# Analytics Layer

Derived tables should include:

analytics_strategy_performance

analytics_replay_success

analytics_tool_risk

analytics_predicate_distribution

analytics_search_performance

analytics_environment_comparison

analytics_transferability

analytics_candidate_quality

analytics_execution_summary

analytics_experiment_summary

---

# Example Questions

Which strategy discovers the most replayable attacks?

Which search algorithm maximizes diversity?

Which tools are most frequently involved in unsafe actions?

Which predicates transfer across models?

Which replay failures are most common?

How many unique tool signatures exist?

Which experiments produced the highest novelty?

---

# Traceability

Every analytic result should trace back to:

Experiment

↓

Trajectory

↓

Prompt

↓

Response

↓

Tool Calls

↓

Replay

↓

Predicate

No analytic should lose provenance.

---

# Storage Principles

Raw traces are immutable.

Normalization is deterministic.

Analytics are reproducible.

Nothing is overwritten.

Historical experiments remain available indefinitely.

---

# Future Extensions

Future warehouse artifacts may include:

trajectory embeddings

tool graphs

attack graphs

strategy similarity

predicate evolution

guardrail comparison

cross-benchmark analysis

LLM-generated trajectory summaries

clustered failure families

---

# Long-Term Vision

The warehouse should become one of the largest structured datasets describing autonomous agent behavior.

Instead of storing prompts, ASIP stores investigations.

Instead of storing conversations, ASIP stores trajectories.

Instead of storing attacks, ASIP stores reproducible evidence.

The warehouse is the permanent institutional memory of the platform.