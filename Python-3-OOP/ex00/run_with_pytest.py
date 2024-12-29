import pytest
from S1E9 import Character, Stark


def test_default_values():
    jon = Stark("Jon")
    assert jon.is_alive is True


def test_die_method():
    arya = Stark("Arya")
    assert arya.is_alive is True

    arya.die()
    assert arya.is_alive is False

    
    arya.die()
    assert arya.is_alive is False


def test_abstract_class():
    with pytest.raises(TypeError) as excinfo:
        hodor = Character("Hodor")
        hodor.die()
    assert "Can't instantiate abstract class Character" in str(excinfo.value)


def test_invalid_subclass():
    class FakeCharacter(Character):
        pass

    with pytest.raises(TypeError) as excinfo:
        fake = FakeCharacter("Fake")
        fake.die()
    assert "Can't instantiate abstract class FakeCharacter" in str(excinfo.value)


def test_invalid_arguments():
    with pytest.raises(TypeError):
        invalid_stark = Stark(123)
        invalid_stark.die()

    with pytest.raises(TypeError):
        invalid_stark = Stark("Robb", "alive")  


def test_docstrings():
    ned = Stark("Ned")
    assert isinstance(ned.__doc__, str)
    assert isinstance(ned.__init__.__doc__, str)
    assert isinstance(ned.die.__doc__, str)


def test_inheritance():
    assert issubclass(Stark, Character)
    ned = Stark("Ned")
    assert isinstance(ned, Character)


def test_instance_attributes():
    robb = Stark("Robb", False)
    assert robb.first_name == "Robb"
    assert robb.is_alive is False


def test_multiple_instances():
    ned = Stark("Ned")
    arya = Stark("Arya", False)

    ned.die()
    assert ned.is_alive is False
    assert arya.is_alive is False  


def test_many_instances():
    starks = [Stark(f"Stark_{i}") for i in range(1000)]
    assert all(stark.is_alive for stark in starks)

if __name__ == "__main__":
    pytest.main()
