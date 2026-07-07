from __future__ import annotations

from collections import Counter

from asip.execution.execution_result import ExecutionResult


def print_attack_plan_report(results: list[ExecutionResult]) -> None:
    ranked = sorted(
        results,
        key=lambda item: (item.success, len(set(item.tool_sequence)), len(item.predicates)),
        reverse=True,
    )

    print()
    print("=" * 80)
    print("ASIP Attack Plan Execution Report")
    print("=" * 80)
    print(f"Plans executed : {len(results)}")
    print(f"Successes      : {sum(result.success for result in results)}")
    print(f"Predicate hits : {sum(len(result.predicates) for result in results)}")
    print()

    print("Ranked Plans")
    print("-" * 80)

    for idx, result in enumerate(ranked, start=1):
        print(f"{idx}. plan_id={result.plan.plan_id}")
        print(f"   goal       : {result.plan.goal}")
        print(f"   family     : {result.plan.metadata.get('family')}")
        print(f"   success    : {result.success}")
        print(f"   tools      : {' -> '.join(result.tool_sequence) or 'none'}")
        print(f"   predicates : {result.predicates or 'none'}")
        print("   tool events:")
        for event in result.trace.get("tool_events", []):
            print(f"      - {event.get('name')} ok={event.get('ok')} source={event.get('source')}")
            print(f"        args={event.get('args')}")
            output = str(event.get("output", ""))
            if output:
                print(f"        output={output[:240]}")
        print()

    tools = Counter()
    predicates = Counter()

    for result in results:
        tools.update(result.tool_sequence)
        predicates.update(str(p.get("predicate", "")) for p in result.predicates)

    print("Tool Frequency")
    print("-" * 80)
    for tool, count in tools.most_common():
        print(f"{tool}: {count}")

    print()
    print("Predicate Frequency")
    print("-" * 80)
    for predicate, count in predicates.most_common():
        if predicate:
            print(f"{predicate}: {count}")