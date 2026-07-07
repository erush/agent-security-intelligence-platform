from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AttackGoal:
    name: str
    description: str
    target_predicates: tuple[str, ...]