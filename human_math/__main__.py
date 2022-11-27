import human_math as hm


def main() -> None:
    expression_string = input("Enter an expression: ")
    pattern_string = input("Enter a pattern: ")

    expression = hm.parser.parse(expression_string)
    pattern = hm.parser.parse(pattern_string)

    if expression.matches(pattern):
        print("The pattern matches the expression!")
    else:
        print("The pattern does not match the expression!")


if __name__ == '__main__':
    main()
