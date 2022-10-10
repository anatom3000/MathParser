from pprint import pprint

from tokenizer import parser, SimpleExplcitToken, MultipleExplicitToken, Token
import tokenizer
from tokens import Number, Add, Sub, Mul, Div, Pow, Mod, OpeningParenthese, ClosingParenthese


def main():
    expr = input("> ")

    result = tokenizer.parse(expr, token_kinds=[
        Number,
        Add,
        Sub,
        Mul,
        Div,
        Pow,
        Mod,
        OpeningParenthese,
        ClosingParenthese
    ], raise_on_unknown=False)

    pprint(result, underscore_numbers=True)

if __name__ == '__main__':
    main()
