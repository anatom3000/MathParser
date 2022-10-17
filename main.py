from pprint import pprint

import parser
import tokens
from parser.tokens import Num, Add, Sub, Mul, Div, Pow, Mod, OpeningParenthese, ClosingParenthese, Name


def main():
    expr = input("> ")

    result = tokens.tokenize(expr, token_kinds=[
        Num,
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
    pprint(result)
    pprint(parser.parse(result))

if __name__ == '__main__':
    main()
