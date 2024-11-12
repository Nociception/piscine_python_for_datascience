# Subject
"""
Allowed functions : None ; except maybe type, print, and our ?

Running your function alone does nothing.
Expected output:
$>python find_ft_type.py | cat -e
$>

Probably the author meant "Running your FILE alone does nothing."
Because the function has definetly something to do :
"Write a function that prints the object types and returns 42."
"""


def all_thing_is_obj(object: any) -> int:
    """DOCSTRING"""
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
