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

Your tester.py:
from S1E7 import Baratheon, Lannister
Robert = Baratheon("Robert")
print(Robert.__dict__)
print(Robert.__str__)
print(Robert.__repr__)
print(Robert.is_alive)
Robert.die()
print(Robert.is_alive)
print(Robert.__doc__)
print("---")
Cersei = Lannister("Cersei")
print(Cersei.__dict__)
print(Cersei.__str__)
print(Cersei.is_alive)
print("---")
Jaine = Lannister.create_lannister("Jaine", True)
print(f"Name:{Jaine.first_name, type(Jaine).__name__}, Alive:{Jaine.is_alive}")

Expected output: (docstrings can be different)
$> python tester.py
{
    'first_name': 'Robert',
    'is_alive': True,
    'family_name': 'Baratheon',
    'eyes': 'brown',
    'hairs': 'dark'
}
<bound method Baratheon.__str__ of Vector: ('Baratheon', 'brown', 'dark')>
<bound method Baratheon.__repr__ of Vector: ('Baratheon', 'brown', 'dark')>
True
False
Representing the Baratheon family.
---
{
    'first_name': 'Cersei',
    'is_alive': True,
    'family_name': 'Lannister',
    'eyes': 'blue',
    'hairs': 'light'
}
<bound method Lannister.__str__ of Vector: ('Lannister', 'blue', 'light')>
True
---
Name : ('Jaine', 'Lannister'), Alive : True
$>
"""


class Dummy_Character(Character):
    """DO NOT USE, except for get_class_specific_attributes"""

    def die():
        pass

def get_class_specific_attributes(
    obj: object,
    parent_obj: object
) -> dict[str, Any]:

    instance_attributes = obj.__dict__.keys()
    
    parent_class_attributes = parent_obj.__dict__.keys()

    specific_attributes = set(instance_attributes) - set(parent_class_attributes)
    
    # print(f"instance_attributes : {instance_attributes}")
    # print(f"parent_class_attributes : {parent_class_attributes}")
    # print(f"specific_attributes : {specific_attributes}")
    # print()

    return {
        attr: getattr(obj, attr)
        for attr in specific_attributes
    }




class Baratheon(Character):
    """DOCSTRING"""

    def __init__(
        self,
        first_name: str,
        is_alive = True
    ):
        """DOCSTRING"""

        super().__init__(
            first_name,
            is_alive
        )
        self.family_name = "Baratheon"
        self.eyes = "brown"
        self.hairs = "dark"

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

        
    def __repr__(self):
        """
        __repr__ Bratheon overload of the native __repr__ class method.
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
        return f"Vector: ({', '.join(str(v) for v in sorted(spec_attrs.values()))})"


    def __str__(self) -> str:
        """
        __str__ Bratheon overload of the native __str__ class method.
        This method is called if the code contains such instructions:
        - str(obj)
        - print(obj)
        (With obj as a custom class object
        (for instance here, a Baratheon class object))
        """
        return self.__repr__()

    # DEF CHAIN CHARACTER_CREATION
