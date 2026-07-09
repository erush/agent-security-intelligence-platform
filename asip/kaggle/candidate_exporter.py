from __future__ import annotations

from dataclasses import dataclass

from aicomp_sdk.attacks import AttackCandidate

from asip.campaign.attack_campaign import AttackCampaign


MAX_MESSAGES = 32
MAX_MESSAGE_CHARS = 2_000


@dataclass(slots=True)
class CandidateExporter:
    max_candidates: int = 2000

    def export(
        self,
        campaign: AttackCampaign,
    ) -> list[AttackCandidate]:
        ranked = sorted(
            campaign.executions,
            key=lambda r: float(
                r.metadata.get("fitness", 0.0)
            ),
            reverse=True,
        )

        candidates: list[AttackCandidate] = []
        seen: set[tuple[str, ...]] = set()

        for result in ranked:
            messages = self._messages(result)

            if not messages:
                continue

            if messages in seen:
                continue

            seen.add(messages)

            candidates.append(
                AttackCandidate.from_messages(messages)
            )

            if len(candidates) >= self.max_candidates:
                break

        return candidates

    def _messages(
        self,
        result,
    ) -> tuple[str, ...]:
        prompts = result.metadata.get(
            "executed_prompts",
            [],
        )

        cleaned = []

        for prompt in prompts[:MAX_MESSAGES]:
            text = str(prompt).strip()

            if not text:
                continue

            cleaned.append(
                text[:MAX_MESSAGE_CHARS]
            )

        return tuple(cleaned)