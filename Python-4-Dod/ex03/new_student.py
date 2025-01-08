# Subject
"""
Exercice 03: data class
Turn-in directory : ex03/
Files to turn in : new_student.py
Allowed functions : dataclasses, random, string

Write a dataclass that takes as arguments
a name and nickname, set active to True,
create the student login, and generate
a random ID with the generate_id function.
You must not use __str__ , __repr__ in your class.

The prototype of function and class is:
import random
import string
from dataclasses import dataclass, field
def generate_id() -> str:
return "".join(random.choices(string.ascii_lowercase, k = 15))
@dataclass
class Student:
#your code here
"""

import random
import string
from dataclasses import dataclass, field


def generate_id() -> str:
    """Generates a random ID with 15 lower letters"""

    return "".join(random.choices(string.ascii_lowercase, k=15))


@dataclass
class Student:
    """
    dataclass decorated class;
    This means that some things are autamically handled, such as:
        - __init__, based on the attributes' type annotation
        Therefore, Student(name = "Edward", surname = "agle") is possible.
        - __repr__ already prints properly all attributes
        - __eq__ allows to compare two instances of the same class,
        according to their attributes

    __post_init__ allows to run a customized logic after initialization.

    field allows to set:
    - if an attribute is definable or not by the user
    - a value handled with a specific function
    """

    name: str
    surname: str
    active: bool = True
    login: str = field(init=False)
    id: str = field(init=False, default_factory=generate_id)

    def __post_init__(self):
        """Magic dataclass method, run just after the initialization"""

        self.login = self.name[0] + self.surname
