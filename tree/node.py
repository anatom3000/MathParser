from abc import ABC, abstractmethod

from tokens import Token


class Node(ABC):
    @abstractmethod
    def evaluate(self):
        pass


class BinaryOperatorNode(Node, ABC):
    def __init__(self, token: Token, left: Node, right: Node):
        self.token = token
        self.left = left
        self.right = right

    # self.evaluate() left to implement by subclassing
    # should be something like
    # def evaluate(self):
    #     return self.left + self.right


class ValueNode(Node, ABC):
    def __init__(self, token: Token):
        self.token = token

    # self.evaluate() left to implement by subclassing
    # should be something like
    # def evaluate(self):
    #     return float(self.token.symbols)


class UnaryOperatorNode(Node, ABC):
    def __init__(self, node: Node):
        self.node = node

    # self.evaluate() left to implement by subclassing
    # should be something like
    # def evaluate(self):
    #     return -1 * self.node.evaluate()


class Tree(UnaryOperatorNode):

    def evaluate(self):
        return self.node.evaluate()
