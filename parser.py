from tokens import SimpleExplcitToken, MultipleExplicitToken, Token
from tree import BinaryOperatorNode, ValueNode


class Add(SimpleExplcitToken, BinaryOperatorNode):
    name = '+'

    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()


class Sub(SimpleExplcitToken, BinaryOperatorNode):
    name = '-'

    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()


class Mul(SimpleExplcitToken, BinaryOperatorNode):
    name = '*'

    def evaluate(self):
        return self.left.evaluate() * self.right.evaluate()


class Div(SimpleExplcitToken, BinaryOperatorNode):
    name = '/'

    def evaluate(self):
        return self.left.evaluate() / self.right.evaluate()


class Pow(MultipleExplicitToken, BinaryOperatorNode):
    names = ('**', '^')
    def evaluate(self):
        return self.left.evaluate() ** self.right.evaluate()


class Mod(MultipleExplicitToken, BinaryOperatorNode):
    names = ("mod", "%")

    def evaluate(self):
        return self.left.evaluate() % self.right.evaluate()


class OpeningParenthese(SimpleExplcitToken):
    name = "("


class ClosingParenthese(SimpleExplcitToken):
    name = ")"


class Number(Token, ValueNode):

    @classmethod
    def is_candidate(cls, symbols: str) -> bool:
        return all(map(lambda x: x in "0123456789", symbols))

    @classmethod
    def is_valid(cls, symbols: str) -> bool:
        return all(map(lambda x: x in "0123456789", symbols))

    def evaluate(self):
        return int(self.symbols)


class TreeBuilderError(Exception):
    pass

def handle_binary_operator(operator: Operator.__class__, token_stream: Sequence[Token], token_index: int) -> Sequence[Token]:
    if token_index == 0:
        raise TreeBuilderError("binary operator found at the beginning of stream")
    previous_element = token_stream[i-1]

    if isinstance(previous_element, OpeningParenthese):
        raise TreeBuilderError(f"opening parenthese found before operator at token {token_index}")

    if isinstance(previous_element, BinaryOperatorNode):
        raise TreeBuilderError(f"operator found before operator at token {token_index}")

    
    if isinstance(previous_element, Node):
        left = previous_element
    elif isinstance(previous_element, ValueNode):
        left = 

def build(token_stream: Sequence[Token], operators: Sequence[Operator.__class__]):
    for op in operators:
        
