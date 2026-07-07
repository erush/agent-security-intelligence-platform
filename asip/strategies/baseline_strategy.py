from __future__ import annotations

from dataclasses import dataclass

from asip.models.candidate import Candidate


@dataclass(slots=True)
class BaselineStrategy:
    """
    Minimal attack strategy.

    Future implementations will search, branch,
    replay, mutate and score.
    """

    name: str = "baseline"

    def generate(self, prompt: str) -> list[Candidate]:

        return [
            Candidate(
                strategy=self.name,
                prompt=prompt,
                metadata={}
            )
        ]