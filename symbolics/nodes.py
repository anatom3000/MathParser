from __future__ import annotations
from abc import ABC, abstractmethod

from symbolics import operators


class EvaluateError(ValueError):
    pass


class Node(ABC):
    @abstractmethod
    def evaluate(self) -> operators.Value:
        pass

    def reduce(self) -> Node:
        return self.evaluate()


class BinaryOperatorNode(Node, ABC):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    # self.evaluate() left to implement by subclassing
    # should be something like
    # def evaluate(self):
    #     return self.left + self.right


class UnaryOperatorNode(Node, ABC):
    def __init__(self, node: Node):
        self.node = node

    # self.evaluate() left to implement by subclassing
    # should be something like
    # def evaluate(self):
    #     return -1 * self.node.evaluate()
