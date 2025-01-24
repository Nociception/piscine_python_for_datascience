from abc import ABC, abstractmethod


class Character(ABC):
    """
    Abstract class Character, which inherits from ABC (abc module).
    Cannot be instantiated, because of the abstract die method.
    """

    def __init__(
        self,
        first_name: str,
        is_alive: bool = True
    ):
        """
        Character abstract class constructor.
        """

        if not isinstance(first_name, str):
            raise TypeError(
                f"Character Error:"
                f"first_name must be a str, not a {type(first_name)}."
            )
        if not isinstance(is_alive, bool):
            raise TypeError(
                f"Character Error:"
                f"is_alive must be a str, not a {type(first_name)}."
            )
        """
        By the way, simpler way to check parameters types:
        pip install typeguard
        import typeguard
        Write @typeguard.typechecked above the __init__ definition
        """

        self.first_name = first_name
        self.is_alive = is_alive

    @classmethod
    def get_class_attributes(cls):
        """DCOSTRING"""

        return {
            attr for attr in cls.__dict__.keys()
            if not attr.startswith("__")
        }

    @abstractmethod
    def die(self) -> None:
        """
        Abstract die method of the abstract class Character.
        Nothing implemented here.
        This system just makes inevitable to implement this method
        in any inherited class from this one (Chararter).
        """

        pass


class Stark(Character):
    """
    Stark class, inherited from the abstract class Character.
    Contains an inplemented die method, and then can be instantiated.
    """

    def die(self) -> None:
        """
        die method implemented.
        As the Stark class inherits from the abstract class Character
        (which contains the abstract method die), the Stark class
        must contain a well implemented die method,
        in order to be able to instantiate object of the Stark class.
        """

        if self.is_alive:
            self.is_alive = False
