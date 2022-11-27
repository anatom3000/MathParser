import human_math as hm


def main():
    # expr = input("Enter an expression: ")
    # pattern = input("Enter a pattern: ")

    result = hm.parser.parse("(2+1)/(7+4)")
    print(result)
    # pattern = hm.parser.parse(pattern)
    #
    # if result.matches(pattern):
    #     print("The pattern matches the expression!")
    # else:
    #     print("The pattern does not match the expression!")


if __name__ == '__main__':
    main()
