from tokenizer import SimpleExplcitToken, MultipleExplicitToken, Token


class Add(SimpleExplcitToken):
    name = '+'


class Sub(SimpleExplcitToken):
    name = '-'


class Mul(SimpleExplcitToken):
    name = '*'


class Div(SimpleExplcitToken):
    name = '/'


class Pow(MultipleExplicitToken):
    names = ('**', '^')


class Mod(MultipleExplicitToken):
    names = ("mod", "%")


class OpeningParenthese(SimpleExplcitToken):
    name = "("


class ClosingParenthese(SimpleExplcitToken):
    name = ")"


class Number(Token):

    @classmethod
    def is_candidate(cls, symbols: str) -> bool:
        return all(map(lambda x: x in "0123456789", symbols))

    @classmethod
    def is_valid(cls, symbols: str) -> bool:
        return all(map(lambda x: x in "0123456789", symbols))
