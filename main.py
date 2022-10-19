import parser


def main():
    expr = input("> ")

    # Rust at home:
    match parser.parse(expr):
        case None:
            print("There is nothing in the expression!")
        case result:
            print(f"{result} = {result.evaluate()}")


if __name__ == '__main__':
    main()
