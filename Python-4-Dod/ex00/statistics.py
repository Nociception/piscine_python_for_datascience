from typing import Any

# Subject
"""
Exercice 00: Calculate my statistics
Turn-in directory : ex00/
Files to turn in : statistics.py
Allowed functions : None

You must take in *args a quantity of unknown number and make
the Mean, Median, Quartile (25% and 75%), Standard Deviation and Variance
according to the **kwargs ask.
You have to manage the errors.

The prototype of function is:
def ft_statistics(*args: Any, **kwargs: Any) -> None:
#your code here
"""


def ft_statistics(
    *args: Any,
    **kwargs: Any
) -> None:
    """
    Accepts a various number of int/float as positional arguments (stored
    into a `data` variable),
    and a various number of str known arguments for asking to
    calculate statistics indicators such as :
    mean, median, quartile, standard deviation and variance.
    """

    error_text = "ERROR"

    if not all(isinstance(x, (int, float)) for x in args):
        print(error_text)
        return

    def mean(data) -> float | str:
        """Calculates the mean of the `data` variable."""

        return sum(data) / len(data)

    def median(data):
        """Calculates the median of the `data` variable."""

        n = len(data)
        if n % 2 == 1:
            return data[n // 2]
        return (data[n // 2 - 1] + data[n // 2]) / 2

    def quartile(data):
        """Calculates the quartiles of the `data` variable."""

        q25 = float(data[len(data) // 4])
        q75 = float(data[3 * len(data) // 4])
        return [q25, q75]

    def std(data):
        """Calculates the standard deviation of the `data` variable."""

        return var(data) ** 0.5

    def var(data):
        """Calculates the variance of the `data` variable."""

        m = mean(data)
        return sum((x - m) ** 2 for x in data) / len(data)

    data = sorted(args)
    stat_calc = {
        "mean": mean,
        "median": median,
        "quartile": quartile,
        "std": std,
        "var": var,
    }
    results = list()

    for calc, func in stat_calc.items():
        if calc in kwargs.values():
            if len(data) > 0:
                results.append(f"{calc} : {func(data)}")
            else:
                results.append(error_text)

    for result in results:
        print(result)
