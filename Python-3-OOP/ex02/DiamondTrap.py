from S1E7 import Baratheon, Lannister

# You should read this
"""
This file contain a side commented "project",
just after the uncommented code.
Copy paste and uncomment the commented code you will
find after the @@@@@@@@@@@@@@@@@@@@@@ modern_properties.py @@@@@@@@@@@
comments bloc.

Another little tip: in this file, the attribute hairs has become hair.
"""

# Subject
"""
Exercice 02: Now it's weird!
Turn-in directory : ex02/
Files to turn in : Files from previous exercises + DiamondTrap.py
Allowed functions : None

In this exercise, you will create a monster: Joffrey Baratheon.
This is so risky!
There is something inconsistent with this new "false" king.
You must use the Properties to change the physical
characteristics of our new king.

The prototype of Class is:
from S1E7 import Baratheon, Lannister
class King(Baratheon, Lannister):
#your code here
"""


class King(Baratheon, Lannister):
    """
    King class, which inherits from Baratheon and Lannister classes.
    The idea is to test the diamond inheritance, in fact handled by Python
    thanks to C3 linearization (used since python 2.3).

    The tester allows to understand that the King is a Baratheon:
    Build a King class object without any more cutomization leads to
    to create a King object with specific attributes from the Baratheon class.
    """

    def __init__(
        self,
        first_name: str,
        is_alive=True
    ):
        """
        King constructor, which uses the Character constructor,
        and the Baratheon constructor (understood from the tester.py
        results).
        """

        super().__init__(first_name, is_alive)

    def get_eyes(self) -> str:
        """
        Getter for the eyes attributes.
        """

        return self.eyes

    def set_eyes(
        self,
        color: str
    ) -> None:
        """
        Setter for the eyes attributes.
        """

        if not isinstance(color, str):
            raise ValueError("color must be a string.")
        self.eyes = color

    def get_hair(self) -> str:
        """
        Getter for the hair attributes.
        """

        return self.hair

    def set_hair(
        self,
        color: str
    ) -> None:
        """
        Setter for the hair attributes.
        """

        if not isinstance(color, str):
            raise ValueError("color must be a string.")
        self.hair = color

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@ modern_properties.py @@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
