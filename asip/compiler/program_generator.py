from __future__ import annotations

import importlib
import random
from dataclasses import dataclass, field
from typing import Iterable

from asip.compiler.attack_instruction import AttackInstruction, AttackStage
from asip.compiler.attack_program import AttackProgram


FAMILY_MODULES = (
    "asip.compiler.families.credential",
    "asip.compiler.families.prompt_injection",
    "asip.compiler.families.authority_spoofing",
    "asip.compiler.families.tool_abuse",
    "asip.compiler.families.reasoning",
    "asip.compiler.families.planning",
    "asip.compiler.families.memory",
    "asip.compiler.families.encoding",
    "asip.compiler.families.persistence",
)


@dataclass(slots=True)
class ProgramGenerator:
    """
    Generates new structured AttackProgram objects from family templates.

    This is the bridge from a static attack library to compiler-driven
    attack synthesis.
    """

    max_programs: int = 250
    min_stages: int = 2
    max_stages: int = 7
    random_seed: int = 42
    family_modules: tuple[str, ...] = FAMILY_MODULES

    rng: random.Random = field(init=False)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.random_seed)

    def generate(self) -> list[AttackProgram]:
        seeds = self.load_seed_programs()

        generated: list[AttackProgram] = []
        seen: set[tuple] = set()

        for program in seeds:
            if self._valid(program):
                key = program.signature()
                if key not in seen:
                    seen.add(key)
                    generated.append(program)

        attempts = 0
        max_attempts = self.max_programs * 20

        while len(generated) < self.max_programs and attempts < max_attempts:
            attempts += 1

            program = self._synthesize(seeds)

            if not self._valid(program):
                continue

            key = program.signature()

            if key in seen:
                continue

            seen.add(key)
            generated.append(program)

        return generated[: self.max_programs]

    def load_seed_programs(self) -> list[AttackProgram]:
        programs: list[AttackProgram] = []

        for module_name in self.family_modules:
            try:
                module = importlib.import_module(module_name)
            except ModuleNotFoundError:
                continue

            all_programs = getattr(module, "all_programs", None)

            if all_programs is None:
                continue

            programs.extend(all_programs())

        return programs

    def by_family(self) -> dict[str, list[AttackProgram]]:
        families: dict[str, list[AttackProgram]] = {}

        for program in self.load_seed_programs():
            family = str(program.metadata.get("family", "unknown"))
            families.setdefault(family, []).append(program)

        return families

    def _synthesize(
        self,
        seeds: list[AttackProgram],
    ) -> AttackProgram:
        if not seeds:
            raise ValueError("ProgramGenerator has no seed programs.")

        selected = self.rng.sample(
            seeds,
            k=min(
                self.rng.randint(2, min(4, len(seeds))),
                len(seeds),
            ),
        )

        stages: list[AttackStage] = []

        for program in selected:
            if not program.stages:
                continue

            stage = self.rng.choice(program.stages)

            stages.append(
                self._copy_stage(stage)
            )

        stages = self._normalize_stage_count(stages)

        name = "generated_" + "_".join(
            str(p.metadata.get("family", p.name))
            for p in selected
        )

        families = sorted(
            {
                str(p.metadata.get("family", "unknown"))
                for p in selected
            }
        )

        techniques = sorted(
            {
                str(p.metadata.get("technique", "unknown"))
                for p in selected
                if p.metadata.get("technique")
            }
        )

        return AttackProgram(
            name=name[:120],
            goal=selected[0].goal,
            stages=stages,
            metadata={
                "family": "generated",
                "source_families": families,
                "source_programs": [p.name for p in selected],
                "techniques": techniques,
                "generator": "ProgramGenerator",
                "stage_count": len(stages),
            },
        )

    def _normalize_stage_count(
        self,
        stages: list[AttackStage],
    ) -> list[AttackStage]:
        if len(stages) < self.min_stages:
            while len(stages) < self.min_stages and stages:
                stages.append(
                    self._copy_stage(
                        self.rng.choice(stages)
                    )
                )

        if len(stages) > self.max_stages:
            stages = stages[: self.max_stages]

        return stages

    def _copy_stage(
        self,
        stage: AttackStage,
    ) -> AttackStage:
        return AttackStage(
            name=stage.name,
            instructions=[
                AttackInstruction(
                    opcode=i.opcode,
                    target=i.target,
                    variable=i.variable,
                    value=i.value,
                    transform=i.transform,
                    metadata=dict(i.metadata),
                )
                for i in stage.instructions
            ],
            metadata=dict(stage.metadata),
        )

    def _valid(
        self,
        program: AttackProgram,
    ) -> bool:
        if not program.stages:
            return False

        if len(program.stages) < 1:
            return False

        if len(program.stages) > self.max_stages:
            return False

        instructions = program.instructions()

        if not instructions:
            return False

        for stage in program.stages:
            if not stage.instructions:
                return False

        return True

    def statistics(self) -> dict:
        seeds = self.load_seed_programs()
        families = self.by_family()

        return {
            "seed_programs": len(seeds),
            "families": {
                family: len(programs)
                for family, programs in sorted(families.items())
            },
            "max_programs": self.max_programs,
            "min_stages": self.min_stages,
            "max_stages": self.max_stages,
            "random_seed": self.random_seed,
        }