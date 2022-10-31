import sys

import parser
from symbolics import EvaluateError, Value


def main():
    expr = input("> ")

    result = parser.parse(expr)
    if result is None:
        print("There is nothing in the expression!")
    else:
        try:
            print(f"{expr} = {result.evaluate()}")
        except EvaluateError:
            try:
                val = Value(float(input("x = ")))
            except ValueError:
                print("Wrong value! Quitting...")
                sys.exit(1)
            print(f"{expr}({val.value}) = {result.replace('x', val).evaluate()}")

if __name__ == '__main__':
    main()