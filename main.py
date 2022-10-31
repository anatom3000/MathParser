import parser
from symbolics import EvaluateError, Value


def main():
    expr = input("> ")

    # Rust at home:
    result = parser.parse(expr)
    if result is None:
        print("There is nothing in the expression!")
    else:
        try:
            print(f"{expr} = {result.evaluate()}")
        except EvaluateError:
            val = Value(float(input("x = ")))
            print(f"{expr}({val.value}) = {result.replace('x', val).evaluate()}")

if __name__ == '__main__':
    main()
