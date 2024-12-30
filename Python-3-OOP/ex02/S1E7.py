from S1E9 import Character
from typing import Any

# SUBJECT
"""
Create two families that inherit from the Character class,
that we can instantiate without going through the Character class.

Find a solution so that "__str__" and "__repr__"
return strings and not objects.

Write a Class method to create characters in a chain.

The prototype of Class is:
from S1E9 import Character
class Baratheon(Character):
#your code here
class Lannister(Character):
#your code here
# decorator
def create_lannister(your code here):
#your code here
"""


class Dummy_Character(Character):
    """
    DO NOT USE, except for get_class_specific_attributes.
    Create an instance of this class only for getting a list of
    Character attributes.
    """

    def die():
        pass


def get_class_specific_attributes(
    child_obj: object,
    parent_obj: object
) -> dict[str, Any]:
    """
    Filters attributes of a class which inherits from another class:

    Returns a dictionnary of attributes and its value for each.
    Only the specific attributes of the child_obj class are in this dict.
    """

    instance_attr = child_obj.__dict__.keys()
    parent_class_attr = parent_obj.__dict__.keys()
    specific_attr = set(instance_attr) - set(parent_class_attr)

    return {
        attr: getattr(child_obj, attr)
        for attr in specific_attr
    }


class Baratheon(Character):
    """
    Baratheon class, which inherits from the Character class.

    Comparison with the Character class ; Baratheon has:
    - three specific unchangeable attributes
    - __str__ and __repr__ are overloaded in order to return str
    - an implemented die method, which returns self
    - a classmethod create_baratheon in order to be able to create
    characters in a chain methods calling.
    """

    def __init__(
        self,
        first_name: str,
        is_alive=True
    ):
        """
        Baratheon constructor.
        Uses the Character constructor to handle first_name and is_alive.
        Sets three specific Baratheon class attributes with unchangeable
        values (they are then not parameters for the constructor):
        self.family_name = "Baratheon"
        self.eyes = "brown"
        self.hair = "dark"
        """

        super().__init__(
            first_name,
            is_alive
        )
        self.family_name = "Baratheon"
        self.eyes = "brown"
        self.hair = "dark"

    def die(self):
        """
        die method implemented.
        As the Baratheon class inherits from the abstract class Character
        (which contains the abstract method die), the Baratheon class
        must contain a well implemented die method,
        in order to be able to instantiate object of the Baratheon class.
        """

        if self.is_alive:
            self.is_alive = False
        return self

    def __repr__(self):
        """
        __repr__ Baratheon overload of the native __repr__ class method.
        This method is called if the code contains such instructions:
        - repr(obj)
        - obj
        (With obj as a custom class object
        (for instance here, a Baratheon class object))
        """

        spec_attrs = get_class_specific_attributes(
            self,
            Dummy_Character("Dummy")
        )
        return (
            f"Vector: "
            f"({', '.join(str(v) for v in sorted(spec_attrs.values()))})"
        )

    def __str__(self) -> str:
        """
        __str__ Baratheon overload of the native __str__ class method.
        This method is called if the code contains such instructions:
        - str(obj)
        - print(obj)
        (With obj as a custom class object
        (for instance here, a Baratheon class object))
        """

        return self.__repr__()

    @classmethod
    def create_baratheon(
        self,
        first_name: str,
        is_alive: bool = True
    ):
        """
        Classmethod which creates a Baratheon class object,
        usable in a chain such as:
        B = Baratheon.create_baratheon('B').die()

        As die returns self, die also fits in a chain methods calling.
        """

        return Baratheon(first_name, is_alive)


class Lannister(Character):
    """
    Lannister class, which inherits from the Character class.

    Comparison with the Character class ; Lannister has:
    - three specific unchangeable attributes
    - __str__ and __repr__ are overloaded in order to return str
    - an implemented die method, which returns self
    - a classmethod create_lannister in order to be able to create
    characters in a chain methods calling.
    """

    def __init__(
        self,
        first_name: str,
        is_alive=True
    ):
        """
        Lannister constructor.
        Uses the Character constructor to handle first_name and is_alive.
        Sets three specific Lannister class attributes with unchangeable
        values (they are then not parameters for the constructor):
        self.family_name = "Lannister"
        self.eyes = "blue"
        self.hair = "light"
        """

        super().__init__(
            first_name,
            is_alive
        )
        self.family_name = "Lannister"
        self.eyes = "blue"
        self.hair = "light"

    def die(self):
        """
        die method implemented.
        As the Lannister class inherits from the abstract class Character
        (which contains the abstract method die), the Lannister class
        must contain a well implemented die method,
        in order to be able to instantiate object of the Lannister class.
        """

        if self.is_alive:
            self.is_alive = False
        return self

    def __repr__(self):
        """
        __repr__ Lannister overload of the native __repr__ class method.
        This method is called if the code contains such instructions:
        - repr(obj)
        - obj
        (With obj as a custom class object
        (for instance here, a Lannister class object))
        """

        spec_attrs = get_class_specific_attributes(
            self,
            Dummy_Character("Dummy")
        )
        return (
            f"Vector: "
            f"({', '.join(str(v) for v in sorted(spec_attrs.values()))})"
        )

    def __str__(self) -> str:
        """
        __str__ Bratheon overload of the native __str__ class method.
        This method is called if the code contains such instructions:
        - str(obj)
        - print(obj)
        (With obj as a custom class object
        (for instance here, a Lannister class object))
        """

        return self.__repr__()

    @classmethod
    def create_lannister(
        self,
        first_name: str,
        is_alive: bool = True
    ):
        """
        Classmethod which creates a Lannister class object,
        usable in a chain such as:
        B = Lannister.create_lannister('B').die()

        As die returns self, die also fits in a chain methods calling.
        """

        return Lannister(first_name, is_alive)
