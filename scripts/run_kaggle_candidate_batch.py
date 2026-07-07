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
from asip.evaluation.kaggle_jed_evaluator import KaggleJEDEvaluator
from asip.reporting.kaggle_jed_report import print_kaggle_jed_report
from asip.strategies.prompt_bank_strategy import PromptBankStrategy


def build_env() -> SandboxEnv:
    fixtures = SDK_ROOT / "aicomp_sdk" / "fixtures"

    return SandboxEnv(
        seed=123,
        fixtures_dir=fixtures,
        agent=build_agent("deterministic"),
        guardrail=Guardrail(),
    )


def main() -> None:
    adapter = KaggleJEDAdapter(
        env=build_env(),
        eval_predicates_fn=eval_predicates,
    )

    evaluator = KaggleJEDEvaluator(adapter)
    strategy = PromptBankStrategy()

    evaluations = [
        evaluator.evaluate(candidate)
        for candidate in strategy.generate()
    ]

    print_kaggle_jed_report(evaluations)


if __name__ == "__main__":
    main()