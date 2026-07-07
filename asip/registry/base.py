from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class RegistryEntry(Generic[T]):
    name: str
    value: T
    description: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    version: str = "0.1.0"


class Registry(Generic[T]):
    def __init__(self, name: str) -> None:
        self.name = name
        self._entries: dict[str, RegistryEntry[T]] = {}

    def register(
        self,
        name: str,
        value: T,
        description: str = "",
        tags: Iterable[str] = (),
        version: str = "0.1.0",
    ) -> None:
        if name in self._entries:
            raise ValueError(f"{self.name} registry already contains entry: {name}")

        self._entries[name] = RegistryEntry(
            name=name,
            value=value,
            description=description,
            tags=tuple(tags),
            version=version,
        )

    def get(self, name: str) -> T:
        if name not in self._entries:
            raise KeyError(f"{self.name} registry does not contain entry: {name}")

        return self._entries[name].value

    def entry(self, name: str) -> RegistryEntry[T]:
        if name not in self._entries:
            raise KeyError(f"{self.name} registry does not contain entry: {name}")

        return self._entries[name]

    def names(self) -> list[str]:
        return sorted(self._entries)

    def entries(self) -> list[RegistryEntry[T]]:
        return [self._entries[name] for name in self.names()]

    def values(self) -> list[T]:
        return [entry.value for entry in self.entries()]

    def __contains__(self, name: str) -> bool:
        return name in self._entries

    def __len__(self) -> int:
        return len(self._entries)