from abc import ABC

from symbolics.nodes import Node, BinaryOperatorNode


class NodeWithOperatorSupport(Node, ABC):

    def __add__(self, other):
        if isinstance(other, Node):
            return Add(self, other)
        else:
            return self + Value(other)

    def __sub__(self, other):
        if isinstance(other, Node):
            return Sub(self, other)
        else:
            return self - Value(other)

    def __mul__(self, other):
        if isinstance(other, Node):
            return Mul(self, other)
        else:
            return self * Value(other)

    def __truediv__(self, other):
        if isinstance(other, Node):
            return Div(self, other)
        else:
            return self / Value(other)

    def __pow__(self, other):
        if isinstance(other, Node):
            return Pow(self, other)
        else:
            return self ** Value(other)

    def __mod__(self, other):
        if isinstance(other, Node):
            return Mod(self, other)
        else:
            return self % Value(other)


class ReduceableBinaryOperator(BinaryOperatorNode, ABC):
    def reduce(self):
        if isinstance(self.left, Value) and isinstance(self.right, Value):
            return self.evaluate()
        else:
            return type(self)(self.left.reduce(), self.right.reduce())


class Value(NodeWithOperatorSupport):

    def __init__(self, value: float):
        self.value = value

    def evaluate(self):
        return self.value

    def reduce(self):
        return self.evaluate()

    def __repr__(self):
        return repr(self.value)


class Add(ReduceableBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()

    def __repr__(self):
        return f"{repr(self.left)} + {repr(self.right)}"


class Sub(ReduceableBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()

    def __repr__(self):
        return f"{repr(self.left)} - {repr(self.right)}"


class Mul(ReduceableBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self):
        return self.left.evaluate() * self.right.evaluate()

    def __repr__(self):
        return f"{repr(self.left)} * {repr(self.right)}"


class Div(ReduceableBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self):
        return self.left.evaluate() / self.right.evaluate()

    def __repr__(self):
        return f"{repr(self.left)} / {repr(self.right)}"


class Pow(ReduceableBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self):
        return self.left.evaluate() ** self.right.evaluate()

    def __repr__(self):
        return f"{repr(self.left)} ** {repr(self.right)}"


class Mod(ReduceableBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self):
        return self.left.evaluate() % self.right.evaluate()

    def __repr__(self):
        return f"{repr(self.left)} % {repr(self.right)}"
