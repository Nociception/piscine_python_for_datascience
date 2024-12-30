from S1E7 import Baratheon, Lannister


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

    @property
    def eyes(self) -> str:
        """
        Getter for the eyes attributes, using the @property decorator.
        Convention: this decorator @property is used to define a getter.
        """

        return self._eyes

    @eyes.setter
    def eyes(
        self,
        color: str
    ) -> None:
        """
        Setter for the eyes attributes, using the attribute connected
        setter decorator.

        Notice that the last two method have the same name
        (but not the same arguments, and not the same decorator of course).
        """

        if not isinstance(color, str):
            raise ValueError("color must be a string.")
        self._eyes = color

    @property
    def hair(self) -> str:
        """
        Getter for the hair attributes, using the @property decorator.
        """

        return self._hair

    @hair.setter
    def hair(
        self,
        color: str
    ) -> None:
        """
        Setter for the hair attributes, using the attribute connected
        setter decorator.
        """

        if not isinstance(color, str):
            raise ValueError("color must be a string.")
        self._hair = color
