# Subject
"""
Exercice 02: compare my country
Turn-in directory : ex02/
Files to turn in : load_csv.py, aff_pop.py
Allowed functions : matplotlib, seaborn or any lib for Data Visualization

Create a program that calls the load function from the first exercise,
loads the file population_total.csv,
and displays the country information of your campus versus other
country of your choice.
Your graph must have a title,
a legend for each axis and a legend for each graph.
You must display the years from 1800 to 2050.

For example, for the 42 campuses in France we will have this result:
See the expected.jpg file to compare with my result.
"""

from load_csv import load
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def main() -> None:
    """
    Compare the population of two countries over the years.

    Args:
        data (pd.DataFrame): The dataset containing population data.
        country1 (str): The name of the first country to compare.
        country2 (str): The name of the second country to compare.

    Returns:
        None
    """

    DEBUG = 0
    NOTES = 0
    PRINT_NOTES = 1

    DATASET_PATH = "population_total.csv"
    data = load(DATASET_PATH)

    START = 1800
    END = 2050

    COUNTRIES = ["France",
                 "Belgium",
                 # "Japan",
                 # "type_another_existing_country",
                 # "non_existing_country",
                 ]
    COLORS = ["green",
              "blue",
              "red",
              "orange",
              "yellow"]

    if DEBUG:
        print("\n### DEBUG ###\n"
              "function: main from aff_pop.py\n"
              "data:\n"
              f"{data}"
              f"\nSTART: {START} ; END: {END}"
              f"\nCOUNTRIES:\n{COUNTRIES};  len(COUNTRIES): {len(COUNTRIES)}"
              f"\nCOLORS:\n{COLORS}; len(COLORS): {len(COLORS)}"
              "Reminder : len(COLORS) must be >= len(COUNTRIES)."
              "\n### DEBUG END###\n")

    def parsing_reindex_df(data) -> np.ndarray:
        """
        Validates the input dataset, reindexes it by the 'country' column,
        and ensures the specified countries and years are present.

        Args:
            data (pd.DataFrame): The dataset to process.

        Returns:
            pd.DataFrame: The reindexed dataset with 'country' as the index.

        Raises:
            AssertionError: If any of the following conditions are not met:
                - The 'country' column is missing.
                - The `START` year is not a column in the dataset.
                - The `END` year is not a column in the dataset.
                - Any of the countries in `COUNTRIES`
                are not present in the dataset.

        Notes:
            - The dataset is modified in place due to `inplace=True`
            in the `set_index` method.
        """

        assert 'country' in data.columns, (
            "'country' is not a column of the dataframe."
        )
        data.set_index('country', inplace=True)

        assert str(START) in data.columns, (
            f"{START} is not in the dataframe."
        )
        assert str(END) in data.columns, (
            f"{END} is not in the dataframe."
        )

        missing_countries = [country for country in COUNTRIES
                             if country not in data.index]
        assert not missing_countries, (
                f"These countries are missing in the dataset:\n"
                f"{', '.join(missing_countries)}"
        )

        return data

    def parsing_value(value: str) -> int:
        """
        Parses a human-readable string representing a
        large number (e.g., "5k", "3M", "2B") into an integer value.

        Args:
            value (str): The human-readable string to parse.

        Returns:
            int: The parsed integer value.
            Returns -1 if an error occurs or the input is invalid.

        Raises:
            AssertionError: If the input value is not a valid non-empty string.
            Exception: If an unexpected error occurs during parsing.

        Examples:
            >>> parsing_value("5k")
            5000
            >>> parsing_value("3M")
            3000000
            >>> parsing_value("123")
            123
            >>> parsing_value("invalid")
            -1
        """

        int_value = -1

        try:
            assert (isinstance(value, str)
                    and len(value)), (
                        "Missing or invalid value."
            )

            factors = {'k': 1e3,
                       'M': 1e6,
                       'B': 1e9}
            if value.endswith((tuple(factors))):
                int_value = int(float(value[:-1]) * factors[value[-1]])
            else:
                int_value = int(value)

            return int_value

        except AssertionError as error:
            print(f"{type(error).__name__}: {error}")
            return -1
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            return -1

    def human_readable_formatter(x, _):
        """
        Converts a large number into a human-readable
        string format (e.g., "5k", "3M", "2B").
        This function is commonly used for formatting axis labels in plots.

        Args:
            x (float or int): The numeric value to format.
            _ (Any): A placeholder argument required
                for compatibility with certain libraries
                (e.g., matplotlib tick formatters).

        Returns:
            str: The formatted string in a human-readable format.

        Examples:
            >>> human_readable_formatter(5000, None)
            '5k'
            >>> human_readable_formatter(3000000, None)
            '3M'
            >>> human_readable_formatter(2000000000, None)
            '2B'
            >>> human_readable_formatter(500, None)
            '500'
        """

        if x >= 1_000_000_000:
            return f"{int(x / 1_000_000_000)}B"
        elif x >= 1_000_000:
            return f"{int(x / 1_000_000)}M"
        elif x >= 1_000:
            return f"{int(x / 1_000)}k"
        else:
            return str(int(x))

    # TO SKIP THESE NOTES, CLICK ON THE LITTLE ARROW
    # JUST AFTER THE LINE NUMBER (ON VSCODE), ON THE if NOTES: line just below
    if NOTES:
        if not all([DEBUG, PRINT_NOTES]):
            print("For this part NOTES part, "
                  "it is advised to enable DEBUG, and PRINT_NOTES.\n")
        """
        This df is quite similar,
        compared to the previous exercise df:
        Columns: 'country', and then years from 1800 to 2100.
        Default index: each line are indexed from 0 to 196.
        Lines: one for each country.
        We want to plot data from two (or several, but not all)
        countries.

        So first usual step: data = parsing_reindex_df(data)
        Several checks, and also: reindexing with country.
        """
        data = parsing_reindex_df(data)
        if PRINT_NOTES:
            print(f"data:\n{data}")
        """
        In case of some values are missing, we use the dropna method,
        to remove them.

        We also can see that (most of) the values contain letters
        (k, M, B, which of course means thousand, million, and billion).
        So we need to parse them with the apply method before any plot,
        and then convert them to integers.
        """
        plt.figure(figsize=(12, 8))
        for icolor, country in enumerate(COUNTRIES):
            country_data = data.loc[country].dropna().apply(parsing_value)
            years = country_data.index.astype(int)
            values = country_data.values.astype(float)
            plt.plot(years, values, label=country, color=COLORS[icolor])
        """
        We add some details required by the subject.
        """
        plt.title("Population Projections", fontsize=16)
        plt.xlabel("Year", fontsize=14)
        plt.ylabel("Population", fontsize=14)
        plt.legend(loc="lower right", fontsize=12)

        # As plt.show() "consumes" everything set before with plt,
        # remind to switch on or off this one.
        # Everything after won't work as expected if this stays enabled.
        if 0:
            print("\nA first plt.show(), not good enough.")
            plt.show()
        """
        Last detail: the y axis legend, written in scientific notation.
        To convert that to M (millions), here are the steps:
        plt.gca().yaxis.set_major_formatter(FuncFormatter(human_readable_formatter))
        plt.gca().yaxis.set_major_locator(MultipleLocator(20_000_000))

        About the first line:
        gca stands fro get current axis.
        set_major_formatter is useful for modifying
            how the values are displayed on this axis.
        human_readable_formatter is a function I wrote,
            in order to get the effect expected.
        """
        plt.gca().yaxis.set_major_formatter(human_readable_formatter)
        # As plt.show() "consumes" everything set before with plt,
        # remind to switch on or off this one.
        # Everything after won't work as expected if this stays enabled.
        if 0:
            print("\nA first plt.show(), not good enough.")
            plt.show()
        """
        But the first line is not enough for formating exactly
        as the subject requires.
        We want the y axis legend with slices of 20M.
        Here are some explanations about the second line:
        plt.gca().yaxis.set_major_locator(MultipleLocator(20_000_000))
        set_major_locator to set the intervals between each value
            displayed on the y axis.
            Requires a parameter type matplotlib.ticker.Locator
        MultipleLocator(20_000_000) is such a parameter
            20_000_000 is then the range of the intervals.
        """
        plt.gca().yaxis.set_major_locator(MultipleLocator(20_000_000))

        plt.show()

        return None

    try:
        assert data is not None, ("data is None")
        assert len(COLORS) >= len(COUNTRIES), ("More countries than colors.")

        data = parsing_reindex_df(data)

        plt.figure(figsize=(12, 8))

        for icolor, country in enumerate(COUNTRIES):
            country_data = data.loc[country].dropna().apply(parsing_value)
            years = country_data.index.astype(int)
            values = country_data.values.astype(float)
            plt.plot(years, values, label=country, color=COLORS[icolor])

        plt.title("Population Projections", fontsize=16)
        plt.xlabel("Year", fontsize=14)
        plt.ylabel("Population", fontsize=14)
        plt.legend(loc="lower right", fontsize=12)
        plt.gca().yaxis.set_major_formatter(human_readable_formatter)
        plt.gca().yaxis.set_major_locator(MultipleLocator(20_000_000))
        plt.show()

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()
