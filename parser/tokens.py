from tokens import SimpleExplcitToken, MultipleExplicitToken, Token


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


class Num(Token):

    @classmethod
    def is_candidate(cls, symbols: str) -> bool:
        if symbols[0] in "+-":
            return False

        try:
            float(symbols + "0")
            return True
        except ValueError:
            return False

    @classmethod
    def is_valid(cls, symbols: str) -> bool:
        try:
            float(symbols)
            return True

        except ValueError:
            return False


class Name(Token):

    @classmethod
    def is_candidate(cls, symbols: str) -> bool:
        return symbols.isalnum() and symbols[0] not in "0123456789"

    @classmethod
    def is_valid(cls, symbols: str) -> bool:
        return symbols.isalnum() and symbols[0] not in "0123456789"
