from __future__ import annotations

from abc import ABC, abstractmethod

from human_math.symbolics.nodes import Node, BinaryOperatorNode, EvaluateError, CommutativeAssociativeOperatorNode


class NodeWithOperatorSupport(Node, ABC):

    def __add__(self, other: Node | float) -> Node:
        if isinstance(other, Node):
            return Add(self, other)

        return self + Value(other)

    __radd__ = __add__

    def __sub__(self, other: Node | float) -> Node:
        if isinstance(other, Node):
            return Sub(self, other)

        return self - Value(other)

    __rsub__ = __sub__

    def __mul__(self, other: Node | float) -> Node:
        if isinstance(other, Node):
            return Mul(self, other)

        return self * Value(other)

    __rmul__ = __mul__

    def __truediv__(self, other: Node | float) -> Node:
        if isinstance(other, Node):
            return Div(self, other)

        return self / Value(other)

    __rtruediv__ = __truediv__

    def __pow__(self, other: Node | float) -> Node:
        if isinstance(other, Node):
            return Pow(self, other)

        return self ** Value(other)

    __rpow__ = __pow__

    def __mod__(self, other: Node | float) -> Node:
        if isinstance(other, Node):
            return Mod(self, other)

        return self % Value(other)

    __rmod__ = __mod__


class ReducibleBinaryOperator(BinaryOperatorNode, ABC):
    def reduce(self) -> Node:
        if isinstance(self.left, Value) and isinstance(self.right, Value):
            return self.evaluate()
        else:
            return type(self)(self.left.reduce(), self.right.reduce())

class CommutativeAssociativeReducibleOperatorNode(CommutativeAssociativeOperatorNode, ABC):
    def reduce(self) -> Node:
        if all(isinstance(c, Value) for c in self.childs):
            return self.evaluate()
        else:
            return type(self)(*(c.reduce() for c in self.childs))


class FunctionNode(NodeWithOperatorSupport, ABC):
    name: str
    arg: Node

    def __init__(self, arg: Node):
        self.arg = arg

    @classmethod
    @abstractmethod
    def call(cls, arg: Node) -> Value:
        pass

    def evaluate(self) -> Value:
        try:
            return self.call(self.arg)
        except Exception as exc:
            raise EvaluateError(
                f"error while evaluating function call {self.name}({self.arg})"
            ) from exc

    def reduce(self) -> Node:
        if isinstance(self.arg, Value):
            return self.evaluate()
        return self

    def __repr__(self) -> str:
        arg_str = f"{self.arg}"
        if arg_str[0] == '(' and arg_str[-1] == ')':
            return f"{self.name}{self.arg}"
        else:
            return f"{self.name}({self.arg})"

    def matches_raw(self, pattern: FunctionNode) -> bool:  # type: ignore
        return self.arg.matches(pattern.arg)


class Value(NodeWithOperatorSupport):

    def __init__(self, value: float):
        self.value = value

    def evaluate(self) -> Value:

        if isinstance(self.value, Node):
            return self.value.evaluate()
        return self

    def __repr__(self) -> str:
        if (not isinstance(self.value, Node)) and self.value.is_integer():
            return repr(int(self.value))
        return repr(self.value)

    def matches_raw(self, pattern: Value) -> bool:  # type: ignore
        return pattern.value == self.value


class Constant(Value):
    def __init__(self, value: float, name: str):
        super().__init__(value)
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def matches_raw(self, pattern: Constant) -> bool:  # type: ignore
        return pattern.name == self.name and pattern.value == self.value


class Variable(NodeWithOperatorSupport):

    def __init__(self, name: str):
        self.name = name

    def evaluate(self) -> Value:
        raise EvaluateError("can't evaluate a variable")

    def reduce(self) -> Node:
        return self

    def replace(self, name: str, value: Node) -> Node:
        if self.name == name:
            return value
        else:
            return self

    def __repr__(self) -> str:
        return self.name

    def matches_raw(self, pattern: Variable) -> bool:  # type: ignore
        # print(f"{self = }, {pattern = }")
        return self.name == pattern.name


class Add(CommutativeAssociativeReducibleOperatorNode, NodeWithOperatorSupport):
    def evaluate(self) -> Value:
        return Value(sum(c.evaluate().value for c in self.childs))

    def __repr__(self) -> str:
        return ' + '.join(map(repr, self.childs))


class Sub(ReducibleBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self) -> Value:
        return Value(self.left.evaluate().value - self.right.evaluate().value)

    def __repr__(self) -> str:
        return f"({repr(self.left)} - {repr(self.right)})"


class Mul(CommutativeAssociativeReducibleOperatorNode, NodeWithOperatorSupport):
    def evaluate(self) -> Value:
        result = 1
        for c in self.childs:
            result *= c.evaluate().value
        return Value(result)

    def __repr__(self) -> str:
        return ' * '.join(map(repr, self.childs))


class Div(ReducibleBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self) -> Value:
        left = self.left.evaluate().value
        right = self.right.evaluate().value
        if right == 0:
            raise EvaluateError(f"can't divide {left} by zero")
        return Value(left / right)

    def __repr__(self) -> str:
        return f"({repr(self.left)} / {repr(self.right)})"


class Pow(ReducibleBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self) -> Value:
        return Value(self.left.evaluate().value ** self.right.evaluate().value)

    def __repr__(self) -> str:
        return f"({repr(self.left)} ** {repr(self.right)})"


class Mod(ReducibleBinaryOperator, NodeWithOperatorSupport):
    def evaluate(self) -> Value:
        return Value(self.left.evaluate().value % self.right.evaluate().value)

    def __repr__(self) -> str:
        return f"({repr(self.left)} % {repr(self.right)})"
