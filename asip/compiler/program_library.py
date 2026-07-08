from __future__ import annotations

from dataclasses import dataclass, field

from asip.compiler.attack_program import AttackProgram
from asip.compiler.program_generator import ProgramGenerator


@dataclass(slots=True)
class ProgramLibrary:
    """
    Central registry for every AttackProgram available to ASIP.

    Sources
    -------
    • Seed programs from handwritten families
    • Generated programs from ProgramGenerator

    Future
    ------
    • EvolutionEngine
    • Warehouse replay imports
    • Learned attack programs
    """

    generator: ProgramGenerator = field(
        default_factory=ProgramGenerator
    )

    _seed_programs: list[AttackProgram] = field(
        default_factory=list,
        init=False,
    )

    _generated_programs: list[AttackProgram] = field(
        default_factory=list,
        init=False,
    )

    def load(self) -> None:
        """
        Load handwritten attack programs.
        """

        self._seed_programs = (
            self.generator.load_seed_programs()
        )

    def generate(self) -> None:
        """
        Generate synthesized attack programs.
        """

        self._generated_programs = (
            self.generator.generate()
        )

    def refresh(self) -> None:
        """
        Rebuild the complete library.
        """

        self.load()
        self.generate()

    @property
    def seed_programs(self) -> list[AttackProgram]:
        return list(self._seed_programs)

    @property
    def generated_programs(self) -> list[AttackProgram]:
        return list(self._generated_programs)

    @property
    def programs(self) -> list[AttackProgram]:
        return (
            self.seed_programs
            + self.generated_programs
        )

    def __len__(self) -> int:
        return len(self.programs)

    def by_family(
        self,
        family: str,
    ) -> list[AttackProgram]:

        return [
            p
            for p in self.programs
            if p.metadata.get("family") == family
        ]

    def names(self) -> list[str]:

        return [
            p.name
            for p in self.programs
        ]

    def statistics(self) -> dict:

        family_counts: dict[str, int] = {}

        for program in self.programs:

            family = str(
                program.metadata.get(
                    "family",
                    "unknown",
                )
            )

            family_counts[family] = (
                family_counts.get(family, 0) + 1
            )

        return {
            "seed_programs": len(
                self._seed_programs
            ),
            "generated_programs": len(
                self._generated_programs
            ),
            "total_programs": len(
                self.programs
            ),
            "families": dict(
                sorted(family_counts.items())
            ),
        }

    def summary(self) -> str:

        stats = self.statistics()

        lines = [
            "=== Program Library ===",
            "",
            f"Seed Programs      : {stats['seed_programs']}",
            f"Generated Programs : {stats['generated_programs']}",
            f"Total Programs     : {stats['total_programs']}",
            "",
            "Families:",
        ]

        for family, count in stats["families"].items():
            lines.append(
                f"  {family:<20} {count}"
            )

        return "\n".join(lines)