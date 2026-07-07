from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class PromptMutation(Protocol):
    """Contract for all prompt mutations."""

    name: str

    def mutate(self, prompt: str) -> str:
        ...


@dataclass(slots=True)
class IdentityMutation:
    """Return the prompt unchanged."""

    name: str = "identity"

    def mutate(self, prompt: str) -> str:
        return prompt


@dataclass(slots=True)
class PrefixMutation:
    """Prepends text to a prompt."""

    prefix: str
    name: str = "prefix"

    def mutate(self, prompt: str) -> str:
        return f"{self.prefix}\n\n{prompt}"


@dataclass(slots=True)
class SuffixMutation:
    """Appends text to a prompt."""

    suffix: str
    name: str = "suffix"

    def mutate(self, prompt: str) -> str:
        return f"{prompt}\n\n{self.suffix}"


@dataclass(slots=True)
class ChainMutation:
    """Execute multiple mutations sequentially."""

    mutations: list[PromptMutation]
    name: str = "chain"

    def mutate(self, prompt: str) -> str:
        current = prompt
        for mutation in self.mutations:
            current = mutation.mutate(current)
        return current