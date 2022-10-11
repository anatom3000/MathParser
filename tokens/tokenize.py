from collections.abc import Sequence

from .token import Token, Unknown

TokenKinds = Sequence[Token.__class__]


class ParsingError(Exception):
    pass


def first_token(expression: str, token_kinds: TokenKinds) -> Token:
    last_char = 1
    previous_candidates = None
    candidates = [kind for kind in token_kinds if kind.is_candidate(expression[:last_char])]  # you can't get the length of a filter object :/

    while True:
        # print(f"\nCandidates for <{expression[:last_char]}>: {candidates}")
        if len(candidates) == 0:
            if last_char > 1:
                previous_part = expression[:last_char-1]

                valid_kinds = [kind for kind in previous_candidates if kind.is_valid(previous_part)]

                kind_number = len(valid_kinds)
                if kind_number == 0:
                    return Unknown(previous_part)
                elif kind_number == 1:
                    return valid_kinds[0](previous_part)
                else:
                    raise ParsingError(f"too many candidates {valid_kinds} for \"{previous_part}\"")

            else:
                return Unknown(expression[:last_char])

        elif len(candidates) == 1:
            candidate = candidates[0]

            while candidate.is_candidate(expression[:last_char+1]):
                if last_char > len(expression):
                    break

                last_char += 1

            if candidate.is_valid(expression[:last_char]):
                return candidate(expression[:last_char])
            else:
                return Unknown(expression[:last_char])

        else:
            last_char += 1
            previous_candidates = candidates[:]
            candidates = [kind for kind in token_kinds if kind.is_candidate(expression[:last_char])]


def tokenize(expression: str, token_kinds: TokenKinds, *, raise_on_unknown=True, ignore_whitespaces=True) -> Sequence[Token]:
    if ignore_whitespaces:
        expression = ''.join(expression.split())

    tokens = []
    while len(expression) != 0:
        token = first_token(expression, token_kinds)

        is_unknown = isinstance(token, Unknown)

        if raise_on_unknown and is_unknown:
            raise ParsingError(f"invalid expression \"{token.symbols}\" ")

        if len(tokens) != 0 and is_unknown and isinstance(tokens[-1], Unknown):
            tokens[-1] = Unknown(tokens[-1].symbols + token.symbols)
        else:
            tokens.append(token)

        expression = expression[len(token.symbols):]

    return tokens
