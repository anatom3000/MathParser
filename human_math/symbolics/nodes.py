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


class BinaryOperatorNode(Node, ABC):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    def replace(self, name: str, value: Node) -> Node:
        self.left = self.left.replace(name, value)
        self.right = self.right.replace(name, value)

        return self

    # self.evaluate() left to implement by subclassing
    # should be something like
    # def evaluate(self):
    #     return self.left + self.right
