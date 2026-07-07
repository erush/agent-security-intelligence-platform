from __future__ import annotations

from collections import Counter

from asip.execution.execution_result import ExecutionResult


def print_attack_plan_report(results: list[ExecutionResult]) -> None:
    ranked = sorted(
        results,
        key=lambda r: (
            r.success,
            r.assessment.score if r.assessment else 0.0,
            len(r.findings),
            len(r.predicate_hits),
            len(set(r.tool_sequence)),
        ),
        reverse=True,
    )

    print()
    print("=" * 80)
    print("ASIP Attack Plan Execution Report")
    print("=" * 80)
    print(f"Plans executed : {len(results)}")
    print(f"Successes      : {sum(r.success for r in results)}")
    print(f"Findings       : {sum(len(r.findings) for r in results)}")
    print(f"Predicate hits : {sum(len(r.predicate_hits) for r in results)}")
    print()

    print("Ranked Plans")
    print("-" * 80)

    for idx, result in enumerate(ranked, start=1):
        assessment = result.assessment
        graph = assessment.attack_graph if assessment else None

        print(f"{idx}. plan_id={result.plan.plan_id}")
        print(f"   goal       : {result.plan.goal}")
        print(f"   family     : {result.plan.metadata.get('family')}")
        print(f"   success    : {result.success}")

        if assessment:
            print(f"   severity   : {assessment.severity}")
            print(f"   score      : {assessment.score:.2f}")
            print(f"   chain      : {' -> '.join(assessment.attack_chain) or 'none'}")
        else:
            print("   severity   : none")
            print("   score      : 0.00")
            print("   chain      : none")

        if graph:
            print(f"   graph      : nodes={len(graph.nodes)} edges={len(graph.edges)}")
            print(f"   entry      : {', '.join(graph.entry_points) or 'none'}")
            print(f"   terminal   : {', '.join(graph.terminal_nodes) or 'none'}")

            if graph.edges:
                print("   graph edges:")
                for edge in graph.edges:
                    print(
                        f"      - {edge.source}"
                        f" -> {edge.target}"
                        f" ({edge.relationship})"
                    )

        print(f"   tools      : {' -> '.join(result.tool_sequence) or 'none'}")

        if result.findings:
            print("   findings   :")
            for finding in result.findings:
                print(
                    f"      - {finding.predicate}"
                    f" ({finding.severity})"
                    f" :: occurrences={finding.occurrences}"
                    f" :: events={finding.first_event_index}-{finding.last_event_index}"
                )
        else:
            print("   findings   : none")

        if assessment and assessment.rationale:
            print("   rationale  :")
            for item in assessment.rationale:
                print(f"      - {item}")

        print("   tool events:")

        for event in result.trace.get("tool_events", []):
            print(
                f"      - {event.get('name')} "
                f"ok={event.get('ok')} "
                f"source={event.get('source')}"
            )
            print(f"        args={event.get('args')}")

            output = str(event.get("output", ""))

            if output:
                print(f"        output={output[:240]}")

        print()

    tools = Counter()
    finding_counts = Counter()
    predicate_counts = Counter()
    severity_counts = Counter()
    edge_counts = Counter()

    for result in results:
        tools.update(result.tool_sequence)
        finding_counts.update(finding.predicate for finding in result.findings)
        predicate_counts.update(hit.predicate for hit in result.predicate_hits)

        if result.assessment:
            severity_counts.update([result.assessment.severity])

            if result.assessment.attack_graph:
                edge_counts.update(
                    f"{edge.source}->{edge.target}"
                    for edge in result.assessment.attack_graph.edges
                )

    print("Tool Frequency")
    print("-" * 80)
    for tool, count in tools.most_common():
        print(f"{tool}: {count}")

    print()
    print("Finding Frequency")
    print("-" * 80)
    for finding, count in finding_counts.most_common():
        print(f"{finding}: {count}")

    print()
    print("Assessment Severity Frequency")
    print("-" * 80)
    for severity, count in severity_counts.most_common():
        print(f"{severity}: {count}")

    print()
    print("Attack Graph Edge Frequency")
    print("-" * 80)
    for edge, count in edge_counts.most_common():
        print(f"{edge}: {count}")

    print()
    print("Raw Predicate Hit Frequency")
    print("-" * 80)
    for predicate, count in predicate_counts.most_common():
        print(f"{predicate}: {count}")