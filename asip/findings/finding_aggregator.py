from __future__ import annotations

from collections import defaultdict

from asip.findings.attack_finding import AttackFinding
from asip.predicates.predicate_hit import PredicateHit


SEVERITY_RANK = {
    "info": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


class FindingAggregator:
    def aggregate(self, hits: list[PredicateHit]) -> list[AttackFinding]:
        grouped: dict[str, list[PredicateHit]] = defaultdict(list)

        for hit in hits:
            grouped[hit.predicate].append(hit)

        findings: list[AttackFinding] = []

        for predicate, predicate_hits in grouped.items():
            sorted_hits = sorted(
                predicate_hits,
                key=lambda hit: hit.event_index,
            )

            severity = max(
                (hit.severity for hit in sorted_hits),
                key=lambda value: SEVERITY_RANK.get(value, 0),
            )

            findings.append(
                AttackFinding(
                    predicate=predicate,
                    severity=severity,
                    message=sorted_hits[0].message,
                    first_event_index=sorted_hits[0].event_index,
                    last_event_index=sorted_hits[-1].event_index,
                    occurrences=len(sorted_hits),
                    evidence=sorted_hits,
                    metadata={
                        "event_indexes": [
                            hit.event_index
                            for hit in sorted_hits
                        ],
                    },
                )
            )

        return sorted(
            findings,
            key=lambda finding: (
                SEVERITY_RANK.get(finding.severity, 0),
                finding.occurrences,
                finding.predicate,
            ),
            reverse=True,
        )