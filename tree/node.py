from abc import ABC, abstractmethod

from tokenizer import Token


class Node(ABC):
    @abstractmethod
    def evaluate(self):
        pass


class BinaryOperatorNode(Node):
    def __init__(self, token: Token, left: Node, right: Node):
        self.token = token
        self.left = left
        self.right = right

    # self.evaluate() left to implement by subclassing


class ValueNode(Node):
    def __init__(self, token: Token):
        self.token = token

    # self.evaluate() left to implement by subclassing


class ParentNode(Node):
    def __init__(self, node: Node):
        self.node = node

    def evaluate(self):
        return self.node.evaluate()


Tree = ParentNode
