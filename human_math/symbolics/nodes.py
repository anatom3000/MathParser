from __future__ import annotations

from abc import ABC, abstractmethod

from human_math.symbolics import operators


class EvaluateError(ValueError):
    pass


class Node(ABC):
    @abstractmethod
    def evaluate(self) -> operators.Value:
        pass

    def reduce(self) -> Node:
        return self.evaluate()

    def replace(self, name: str, value: Node) -> Node:
        return self

    def matches(self, pattern: Node) -> bool:
        if isinstance(pattern, Wildcard):
            return True
        elif isinstance(pattern, self.__class__):
            return self.matches_raw(pattern)
        else:
            return False

    @abstractmethod
    def matches_raw(self, pattern: Node) -> bool:
        pass


class BinaryOperatorNode(Node, ABC):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    def replace(self, name: str, value: Node) -> Node:
        self.left = self.left.replace(name, value)
        self.right = self.right.replace(name, value)

        return self

    def matches_raw(self, pattern: BinaryOperatorNode) -> bool:
        return self.left.matches(pattern.left) and self.right.matches(pattern.right)

    # self.evaluate() left to implement by subclassing
    # should be something like
    # def evaluate(self):
    #     return self.left + self.right


class Wildcard(Node):
    def matches_raw(self, pattern: Node) -> bool:
        return True

    def evaluate(self) -> operators.Value:
        raise EvaluateError("can't evaluate a wildward (used for pattern matching)")

    def __repr__(self):
        return "<Wildcard>"
