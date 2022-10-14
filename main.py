from pprint import pprint

import tokenizer
from tokens import Number, Add, Sub, Mul, Div, Pow, Mod, OpeningParenthese, ClosingParenthese, Name


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
        ClosingParenthese,
        Name,
    ], raise_on_unknown=False)

    pprint(result, underscore_numbers=True)

if __name__ == '__main__':
    main()
