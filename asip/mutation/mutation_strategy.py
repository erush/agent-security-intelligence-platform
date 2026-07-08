from __future__ import annotations

from abc import ABC, abstractmethod

from asip.models.attack_plan import AttackPlan


class MutationStrategy(ABC):
    name: str = "base"

    @abstractmethod
    def mutate(self, plan: AttackPlan) -> list[AttackPlan]:
        raise NotImplementedError