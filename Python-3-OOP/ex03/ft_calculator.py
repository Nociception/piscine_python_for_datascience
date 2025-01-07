# Subject
"""
Exercice 03: Calculate my vector
Turn-in directory : ex03/
Files to turn in : ft_calculator.py
Allowed functions : None
Write a calculator class that is able to do calculations
(addition, multiplication, subtraction, division) of vector with a scalar.
The prototype of Class is:
class calculator:
#your code here
def __add__(self, object) -> None:
#your code here
def __mul__(self, object) -> None:
#your code here
def __sub__(self, object) -> None:
#your code here
def __truediv__(self, object) -> None:
#your code here
"""


class Calculator:
    """
    Stores a vector,
    and implements operator overloads for applying them on the vector.
    """

    def __init__(
        self,
        vector: list[int | float]
    ):
        if not all(isinstance(elt, (int, float)) for elt in vector):
            raise TypeError(
                "All elements in the vector must be int of float."
            )
        self.vector = vector

    def __str__(self):
        """String representation for the vector."""

        return str(self.vector)

    def check_type(
        self,
        object
    ) -> bool:
        """Centralized method for type checking."""

        return isinstance(object, (int, float))

    def __add__(
        self,
        object
    ) -> None:
        """Add operator overload"""

        if self.check_type(object):
            self.vector = [x + object for x in self.vector]
            print(self.vector)
        else:
            raise TypeError(
                "Operand must be int or float."
            )

    def __mul__(
        self,
        object
    ) -> None:
        """Multiplication operator overload"""

        if self.check_type(object):
            self.vector = [x * object for x in self.vector]
            print(self.vector)
        else:
            raise TypeError(
                "Operand must be int or float."
            )

    def __sub__(
        self,
        object
    ) -> None:
        """Substraction operator overload"""

        if self.check_type(object):
            self.vector = [x - object for x in self.vector]
            print(self.vector)
        else:
            raise TypeError(
                "Operand must be int or float."
            )

    def __truediv__(
        self,
        object
    ) -> None:
        """Division operator (/) overload"""

        if self.check_type(object):
            if object == 0:
                raise ZeroDivisionError(
                    "Cannot divide by 0."
                )
            self.vector = [x / object for x in self.vector]
            print(self.vector)
        else:
            raise TypeError(
                "Operand must be int or float."
            )
