# human_math
A mathematical expression parser

### Example usage
```python
>>> import human_math as hm                     # import module
>>> tree = hm.parse("2 - (-sin(3pi/2)) - 3.0")  # parse string (user input, etc.)
>>> tree
((2 - (-1 * sin(3 * (pi / 2)))) - 3)            # console representation uses parentheses everywhere to be strictly non-ambigious
>>> tree.evaluate()                             # evaluate the expression tree
-2                                              # nb: sin(3pi/2) = -1 so 2 - (-1) - 3 = -2
```