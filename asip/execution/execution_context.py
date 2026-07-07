from __future__ import annotations

from dataclasses import dataclass, field

from asip.core.observation import Observation
from asip.core.working_memory import WorkingMemory


@dataclass(slots=True)
class ExecutionContext:
    """
    Shared execution state for an attack plan.
    """

    memory: WorkingMemory = field(default_factory=WorkingMemory)

    observations: list[Observation] = field(default_factory=list)

    def record(self, observation: Observation) -> None:
        self.observations.append(observation)

        if observation.memory_updates:
            self.memory.update(observation.memory_updates)