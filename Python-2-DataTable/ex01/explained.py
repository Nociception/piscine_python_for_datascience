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
    PRINT_NOTES = 0

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

    try:
        """
        The df is organized as such:
        First column: 'country'
        the following ones are the years '1800', '1801', ..., '2100'
        First line: the header
        the following ones are the countries
        'Afghanistan', 'Angola', ..., 'Zimbabwe'

        A good way to visualize a df (example from Pandas' doc):
        df = pd.DataFrame(
            {
                "Name": [
                    "Braund, Mr. Owen Harris",
                    "Allen, Mr. William Henry",
                    "Bonnell, Miss. Elizabeth",
                ],
                "Age": [22, 35, 58],
                "Sex": ["male", "male", "female"],
            }
        )
        df
                            Name  Age     Sex
        0   Braund, Mr. Owen Harris   22    male
        1  Allen, Mr. William Henry   35    male
        2  Bonnell, Miss. Elizabeth   58  female

        A dictionnary with columns as keys, and a list of values as values.
        From the Pandas' doc :
        "If you are familiar with Python dictionaries,
        the selection of a single column is very similar
        to the selection of dictionary values based on the key."


        Now that we have this in mind, let's focus on what we want,
        and how to get it.
        As we want to target a specific country's (here: France) values,
        here are the steps (checking ones, and "getting" ones):

        1st:
        Check if the column 'country' exists in the df.
        Several ways (switch the if condition with 0 or 1 if necessary):
        """
        if PRINT_NOTES:
            print("\nNotes (1)")
            print(f"'country' in data:\n{'country' in data}")
            # True ; As expected: data can be handled as a dictionnary.

            print(f"data.columns:\n{data.columns}")
            # Provides a list of each columns.
            print(f"'country' in data.columns:\n{'country' in data.columns}")
            # True
            # My favorite way ; explicit (with the attribute columns,
            # and that as long as the following way).

            print(f"data.columns.values: {data.columns.values}")
            # Provides the same list as above.
            print(
                "'country' in data.columns.values:\n"
                f"{'country' in data.columns.values}"
            )  # True
        """
        So let's check that now:
        """
        assert 'country' in data.columns, (
            "'country' is not a column of the dataframe."
        )
        """
        2nd:
        Getting the line for a specific country.
        Here, "France" is stored in the function's parameter `country`.
        I confess I want to use that kind of syntax:
        data[country]
        But this leads to an error, as the "keys" are "country" and the years.
        So no "France".

        We first change the indexes with:
        """
        data.set_index('country', inplace=True)
        """
        Don't worry, it is possible to, if necessary,
        get back the default indexes with:
        data.reset_index(inplace=True)
        """
        if PRINT_NOTES:
            print("\nNotes (2)")
            print(f"data:\n{data}")
            print(f"data.columns:\n{data.columns}")
        """
        We observe that this index changing removed the 'country' column.
        There only are years.

        Then, data[country] is still not possible : "France" is not
        a column.
        But something quite near is now possible!
        data.loc[country]
        Before using that it is better to check if this country is in the df:
        """
        assert country in data.index, (
                f"{country} not in the dataframe.")
        if PRINT_NOTES:
            print("\nNotes (3)")
            print(f"data.loc[country]:\n{data.loc[country]}")
            print(f"type(data.loc[country]):\n{type(data.loc[country])}")
        """
        data.loc[country] provides a Series
        (as a df is a collection of Series),
        where indexes are the years, and values are the life expectancies.
        Let's now store these precious data in a variable.
        """
        country_data = data.loc[country]
        """
        Now that we have the data for only the country we want to target,
        Two last packed steps for preparing the pyplot.
        3rd:
        """
        years = country_data.index.astype(int)
        values = country_data.values.astype(float)
        if PRINT_NOTES:
            print("\nNotes (4)")
            print(f"country_data:\n{country_data}")
        """
        Indexes and values casted to the right type.
        It does not change the display of country_data, but it is
        necessary for the pyplot.

        4th:
        And now, the pyplot:
        """
        plt.figure(figsize=(10, 6))
        plt.plot(years, values, label=country, color='blue', linewidth=2)
        plt.title(f"Life expectancy in {country} over time", fontsize=14)
        plt.xlabel("Year", fontsize=12)
        plt.xlabel("Life expectancy (years)", fontsize=12)
        plt.grid(True)
        plt.legend(loc="upper left", fontsize=10)
        plt.show()

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
    finally:
        return None


if __name__ == "__main__":
    main()
