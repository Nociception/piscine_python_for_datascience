# Subject
"""
Exercice 03: draw my year
Turn-in directory : ex03/
Files to turn in : load_csv.py, projection_life.py
Allowed functions : matplotlib, seaborn or any lib for Data Visualization and
your lib of ex00
Create a program that calls the load function from the first exercise, loads the files "income_per_person_gdppercapita_ppp_inflation_adjusted.csv" and "life_expectancy_years.csv",
and displays the projection of life expectancy in relation to the gross national product of
the year 1900 for each country.
Your graph must have a title, a legend for each axis and a legend for each graph.
You must display the year 1900.
"""

import pandas as pd
import matplotlib.pyplot as plt
from load_csv import load 


def main() -> None:
    """DOCSTRING"""

    DEBUG = 0
    NOTES = 0
    PRINT_NOTES = 1

    data_y_path = "life_expectancy_years.csv"
    data_x_path = "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
    YEAR = 1900

    # if DEBUG:
    #     print("\n### DEBUG ###\n"
    #           "function: main from aff_pop.py\n"
    #           "data:\n"
    #           f"{data}"
    #           f"\nYEAR: {YEAR}"
    #           "\n### DEBUG END###\n")

    # # TO SKIP THESE NOTES, CLICK ON THE LITTLE ARROW
    # # JUST AFTER THE LINE NUMBER (ON VSCODE), ON THE if NOTES: line just below
    # if NOTES:
    #     if not all([DEBUG, PRINT_NOTES]):
    #         print("For this part NOTES part, "
    #               "it is advised to enable DEBUG, and PRINT_NOTES.\n")

    #     return None


    try:
        data_y = load(data_y_path)
        data_x = load(data_x_path)

        year_col = str(YEAR)
        assert (year_col in data_y.columns
                and year_col in data_y.columns), (
                    f"The year {YEAR} is not available in the datasets."
                )

        life_expectancy_year = data_y[['country', year_col]].rename(
            columns={year_col: 'life_expectancy'}
        )
        gdp_year = data_x[['country', year_col]].rename(columns={year_col: 'gdp'})

        merged_data = pd.merge(life_expectancy_year, gdp_year, on='country')

        merged_data = merged_data.dropna()

        merged_data['life_expectancy'] = merged_data['life_expectancy'].astype(float)
        merged_data['gdp'] = merged_data['gdp'].astype(float)

        plt.figure(figsize=(10, 6))
        plt.scatter(
            merged_data['gdp'],
            merged_data['life_expectancy']
        )

        plt.xscale('log')
        plt.xlim(300, 10000)
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
