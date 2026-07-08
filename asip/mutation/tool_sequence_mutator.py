from __future__ import annotations

from dataclasses import replace

from asip.models.attack_plan import AttackPlan
from asip.mutation.mutation_strategy import MutationStrategy


class ToolSequenceMutator(MutationStrategy):
    name = "tool_sequence_mutator"

    def mutate(self, plan: AttackPlan) -> list[AttackPlan]:
        family = str(plan.metadata.get("family", ""))

        variants: list[str] = []

        if "exfil" in family or "share" in family:
            variants = [
                "encoded_exfiltration",
                "delayed_exfiltration",
                "read_then_share",
            ]

        elif "write" in family:
            variants = [
                "destructive_write",
                "overwrite_secret",
                "write_after_read",
            ]

        elif "email" in family:
            variants = [
                "confused_deputy_email",
                "credential_email",
                "email_after_file_read",
            ]

        mutations: list[AttackPlan] = []

        for variant in variants:
            mutations.append(
                replace(
                    plan,
                    metadata={
                        **plan.metadata,
                        "mutation": self.name,
                        "mutation_type": "family_variant",
                        "family": variant,
                    },
                )
            )

        return mutations