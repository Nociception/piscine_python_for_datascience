import pytest
from modern_properties import King, Baratheon, Lannister


def test_king_initialization():
    """Test King initialization with default attributes."""
    joffrey = King("Joffrey")
    assert joffrey.first_name == "Joffrey"
    assert joffrey.is_alive is True
    assert joffrey.family_name == "Baratheon"
    assert joffrey.eyes == "brown"
    assert joffrey.hair == "dark"


def test_king_set_eyes():
    """Test the setter and getter for the eyes attribute."""
    joffrey = King("Joffrey")
    joffrey.eyes = "blue"
    assert joffrey.eyes == "blue"

    with pytest.raises(ValueError):
        joffrey.eyes = 123  # Invalid type


def test_king_set_hairs():
    """Test the setter and getter for the hair attribute."""
    joffrey = King("Joffrey")
    joffrey.hair = "light"
    assert joffrey.hair == "light"

    with pytest.raises(ValueError):
        joffrey.hair = None  # Invalid value


def test_king_die():
    """Test the die method for King."""
    joffrey = King("Joffrey")
    assert joffrey.is_alive is True
    joffrey.die()
    assert joffrey.is_alive is False


def test_king_inheritance():
    """Test the inheritance and attributes of the King."""
    joffrey = King("Joffrey")
    assert isinstance(joffrey, King)
    assert isinstance(joffrey, Baratheon)
    assert isinstance(joffrey, Lannister)


def test_chaining_setters():
    """Test method chaining using setters."""
    joffrey = King("Joffrey")
    joffrey.eyes = "blue"
    joffrey.hair = "light"
    assert joffrey.eyes == "blue"
    assert joffrey.hair == "light"
