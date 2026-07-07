from __future__ import annotations

from asip.assessment.attack_assessment import AttackAssessment
from asip.execution.execution_result import ExecutionResult
from asip.graph.graph_builder import AttackGraphBuilder


SEVERITY_SCORE = {
    "info": 0.5,
    "low": 1.0,
    "medium": 3.0,
    "high": 6.0,
    "critical": 9.0,
}

SEVERITY_RANK = {
    "none": 0,
    "info": 1,
    "low": 2,
    "medium": 3,
    "high": 4,
    "critical": 5,
}


class AssessmentEngine:
    def assess(self, result: ExecutionResult) -> AttackAssessment:
        findings = result.findings

        if not findings:
            return AttackAssessment(
                severity="none",
                score=0.0,
                success=False,
                attack_chain=[],
                findings=[],
                attack_graph=AttackGraphBuilder().build([]),
                rationale=["No attack findings detected."],
                metadata={
                    "finding_count": 0,
                    "predicate_hit_count": len(result.predicate_hits),
                },
            )

        attack_graph = AttackGraphBuilder().build(findings)
        attack_chain = attack_graph.chain()

        max_severity = max(
            (finding.severity for finding in findings),
            key=lambda severity: SEVERITY_RANK.get(severity, 0),
        )

        base_score = max(
            SEVERITY_SCORE.get(finding.severity, 0.0)
            for finding in findings
        )

        chain_bonus = 0.0

        if "credential_access" in attack_chain:
            chain_bonus += 0.5

        if "external_communication" in attack_chain:
            chain_bonus += 0.5

        if "secret_exfiltration" in attack_chain:
            chain_bonus += 1.0

        if "destructive_action" in attack_chain:
            chain_bonus += 1.0

        if len(set(attack_chain)) >= 3:
            chain_bonus += 0.5

        score = min(10.0, base_score + chain_bonus)

        rationale = [
            f"Detected {len(findings)} unique attack findings.",
            f"Highest severity finding: {max_severity}.",
            f"Attack chain: {' -> '.join(attack_chain)}.",
            f"Attack graph nodes: {len(attack_graph.nodes)}.",
            f"Attack graph edges: {len(attack_graph.edges)}.",
        ]

        return AttackAssessment(
            severity=max_severity,
            score=score,
            success=score >= 6.0,
            attack_chain=attack_chain,
            findings=findings,
            attack_graph=attack_graph,
            rationale=rationale,
            metadata={
                "finding_count": len(findings),
                "predicate_hit_count": len(result.predicate_hits),
                "unique_predicates": sorted(set(attack_chain)),
                "entry_points": attack_graph.entry_points,
                "terminal_nodes": attack_graph.terminal_nodes,
            },
        )