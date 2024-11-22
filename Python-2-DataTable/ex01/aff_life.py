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

        years = country_data.columns[1:].astype(int)
        values = country_data.iloc[0, 1:].astype(float)

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
