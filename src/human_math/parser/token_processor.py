from __future__ import annotations

from abc import abstractmethod, ABC
from collections.abc import MutableSequence

from symbolics import Node
from tokens import Token


class TokenProcessor(ABC):
    @classmethod
    @abstractmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        pass
