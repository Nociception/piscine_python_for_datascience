# Subject
"""
Exercice 02: First function python
Turn-in directory : ex02/
Files to turn in : find_ft_type.py
Allowed functions : None

Running your function alone does nothing.
Expected output:
$>python find_ft_type.py | cat -e
$>

Probably the author meant "Running your FILE alone does nothing."
Because the function has definetly something to do :
"Write a function that prints the object types and returns 42."

Your tester.py:
from find_ft_type import all_thing_is_obj
ft_list = ["Hello", "tata!"]
ft_tuple = ("Hello", "toto!")
ft_set = {"Hello", "tutu!"}
ft_dict = {"Hello" : "titi!"}
all_thing_is_obj(ft_list)
all_thing_is_obj(ft_tuple)
all_thing_is_obj(ft_set)
all_thing_is_obj(ft_dict)
all_thing_is_obj("Brian")
all_thing_is_obj("Toto")
print(all_thing_is_obj(10))

Expected output:
$>python tester.py | cat -e
List : <class 'list'>$
Tuple : <class 'tuple'>$
Set : <class 'set'>$
Dict : <class 'dict'>$
Brian is in the kitchen : <class 'str'>$
Toto is in the kitchen : <class 'str'>$
Type not found$
42$
$>
$>python find_ft_type.py | cat -e
$>
"""


def all_thing_is_obj(object: any) -> int:
    """Receives an arg (object) of any type.
    If object's type is one of the following:
        list, tuple, set, dict, str
    Prints the object's type, "Type not found" otherwise.
    Returns 42 anyway.

    Usage:
    >>> all_thing_is_obj(["elt1", "elt2"])
    List : <class 'list'>
    42"""

    types = {list: "List",
             tuple: "Tuple",
             set: "Set",
             dict: "Dict",
             str: "is in the kitchen"}

    type_object = type(object)
    if type_object in types:
        if type_object == str:
            print(f"{object} ", end="")
        print(f"{types[type_object]} : {type_object}")
    else:
        print("Type not found")

    return 42
