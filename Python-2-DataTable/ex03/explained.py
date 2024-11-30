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
import mplcursors
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

    BONUS = 1
    DEBUG = 1

    data_y_path = "life_expectancy_years.csv"
    data_x_path = "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
    data_point_size_path = "population_total.csv"
    YEAR = 1900

    try:
        data_y = load(data_y_path)
        data_x = load(data_x_path)
        if BONUS:
            data_point_size = load(data_point_size_path)

        if DEBUG:
            print("\n### DEBUG ###\n"
                  "function: main from projection_life.py\n"
                  f"data_y_path: {data_y_path}\n"
                  f"data_y:\n{data_y.head()}\n"
                  f"data_y.shape:\n{data_y.shape}\n"
                  f"data_x_path: {data_x_path}\n"
                  f"data_x:\n{data_x.head()}\n"
                  f"data_x.shape:\n{data_x.shape}\n")
            if BONUS:
                print(f"data_point_size_path: {data_point_size_path}\n"
                      f"data_point_size:\n{data_point_size.head()}\n"
                      f"data_point_size.shape:\n{data_point_size.shape}\n")
            print(f"\nYEAR: {YEAR}"
                  "\n### DEBUG END###\n")

        year_col = str(YEAR)
        assert year_col in data_y.columns, (
            f"The year {YEAR} is not available in {data_y_path}."
        )
        assert year_col in data_x.columns, (
            f"The year {YEAR} is not available in {data_x_path}."
        )
        if BONUS:
            assert year_col in data_point_size.columns, (
                f"The year {YEAR} is not available in {data_point_size_path}."
            )

        """
        life_expectancy_year = data_y[['country', year_col]]
        is the way to extract some specific columns from a df.
        """
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

        if BONUS:
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
                    AssertionError: If the input value
                    is not a valid non-empty string.
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

            pop_year = data_point_size[['country', year_col]].rename(
                columns={year_col: 'population'})
            pop_year['population'] = pop_year['population'].apply(
                parsing_value)
            if DEBUG:
                print("pop_year.head():"
                      f"\n{pop_year.head()}\n")

        merged_data = pd.merge(life_expectancy_year, gdp_year, on='country')
        if BONUS:
            merged_data = pd.merge(merged_data, pop_year, on='country')
        if DEBUG:
            print("merged_data.head():"
                  f"\n{merged_data.head()}\n")

        merged_data = merged_data.dropna()

        merged_data['life_expectancy'] = merged_data[
            'life_expectancy'].astype(float)
        merged_data['gdp'] = merged_data['gdp'].astype(float)
        if BONUS:
            merged_data['population'] = merged_data['population'].astype(float)
        if DEBUG:
            print("merged_data.head():"
                  f"\n{merged_data.head()}\n")

        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(
            x=merged_data['gdp'],
            y=merged_data['life_expectancy'],
            s=merged_data['population']/1e6 if BONUS else None  # point size
        )
        plt.xscale('log')
        plt.title(f"{YEAR}")
        plt.xlabel("Gross domestic product")
        plt.ylabel("Life Expectancy")

        ticks = [300, 1000, 10000]
        labels = ['300', '1k', '10k']
        plt.xticks(ticks, labels)

        if BONUS:
            cursor = mplcursors.cursor(scatter, hover=True)
            """
            What is sel ?
            mplcursors sends a Selection object (as defined in the library)
            to the event manager function just below.

            When the event add is launched
            (by hovering a point with the mouse):
            mplcursors gets the elements about the selected/hovered point,
            and stores them into the Selection object, referred as sel.

            sel.index :
                Allows to retrieve the data from the df.
            sel.annotation :
                Automatically created by matplotlib for each point.
                Can be modified, as the on_add function does.
            """
            @cursor.connect("add")
            def on_add(sel):
                """
                Handles the event triggered by hovering
                or selecting a point in the scatter plot.

                This function is called when the "add"
                event is triggered by mplcursors.
                It updates the annotation (tooltip) for the
                selected point to display the country name,
                with customized text and background styling.

                Args:
                    sel (mplcursors.Selection):
                        An object representing the selected point.
                        Contains attributes such as:
                        - `sel.index`:
                            Index of the selected point in the underlying data.
                        - `sel.annotation`:
                            Annotation object for customizing the tooltip.

                Behavior:
                    - Retrieves the country name from the `merged_data`
                    DataFrame using `sel.index`.
                    - Sets the annotation text to the country name.
                    - Customizes the annotation's appearance
                    (font, size, and background).
                """

                country = merged_data.iloc[sel.index]["country"]
                sel.annotation.set(
                    text=country, fontsize=10, fontweight="bold")
                sel.annotation.get_bbox_patch().set(alpha=0.6, color="white")
            """
            cursor.connect("add", on_add)
            Without the decorator above the on_add function,
            this line would be used.
            """

        plt.show()

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()
