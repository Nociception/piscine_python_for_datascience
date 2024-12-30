import pytest
from DiamondTrap import King


def test_initialization():
    """
    Test initialization of the King class.
    """
    joffrey = King("Joffrey")
    assert joffrey.first_name == "Joffrey"
    assert joffrey.is_alive is True
    assert joffrey.family_name == "Baratheon"
    assert joffrey.eyes == "brown"
    assert joffrey.hair == "dark"


def test_set_and_get_eyes():
    """
    Test setting and getting the eyes attribute.
    """
    joffrey = King("Joffrey")
    joffrey.set_eyes("blue")
    assert joffrey.get_eyes() == "blue"


def test_set_and_get_hair():
    """
    Test setting and getting the hair attribute.
    """
    joffrey = King("Joffrey")
    joffrey.set_hair("light")
    assert joffrey.get_hair() == "light"


def test_invalid_set_eyes():
    """
    Test that setting eyes to an invalid value raises an error.
    """
    joffrey = King("Joffrey")
    with pytest.raises(ValueError):
        joffrey.set_eyes(123)


def test_invalid_set_hair():
    """
    Test that setting hair to an invalid value raises an error.
    """
    joffrey = King("Joffrey")
    with pytest.raises(ValueError):
        joffrey.set_hair(123)


def test_modification_effect_on_dict():
    """
    Test that modifications to eyes and hair are reflected in __dict__.
    """
    joffrey = King("Joffrey")
    joffrey.set_eyes("blue")
    joffrey.set_hair("light")
    assert joffrey.__dict__["eyes"] == "blue"
    assert joffrey.__dict__["hair"] == "light"


def test_is_alive_property():
    """
    Test the is_alive property functionality.
    """
    joffrey = King("Joffrey")
    assert joffrey.is_alive is True
    joffrey.die()
    assert joffrey.is_alive is False


def test_multiple_instances():
    """
    Test that multiple instances of King do not interfere with each other.
    """
    joffrey = King("Joffrey")
    tommen = King("Tommen")
    joffrey.set_eyes("blue")
    tommen.set_eyes("green")
    assert joffrey.get_eyes() == "blue"
    assert tommen.get_eyes() == "green"
    assert joffrey.first_name == "Joffrey"
    assert tommen.first_name == "Tommen"
