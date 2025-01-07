# Subject
"""
Exercice 04: Calculate my dot product
Turn-in directory : ex04/
Files to turn in : ft_calculator.py
Allowed functions : None

Write a calculator class that is able to do calculations
(dot product, addition, subtraction) of 2 vectors.
Vector will always have identical sizes, no error handling.

It's up to you to find a decorator that can
help you to use the Methods of the calculator
class without instantiating this class.

The prototype of Class is:
class calculator:
#your code here
# decorator
def dotproduct(V1: list[float], V2: list[float]) -> None:
#your code here
# decorator
def add_vec(V1: list[float], V2: list[float]) -> None:
#your code here
# decorator
def sous_vec(V1: list[float], V2: list[float]) -> None:
#your code here
"""


class calculator:
    """
    Offers methods for doing vector operations
    (dot product, addition and substraction).
    Class full of static method, and no __init__
    Then no object of this class, and no capital letter.
    """

    @staticmethod
    def dotproduct(
        V1: list[float],
        V2: list[float]
    ) -> None:
        """Does the dot product of two vectors."""

        print(f"Dot product is: {sum(x * y for x, y in zip(V1, V2))}")

    @staticmethod
    def add_vec(
        V1: list[float],
        V2: list[float]
    ) -> None:
        """Does the sum of two vectors."""

        print(f"Add Vector is: {[float(x + y) for x, y in zip(V1, V2)]}")

    @staticmethod
    def sous_vec(
        V1: list[float],
        V2: list[float]
    ) -> None:
        """Does the substraction of two vectors."""

        print(f"Sous Vector is: {[float(x - y) for x, y in zip(V1, V2)]}")
