# Subject
"""
Exercice 00: Load my Dataset
Turn-in directory : ex00/
Files to turn in : load_csv.py
Allowed functions : pandas or any lib for data set manipulation

Make a function that takes a path as argument,
writes the dimensions of the data set and returns it.
You have to handle the error cases and return None if the path is bad,
bad format...

def load(path: str) -> Dataset: (You have to adapt the type
of return according to your library)
#your code here

Your script tester:
from load_csv import load
print(load("life_expectancy_years.csv"))
$> python tester.py
Loading dataset of dimensions (195, 302)
country 1800 1801 1802 1803 ... 2096 2097 2098 2099 2100
Afghanistan 28.2 28.2 28.2 28.2 ... 76.2 76.4 76.5 76.6 76.8
...
$>

You can display the Dataset in any format you like, the given format
is not restrictive.
"""

import pandas as pd
from pandas import DataFrame


def load(path: str) -> DataFrame | None:
    """
    Loads a CSV file, prints its dimensions,
    and returns its content as a DataFrame.

    Args:
        path (str): The file path to the CSV.

    Returns:
        DataFrame | None: The loaded dataset or None if an error occurred.
    """

    try:
        if not path.endswith(".csv"):
            raise ValueError("The file must be a CSV.")

        data = pd.read_csv(path)

        print(f"Loading dataset of dimensions {data.shape}")

        return data

    except FileNotFoundError:
        print(f"Error: File not found at path '{path}'.")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None
