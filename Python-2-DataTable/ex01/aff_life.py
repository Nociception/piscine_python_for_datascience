# Subject
"""
Exercice 01: draw my country
Turn-in directory : ex01/
Files to turn in : load_csv.py, aff_life.py
Allowed functions : matplotlib, seaborn or any lib for Data Visualization

Create a program that calls the load function from
the previous exercise, loads the file life_expectancy_years.csv,
and displays the country information of your campus.
Your graph must have a title and a legend for each axis.

For example, for the 42 campuses in France we will have this result:
see the expected_projections.jpg in the git hub repo.
"""

import pandas as pd
import matplotlib.pyplot as plt


def plot_life_expectancy(data: pd.DataFrame, country: str) -> None:
    """
    Plots the life expectancy of a specific country over the years.

    Args:
        data (pd.DataFrame): The dataset containing life expectancy data.
        country (str): The name of the country to plot.

    Returns:
        None
    """
    try:
        if country not in data['country'].values:
            raise ValueError(f"The country '{country}' is not in the dataset.")

        country_data = data[data['country'] == country]
        """
        As the df contains a line for each country,
        and a column for each year (from 1800 to 2100),
        this instruction gives a new one-line df
        (as each line are unique, one for each country).
        country_data is Series (what you get when you slice a pandas' df)
        So get one specific line only requires simple slicing syntax,
        combined wth a boolean.
        Uncomment the following instruction in order to see this line :
        """
        print(country_data)
        print(country_data.shape)

        """
        Out of the exercise's subject :
        Let's now consider that we want all countries' data
        for one specific year.
        Previsualize what the result will look like:
        194 lines (one for each country + one for the header)
        2 columns : country, and the specific year you target.
        Therefore, you need a sub dataframe (also called subset).
        Therefore, the syntax won't be the same.
        Uncomment the two following instructions to see the syntax
        and its result.
        """
        # another_slice = data[['country', '1960']]
        # print(another_slice)

        years = country_data.columns[1:].astype(int)
        """
        
        """
        # print(country_data.columns)

        values = country_data.iloc[0, 1:].astype(float)


        print("----------------------------------------------")
        plt.figure(figsize=(10, 6))
        plt.plot(years, values, label=country)
        plt.title(f"{country} Life expectancy Projections")
        plt.xlabel("Year")
        plt.ylabel("Life expectancy")
        plt.grid(True)
        plt.show()

    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
