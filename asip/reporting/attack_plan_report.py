from __future__ import annotations

from collections import Counter

from asip.execution.execution_result import ExecutionResult


def print_attack_plan_report(results: list[ExecutionResult]) -> None:
    ranked = sorted(
        results,
        key=lambda r: (
            r.success,
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
        print(f"{idx}. plan_id={result.plan.plan_id}")
        print(f"   goal       : {result.plan.goal}")
        print(f"   family     : {result.plan.metadata.get('family')}")
        print(f"   success    : {result.success}")
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
    predicate_counts = Counter()
    finding_counts = Counter()

    for result in results:
        tools.update(result.tool_sequence)
        predicate_counts.update(
            hit.predicate
            for hit in result.predicate_hits
        )
        finding_counts.update(
            finding.predicate
            for finding in result.findings
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

    print("Raw Predicate Hit Frequency")
    print("-" * 80)

    for predicate, count in predicate_counts.most_common():
        print(f"{predicate}: {count}")