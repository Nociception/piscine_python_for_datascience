# SUBJECT
"""
Exercice 00: GOT S1E9
Turn-in directory : ex00/
Files to turn in : S1E9.py
Allowed functions : None

Create an abstract class "character"
which can take a first_name as first parameter,
is_alive as second non mandatory parameter set
to True by default and can change the health state
of the character with a method that passes is_alive from True to False.

And a "stark" class which inherits from Character

The prototype of Class is:
from abc import ABC, abstractmethod
class Character(ABC):
\"""Your docstring for Class""\"
@abstractmethod
#your code here

class Stark(Character):
\"""Your docstring for Class""\"
#your code here

Your tester.py:
from S1E9 import Character, Stark
Ned = Stark("Ned")
print(Ned.__dict__)
print(Ned.is_alive)
Ned.die()
print(Ned.is_alive)
print(Ned.__doc__)
print(Ned.__init__.__doc__)
print(Ned.die.__doc__)
print("---")
Lyanna = Stark("Lyanna", False)
print(Lyanna.__dict__)

Expected output: (docstrings can be different)
$> python tester.py
{'first_name': 'Ned', 'is_alive': True}
True
False
Your docstring for Class
Your docstring for Constructor
Your docstring for Method
---
{'first_name': 'Lyanna', 'is_alive': False}
$>
Make sure you have used an abstract class,
the code below should make an error.
from S1E9 import Character
hodor = Character("hodor")
TypeError: Can't instantiate abstract class Character with abstract method
$>
"""

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
