from DiamondTrap import King

# Subject excerpt concerning the tester
"""
Your tester.py:
from DiamondTrap import King
Joffrey = King("Joffrey")
print(Joffrey.__dict__)
Joffrey.set_eyes("blue")
Joffrey.set_hairs("light")
print(Joffrey.get_eyes())
print(Joffrey.get_hairs())
print(Joffrey.__dict__)
Expected output: (docstrings can be different)
$> python tester.py
{
    'first_name': 'Joffrey',
    'is_alive': True,
    'family_name': 'Baratheon',
    'eyes': 'brown',
    'hair': 'dark'
}
blue
light
{
    'first_name': 'Joffrey',
    'is_alive': True,
    'family_name': 'Baratheon',
    'eyes': 'blue',
    'hairs': 'light'
}
$>
"""

Joffrey = King("Joffrey")
print(Joffrey.__dict__)
Joffrey.set_eyes("blue")
Joffrey.set_hair("light")
print(Joffrey.get_eyes())
print(Joffrey.get_hair())
print(Joffrey.__dict__)
