# Subject
"""
Exercice 03: draw my year
Turn-in directory : ex03/
Files to turn in : load_csv.py, projection_life.py
Allowed functions : matplotlib, seaborn or any lib for Data Visualization and
your lib of ex00

Create a program that calls the load function from the first exercise,
loads the files "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
and "life_expectancy_years.csv", and displays the projection of
life expectancy in relation to the gross national product of
the year 1900 for each country.
Your graph must have a title,
a legend for each axis and a legend for each graph.
You must display the year 1900.

See the expected.jpg file in the github repo.
"""

import pandas as pd
import matplotlib.pyplot as plt
from load_csv import load


def main() -> None:
    """
    Main function to load data, process it, and visualize life expectancy
    versus GDP for a specific year.

    This function performs the following steps:
    1. Loads three datasets:
        - Life expectancy data (life_expectancy_years.csv)
        - GDP data (income_per_person_gdppercapita_ppp_inflation_adjusted.csv)
        - Population data (population_total.csv)
    2. Selects data for the specified year (`YEAR`).
    3. Processes and merges the datasets to prepare for visualization.
    4. Generates a scatter plot:
        - X-axis: GDP (logarithmic scale)
        - Y-axis: Life expectancy
        - Point size: Proportional to population
    5. Customizes the plot with dynamic ticks and labels.
    6. Adds interactive tooltips displaying the country name on hover.

    Key Variables:
        YEAR (int): The year for which the data is visualized.
        DEBUG (int): Set to 1 to enable debug prints; otherwise 0.
        BONUS (int): Set to 1 to enable the bonus part; otherwise 0.

    Exception Handling:
        - Raises an `AssertionError`
        if the selected year is not available in the datasets.
        - Catches and prints unexpected errors.
    """

    DEBUG = 0

    data_y_path = "life_expectancy_years.csv"
    data_x_path = "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
    YEAR = 1900

    try:
        data_y = load(data_y_path)
        data_x = load(data_x_path)

        if DEBUG:
            print("\n### DEBUG ###\n"
                  "function: main from projection_life.py\n"
                  f"data_y_path: {data_y_path}\n"
                  f"data_y:\n{data_y.head()}\n"
                  f"data_y.shape:\n{data_y.shape}\n"
                  f"data_x_path: {data_x_path}\n"
                  f"data_x:\n{data_x.head()}\n"
                  f"data_x.shape:\n{data_x.shape}\n")
            print(f"\nYEAR: {YEAR}"
                  "\n### DEBUG END###\n")

        year_col = str(YEAR)
        assert year_col in data_y.columns, (
            f"The year {YEAR} is not available in {data_y_path}."
        )
        assert year_col in data_x.columns, (
            f"The year {YEAR} is not available in {data_x_path}."
        )

        life_expectancy_year = data_y[['country', year_col]].rename(
            columns={year_col: 'life_expectancy'}
        )
        if DEBUG:
            print("life_expectancy_year.head():"
                  f"\n{life_expectancy_year.head()}\n")

        gdp_year = data_x[['country', year_col]].rename(
            columns={year_col: 'gdp'}
        )
        if DEBUG:
            print("gdp_year.head():"
                  f"\n{gdp_year.head()}\n")

        merged_data = pd.merge(life_expectancy_year, gdp_year, on='country')
        if DEBUG:
            print("merged_data.head():"
                  f"\n{merged_data.head()}\n")

        merged_data = merged_data.dropna()

        merged_data['life_expectancy'] = merged_data[
            'life_expectancy'].astype(float)
        merged_data['gdp'] = merged_data['gdp'].astype(float)
        if DEBUG:
            print("merged_data.head():"
                  f"\n{merged_data.head()}\n")

        plt.figure(figsize=(10, 6))
        plt.scatter(
            x=merged_data['gdp'],
            y=merged_data['life_expectancy'],
        )
        plt.xscale('log')
        plt.title(f"{YEAR}")
        plt.xlabel("Gross domestic product")
        plt.ylabel("Life Expectancy")

        ticks = [300, 1000, 10000]
        labels = ['300', '1k', '10k']
        plt.xticks(ticks, labels)

        plt.show()

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()
