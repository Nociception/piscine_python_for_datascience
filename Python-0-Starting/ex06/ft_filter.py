# Subject
"""
Exercice 06:
Turn-in directory : ex06/
Files to turn in : ft_filter.py, filterstring.py
Allowed functions : sys or any other library that allows to receive the args

Part 1: Recode filter function
Recode your own ft_filter, it should behave like the original built-in function
(it should return the same thing as "print(filter.__doc__)"),
you should use list comprehensions to recode your ft_filter.
Of course using the original filter built-in is forbidden
"""


def ft_filter(predicate, iterable):
    """filter(function or None, iterable) --> filter object

Return an iterator yielding those items of iterable for which function(item)
is true. If function is None, return the items that are true."""
    if predicate is None:
        return (item for item in iterable if item)
    return (item for item in iterable if predicate(item))
