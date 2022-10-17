from collections.abc import Sequence

from . import tokens as tk
from symbolics import operators as op


class ParsingError(Exception):
    pass


OPERATORS = {
    tk.Pow: op.Pow,
    tk.Mul: op.Mul,
    tk.Div: op.Div,
    tk.Mod: op.Mod,
    tk.Add: op.Add,
    tk.Sub: op.Sub
}


def parse(token_stream: Sequence[tk.Token]):
    opening_parentheses_indexes = list(map(lambda x: x[0],
                                           filter(lambda x: isinstance(x[1], tk.OpeningParenthese),
                                                  enumerate(token_stream))))
    closing_parentheses_indexes = list(map(lambda x: x[0],
                                           filter(lambda x: isinstance(x[1], tk.ClosingParenthese),
                                                  enumerate(token_stream))))
    parentheses_levels = {}
    nesting_level = 0
    for p in opening_parentheses_indexes + closing_parentheses_indexes:
        if p in closing_parentheses_indexes:
            nesting_level -= 1

        parentheses_levels[p] = nesting_level

        if p in opening_parentheses_indexes:
            nesting_level += 1

    try:
        last_parenthese = max(parentheses_levels.keys())
    except ValueError:
        last_parenthese = None  # we dont need the variable since next for loop wont occure (parentheses_level empty)
    for index, level in parentheses_levels.items():
        if index in opening_parentheses_indexes and level == 0:
            closing_index = index + 1
            while parentheses_levels.get(closing_index, -1) != 0:
                closing_index += 1
                if closing_index > last_parenthese:
                    raise ParsingError(f"unmatched '(' at token {index}")
            token_stream[index:closing_index + 1] = [parse(token_stream[index + 1:closing_index])]

    for index, token in enumerate(token_stream):
        if isinstance(token, tk.Num):
            token_stream[index] = float(token.symbols)

    return token_stream
