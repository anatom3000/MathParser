from nodes import NumericOperator, Expression
from tokenizer import SimpleExplcitToken, MultipleExplicitToken, Token


class Add(SimpleExplcitToken, NumericOperator):
    name = '+'

    def process(self, left, right):
        return left + right


class Sub(SimpleExplcitToken, NumericOperator):
    name = '-'

    def process(self, left, right):
        return left - right


class Mul(SimpleExplcitToken, NumericOperator):
    name = '*'

    def process(self, left, right):
        return left * right


class Div(SimpleExplcitToken, NumericOperator):
    name = '/'

    def process(self, left, right):
        return left / right


class Pow(MultipleExplicitToken, NumericOperator):
    names = ('**', '^')

    def process(self, left, right):
        return left ** right


class Mod(MultipleExplicitToken, NumericOperator):
    names = ("mod", "%")

    def process(self, left, right):
        return left % right


class OpeningParenthese(SimpleExplcitToken):
    name = "("


class ClosingParenthese(SimpleExplcitToken):
    name = ")"


class Number(Token, Expression):
    def evaluate(self):
        return float(self.symbols)

    @classmethod
    def is_candidate(cls, symbols: str) -> bool:
        return all(map(lambda x: x in "0123456789", symbols))

    @classmethod
    def is_valid(cls, symbols: str) -> bool:
        return all(map(lambda x: x in "0123456789", symbols))
