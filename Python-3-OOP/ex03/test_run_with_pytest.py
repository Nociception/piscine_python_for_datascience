import pytest
from ft_calculator import Calculator


def test_initialization():
    calc = Calculator([1, 2, 3])
    assert calc.vector == [1, 2, 3]

    with pytest.raises(TypeError):
        Calculator([1, "a", 3])


def test_addition():
    calc = Calculator([1, 2, 3])
    calc + 2
    assert calc.vector == [3, 4, 5]

    with pytest.raises(TypeError):
        calc + "string"


def test_subtraction():
    calc = Calculator([5, 10, 15])
    calc - 3
    assert calc.vector == [2, 7, 12]

    with pytest.raises(TypeError):
        calc - None


def test_multiplication():
    calc = Calculator([1, 2, 3])
    calc * 3
    assert calc.vector == [3, 6, 9]

    with pytest.raises(TypeError):
        calc * {}


def test_division():
    calc = Calculator([10, 20, 30])
    calc / 2
    assert calc.vector == [5, 10, 15]

    with pytest.raises(ZeroDivisionError):
        calc / 0

    with pytest.raises(TypeError):
        calc / []


def test_chained_operations():
    calc = Calculator([1, 2, 3])
    calc + 2
    calc * 3
    calc - 4
    calc / 2
    assert calc.vector == [2.5, 4, 5.5]


def test_string_representation():
    calc = Calculator([1, 2, 3])
    assert str(calc) == "[1, 2, 3]"


def test_edge_cases():
    calc = Calculator([])
    calc + 2
    assert calc.vector == []

    calc = Calculator([1e9, -1e9])
    calc * 2
    assert calc.vector == [2e9, -2e9]
