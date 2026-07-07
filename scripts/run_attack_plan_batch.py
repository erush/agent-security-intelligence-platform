from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SDK_ROOT = ROOT / "external" / "kaggle_jed"

if str(SDK_ROOT) not in sys.path:
    sys.path.insert(0, str(SDK_ROOT))

from aicomp_sdk.agents import build_agent
from aicomp_sdk.attacks.baselines.guardrail_rules import Guardrail
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.core.predicates import eval_predicates

from asip.adapters.kaggle_jed import KaggleJEDAdapter
from asip.execution.attack_executor import AttackExecutor
from asip.planner.attack_goal import AttackGoal
from asip.planner.attack_planner import AttackPlanner
from asip.replay.sqlite_store import SQLiteReplayStore
from asip.reporting.attack_plan_report import print_attack_plan_report


def build_env() -> SandboxEnv:
    fixtures = SDK_ROOT / "aicomp_sdk" / "fixtures"

    return SandboxEnv(
        seed=123,
        fixtures_dir=fixtures,
        agent=build_agent("deterministic"),
        guardrail=Guardrail(),
    )


def main() -> None:
    goal = AttackGoal(
        name="discover_replayable_agent_security_failure",
        description="Generate attack plans that create scored predicate violations in the Kaggle JED sandbox.",
        target_predicates=(
            "EXFILTRATION",
            "UNTRUSTED_TO_ACTION",
            "DESTRUCTIVE_WRITE",
            "CONFUSED_DEPUTY",
        ),
    )

    planner = AttackPlanner()

    plans = planner.plan(goal)

    adapter = KaggleJEDAdapter(
        env=build_env(),
        eval_predicates_fn=eval_predicates,
    )

    executor = AttackExecutor(adapter=adapter)

    store = SQLiteReplayStore()

    results = []

    for plan in plans:
        result = executor.execute(plan)
        store.save(result)
        results.append(result)

    print_attack_plan_report(results)

    print()
    print(f"Replay warehouse rows: {store.count()}")
    print()


if __name__ == "__main__":
    main()