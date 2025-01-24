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

import matplotlib.pyplot as plt
from load_csv import load
import numpy as np


def main() -> None:
    """
    Plots the life expectancy of a specific country over the years.

    Args:
        data (pd.DataFrame): The dataset containing life expectancy data.
        country (str): The name of the country to plot.

    Returns:
        None
    """

    DEBUG = 0

    DATASET_PATH = "life_expectancy_years.csv"
    data = load(DATASET_PATH)
    country = "France"

    if DEBUG:
        print("\n### DEBUG ###\n"
              "function: main from aff_life.py\n"
              "data:\n"
              f"{data}"
              f"\ncountry: {country}"
              "\n### DEBUG END###\n")

    def parsing_reindex(data, country) -> np.ndarray:
        """
        Validates and preprocesses the DataFrame for life expectancy data.

        This function ensures that the input DataFrame
        contains the necessary 'country' column and verifies
        that the specified country exists in the dataset.
        It then sets the 'country' column as the index
        for easier data manipulation.

        Args:
            data (pd.DataFrame):
                The input DataFrame containing life expectancy data.
            country (str):
            The name of the country to validate and extract data for.

        Returns:
            pd.DataFrame:
            The updated DataFrame with 'country' set as the index.

        Raises:
            AssertionError:
            If the 'country' column is missing from the DataFrame,
            or if the specified country is not in the dataset index.
        """

        assert data is not None, "Data is None."

        assert 'country' in data.columns, (
            "'country' is not a column of the dataframe."
        )
        data.set_index('country', inplace=True)

        assert country in data.index, (
            f"{country} not in the dataframe."
        )

        return data

    try:
        data = parsing_reindex(data, country)
        country_data = data.loc[country]
        years = country_data.index.astype(int)
        values = country_data.values.astype(float)

        plt.figure(figsize=(10, 6))
        plt.plot(years, values, label=country, color='blue', linewidth=2)
        plt.title(f"{country} Life expectancy Projections", fontsize=14)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Life expectancy", fontsize=12)
        plt.legend(loc="upper left", fontsize=10)
        plt.show()

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
    finally:
        return None
