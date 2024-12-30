import pytest
from S1E7 import Baratheon, Lannister


def test_baratheon_initialization():
    robert = Baratheon("Robert")
    assert robert.first_name == "Robert"
    assert robert.is_alive is True
    assert robert.family_name == "Baratheon"
    assert robert.eyes == "brown"
    assert robert.hairs == "dark"


def test_lannister_initialization():
    cersei = Lannister("Cersei")
    assert cersei.first_name == "Cersei"
    assert cersei.is_alive is True
    assert cersei.family_name == "Lannister"
    assert cersei.eyes == "blue"
    assert cersei.hairs == "light"


def test_die_method():
    ned = Baratheon("Ned")
    ned.die()
    assert ned.is_alive is False


def test_repr_method():
    robert = Baratheon("Robert")
    expected_repr = "Vector: (Baratheon, brown, dark)"
    assert repr(robert) == expected_repr


def test_str_method():
    cersei = Lannister("Cersei")
    expected_str = "Vector: (Lannister, blue, light)"
    assert str(cersei) == expected_str


def test_chained_creation_and_die():
    jaime = Lannister.create_lannister("Jaine").die()
    assert jaime.first_name == "Jaine"
    assert jaime.is_alive is False
    assert jaime.family_name == "Lannister"


def test_invalid_character_initialization():
    with pytest.raises(TypeError):
        invalid_character = Baratheon(123)
        invalid_character.die()


def test_lannister_create_chaining():
    tyrion = Lannister.create_lannister("Tyrion", True).die()
    assert tyrion.first_name == "Tyrion"
    assert tyrion.is_alive is False
    assert tyrion.family_name == "Lannister"
