import pytest
from in_out import square, pow, outer


def test_square():
    """Test the square function."""
    assert square(3) == 9
    assert square(-3) == 9
    assert square(0) == 0
    assert square(1.5) == 2.25


def test_pow():
    """Test the pow function."""
    assert pow(2) == 4
    assert pow(3) == 27
    assert pow(1) == 1
    assert pow(0.5) == pytest.approx(0.7071067811865476)


def test_outer_with_square():
    """Test the outer function with the square function."""
    my_counter = outer(3, square)

    assert my_counter() == 9
    assert my_counter() == 81
    assert my_counter() == 6561


def test_outer_with_pow():
    """Test the outer function with the pow function."""
    another_counter = outer(1.5, pow)

    assert another_counter() == pytest.approx(1.8371173070873836)
    assert another_counter() == pytest.approx(3.056683336818703)
    assert another_counter() == pytest.approx(30.42684786675409)


def test_outer_with_different_start_values():
    """Test the outer function with different starting values."""
    counter1 = outer(2, square)
    counter2 = outer(4, square)

    assert counter1() == 4
    assert counter1() == 16

    assert counter2() == 16
    assert counter2() == 256


def test_outer_independence():
    """Ensure that multiple counters are independent."""
    counter1 = outer(2, square)
    counter2 = outer(3, square)

    assert counter1() == 4
    assert counter1() == 16

    assert counter2() == 9
    assert counter2() == 81
