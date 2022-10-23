import parser
from symbolics import EvaluateError, Value


def main():
    expr = input("> ")

    # Rust at home:
    match parser.parse(expr):
        case None:
            print("There is nothing in the expression!")
        case result:
            try:
                print(f"{expr} = {result} = {result.evaluate()}")
            except EvaluateError:
                val = Value(float(input("x = ")))
                print(f"{result}({val.value}) = {result.replace('x', val)}")

if __name__ == '__main__':
    main()
