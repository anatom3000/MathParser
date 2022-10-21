from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence


class Token(ABC):
    symbols: str

    def __init__(self, symbols: str):
        self.symbols = symbols

    @classmethod
    @abstractmethod
    def is_candidate(cls, symbols: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def is_valid(cls, symbols: str) -> bool:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<\"{self.symbols}\">"


class SimpleExplcitToken(Token):
    name: str

    @classmethod
    def is_candidate(cls, symbols: str) -> bool:
        return len(symbols) <= len(
            cls.name) and cls.name[:len(symbols)] == symbols

    @classmethod
    def is_valid(cls, symbols: str) -> bool:
        return symbols == cls.name


class MultipleExplicitToken(Token):
    names: Sequence[str]

    @classmethod
    def is_candidate(cls, symbols: str) -> bool:
        return any([
            len(symbols) <= len(name) and name[:len(symbols)] == symbols
            for name in cls.names
        ])

    @classmethod
    def is_valid(cls, symbols: str) -> bool:
        return symbols in cls.names


class Unknown(Token):

    @classmethod
    def is_candidate(cls, symbols: str) -> bool:
        return True

    @classmethod
    def is_valid(cls, symbols: str) -> bool:
        return True
