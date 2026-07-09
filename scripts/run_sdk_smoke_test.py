from __future__ import annotations

import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SDK_ROOT = ROOT / "external" / "kaggle_jed"
FIXTURES = SDK_ROOT / "aicomp_sdk" / "fixtures"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SDK_ROOT))


def main() -> int:
    from aicomp_sdk.core.env.api import EnvSelection
    from aicomp_sdk.evaluation.runner import evaluate_redteam

    from asip.kaggle.attack_algorithm import AttackAlgorithm

    print()
    print("=" * 80)
    print("ASIP Kaggle SDK Smoke Test")
    print("=" * 80)
    print(f"Root     : {ROOT}")
    print(f"SDK      : {SDK_ROOT}")
    print(f"Fixtures : {FIXTURES}")

    if not FIXTURES.exists():
        raise FileNotFoundError(f"Missing fixtures directory: {FIXTURES}")

    print()
    print("Running SDK evaluator...")
    print("-" * 80)

    execution = evaluate_redteam(
        AttackAlgorithm,
        budget_s=30.0,
        env_selection=EnvSelection.SANDBOX,
        fixtures_dir=FIXTURES,
        attack_config={
            "population_size": 3,
            "generations": 1,
            "max_candidates": 25,
        },
    )

    attack = execution.attack

    print()
    print("=" * 80)
    print("Smoke Test Result")
    print("=" * 80)
    print(f"Final Score       : {execution.final_score}")

    if attack is None:
        print("Attack execution  : None")
        return 1

    print(f"Findings Count    : {attack.findings_count}")
    print(f"Unique Cells      : {attack.unique_cells}")
    print(f"Raw Score         : {attack.score_raw}")
    print(f"Normalized Score  : {attack.score}")
    print(f"Time Taken        : {attack.time_taken:.2f}s")
    print(f"Guardrail         : {attack.guardrail_id}@{attack.guardrail_version}")

    print()
    print("Validated Findings")
    print("-" * 80)

    for index, finding in enumerate(attack.findings[:10], start=1):
        predicates = finding.get("predicates", [])
        messages = finding.get("user_messages", [])
        trace = finding.get("trace", {})
        tools = [
            event.get("name")
            for event in trace.get("tool_events", [])
            if event.get("ok") is True
        ]

        print(f"{index}. predicates={len(predicates)} messages={len(messages)} tools={tools}")

    print()
    print("SDK smoke test completed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        print()
        print("=" * 80)
        print("SDK Smoke Test Failed")
        print("=" * 80)
        traceback.print_exc()
        raise