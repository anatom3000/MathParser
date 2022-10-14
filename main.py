from pprint import pprint


import tokens
from parser import Number, Add, Sub, Mul, Div, Pow, Mod, OpeningParenthese, ClosingParenthese, Name


def main():
    expr = input("> ")

    result = tokens.tokenize(expr, token_kinds=[
        Number,
        Add,
        Sub,
        Mul,
        Div,
        Pow,
        Mod,
        OpeningParenthese,
        ClosingParenthese,
        Name,
    ], raise_on_unknown=False)

    pprint(result, underscore_numbers=True)

if __name__ == '__main__':
    main()
