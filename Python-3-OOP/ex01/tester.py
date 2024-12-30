from S1E7 import Baratheon, Lannister

# Subject exerpt concerning the tester
"""
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
print(
    f"Name : {Jaine.first_name, type(Jaine).__name__}, "
    f"Alive : {Jaine.is_alive}")
