from statistics import ft_statistics
from io import StringIO
import sys


def capture_output(func, *args, **kwargs):
    """Capture la sortie standard d'une fonction"""
    captured_output = StringIO()
    sys.stdout = captured_output
    func(*args, **kwargs)
    sys.stdout = sys.__stdout__
    return captured_output.getvalue().strip()


def test_mean():
    output = capture_output(ft_statistics, 1, 2, 3, 4, toto="mean")
    assert output == "mean : 2.5"


def test_median():
    output = capture_output(ft_statistics, 1, 3, 2, 4, tutu="median")
    assert output == "median : 2.5"

    output = capture_output(ft_statistics, 1, 2, 3, tutu="median")
    assert output == "median : 2"


def test_quartile():
    output = capture_output(ft_statistics, 1, 2, 3, 4, 5, tata="quartile")
    assert output == "quartile : [2.0, 4.0]"


def test_std():
    output = capture_output(ft_statistics, 1, 2, 3, hello="std")
    assert output == "std : 0.816496580927726"


def test_variance():
    output = capture_output(ft_statistics, 1, 2, 3, world="var")
    assert output == "var : 0.6666666666666666"


def test_multiple_statistics():
    output = capture_output(ft_statistics, 1, 2, 3, toto="mean", tutu="median")
    assert "mean : 2.0" in output
    assert "median : 2" in output


def test_empty_data():
    output = capture_output(ft_statistics, toto="mean")
    assert output == "ERROR"


def test_non_numeric_data():
    output = capture_output(ft_statistics, 1, "a", 3, toto="mean")
    assert output == "ERROR"


def test_large_data():
    data = list(range(1, 1001))
    output = capture_output(ft_statistics, *data, toto="mean")
    assert output == "mean : 500.5"
