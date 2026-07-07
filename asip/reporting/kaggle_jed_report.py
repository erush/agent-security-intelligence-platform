from __future__ import annotations

from collections import Counter

from asip.evaluation.kaggle_jed_evaluator import KaggleJEDEvaluation


def print_kaggle_jed_report(evaluations: list[KaggleJEDEvaluation]) -> None:
    ranked = sorted(evaluations, key=lambda item: item.score, reverse=True)

    print()
    print("=" * 80)
    print("ASIP Kaggle JED Candidate Batch")
    print("=" * 80)
    print(f"Candidates evaluated : {len(evaluations)}")
    print(f"Predicate hits       : {sum(len(e.predicate_names) for e in evaluations)}")
    print()

    print("Top Candidates")
    print("-" * 80)

    for idx, evaluation in enumerate(ranked[:10], start=1):
        print(f"{idx}. score={evaluation.score}")
        print(f"   prompt     : {evaluation.candidate.prompt}")
        print(f"   tools      : {' -> '.join(evaluation.tool_sequence) or 'none'}")
        print(f"   predicates : {', '.join(evaluation.predicate_names) or 'none'}")
        print()

    tools = Counter()
    predicates = Counter()

    for evaluation in evaluations:
        tools.update(evaluation.tool_sequence)
        predicates.update(evaluation.predicate_names)

    print("Tool Frequency")
    print("-" * 80)
    for tool, count in tools.most_common():
        print(f"{tool}: {count}")

    print()
    print("Predicate Frequency")
    print("-" * 80)
    for predicate, count in predicates.most_common():
        print(f"{predicate}: {count}")