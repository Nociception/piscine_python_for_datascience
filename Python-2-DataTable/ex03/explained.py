"""
Many MULTILINE STRINGS in this file.
Once you read one (or not), remind to FOLD it in order to avoid
flood during your reading.
For instance, try with this one (featur available on VSCode):
click on the little down arrow between the line number 1,
and the three " " " to fold this multiline string.
Hope you have somehting similar, dear vim users <3

You can also fold DOCSTRING, little if (debug related),
and little functions, theoretically well named.

As this file is explained, many text written can flood
and make your reading experience painful.
"""

import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
from load_csv import load
from scipy.stats import linregress
import numpy as np


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

    BONUS = 1  # switch it between 0 or 1 to enable the bonus part.

    DEBUG = 0
    DEBUG_BEACON = 1
    """
    Concerns all the debug print, for knowing what variable content
    at many code critical steps.
    All debug print are conditionned as such:
    if DEBUG and DEBUG_BEACON:
        print(...)

    DEBUG: switch it between 0 or 1 to enable debug prints.
    Initially set to 0.
    This variable is set here and nowhere else.
    0: no debug print will be display at all.
    1: allows debug prints to be display ; adjusted with DEBUG_BEACON

    DEBUG_BEACON:switch it between 0 or 1 to adjust debug prints.
    This variable can be set again before every debug print.
    Initially, they all are set on 1.
    Set 0 or 1 anywhere, according to which debug prints you would like to see.
    """

    data_y_path = "life_expectancy_years.csv"
    data_x_path = "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
    if BONUS:
        data_point_size_path = "population_total.csv"
    YEAR = 1900

    try:
        data_y = load(data_y_path)
        data_x = load(data_x_path)
        if BONUS:
            data_point_size = load(data_point_size_path)

        if DEBUG and DEBUG_BEACON:
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

        # ===== Checking year_col presence in each df =====
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

        # ===== Subsets extraction =====
        life_expectancy_year = data_y[['country', year_col]].rename(
            columns={year_col: 'life_expectancy'}
        )
        DEBUG_BEACON = 1
        if DEBUG and DEBUG_BEACON:
            print("life_expectancy_year.head():"
                  f"\n{life_expectancy_year.head()}\n")
            print(f"life_expectancy_year.shape: {life_expectancy_year.shape}")
        """
        life_expectancy_year = data_y[['country', year_col]]
        is the way to extract some specific columns from a df.
        rename accepts several fields like index, columns, etc...
        These are values which can contain a dictionnary :
        keys are the column's names to replace
        values are their  substitute
        """

        gdp_year = data_x[['country', year_col]].rename(
            columns={year_col: 'gdp'}
        )
        DEBUG_BEACON = 1
        if DEBUG and DEBUG_BEACON:
            print(f"gdp_year.head():\n{gdp_year.head()}\n")
            print(f"gdp_year.shape:\n{gdp_year.shape}\n")

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
            DEBUG_BEACON = 1
            if DEBUG and DEBUG_BEACON:
                print(f"pop_year.head():\n{pop_year.head()}"
                      "pop_year['population'].head():\n"
                      f"{pop_year['population'].head()}")
            pop_year['population'] = pop_year['population'].apply(
                parsing_value)
            DEBUG_BEACON = 1
            if DEBUG and DEBUG_BEACON:
                print(f"pop_year.head():\n{pop_year.head()}\n")
                print(f"pop_year.shape:\n{pop_year.shape}\n")

        # ===== Subsets merge =====
        merged_data = pd.merge(life_expectancy_year, gdp_year, on='country')
        if BONUS:
            merged_data = pd.merge(merged_data, pop_year, on='country')
        DEBUG_BEACON = 1
        if DEBUG and DEBUG_BEACON:
            print(f"merged_data.head():\n{merged_data.head()}\n")
            print(f"merged_data.shape: {merged_data.shape}")

        # ===== merged_data tailoring =====
        merged_data = merged_data.dropna()
        DEBUG_BEACON = 1
        if DEBUG and DEBUG_BEACON:
            print(f"merged_data.head():\n{merged_data.head()}\n")
            print(f"merged_data.shape: {merged_data.shape}")
        merged_data['life_expectancy'] = merged_data[
            'life_expectancy'].astype(float)
        merged_data['gdp'] = merged_data['gdp'].astype(float)
        if BONUS:
            merged_data['population'] = merged_data['population'].astype(float)
        DEBUG_BEACON = 1
        if DEBUG and DEBUG_BEACON:
            print(f"merged_data.head():\n{merged_data.head()}\n")

        # ===== matplotlib settings start from here =====
        fig, ax = plt.subplots(figsize=(10, 6))
        """
        plt.subplots() returns two objects :
        - a Figure object, which contains everything, like a canvas;
        it contains among other things Axes objects.
        It's possible to save a figure with: fig.savefig("savefile.png")
        - an Axes object, where the charts will be drawn.
        As we here have only one chart, we will use everytime this
        variable. As it is a quite usual case, that is probably why
        these variables fix and ax are not created, and the implicit
        automation is used.
        As I prefer explicit objects, I will then use them.
        They become even more useful when more than one Axes objects
        is included in a single Figure object; for example:
            fig, axes = plt.subplots(2, 2, figsize=(10, 8))  # Grille 2x2
            axes[0, 0].plot(x, y)  # first subplot (top left)
            axes[0, 1].scatter(x, y)  # second subplot (top right)
            axes[1, 0].bar(x, y)  # third subplot (bottom left)
            axes[1, 1].hist(y)  # fourth subplot (bottom right)
        """

        scatter = ax.scatter(
            x=merged_data['gdp'],
            y=merged_data['life_expectancy'],
            s=merged_data['population']/1e6 if BONUS else None,  # point's size
            alpha=0.7,  # point's transparancy
            label="Countries (population-weighted)"
        )
        """
        print(f"type(scatter): {type(scatter)}")
            type(scatter): <class 'matplotlib.collections.PathCollection'>
        Does two things here:
        - Creates the scatter object (type showed just above).
        - Adds it to the ax object.
        matplotlib scatter allows to realize what the exercise requests.
        Beyond that requirement, here are some hints about the scatter
        usage, and why to use it:
        A df has two numeric columns, without any link.
        No line order.
        Then a scatter plot allows to :
        - see a potential correlation between the two columns
        - outliers detection
        - add (if relevant) a third data on the dots
        """

        if BONUS:
            # ===== Linear regression settings =====
            slope, intercept, r_value, p_value, std_err = linregress(
                np.log10(merged_data['gdp']), merged_data['life_expectancy']
            )
            """
            linregress is used here to obtain information about the
            linear regression between GDP and life expectancy.
            Here:
            x = np.log10(merged_data['gdp'])
            y = merged_data['life_expectancy']
            n = shape[1] (186: nb of countries with data in 1900)
            linregress returns three key values among others:
            - slope: the slope of the regression line.
            slope = Cov(x,y)/Var(x)
            Cov stands for covariance:
            Cov(x,y) = (1/n) * sum[i=1 to n]((x_i-mean(x)) * (y_i-mean(y)))

            Var for variance:
            Var(x) = (1/n) * sum[i=1 to n]((x_i-mean(x))**2)
            - intercept: the y-intercept of this line.
            This can be represented as: slope * x + intercept (ax+b).
            intercept = mean(y) - slope * mean(x)
            - r_value: the Pearson correlation coefficient
            between the two variables (GDP and life_expectancy).
            - 1: perfect positive correlation.
            - -1: perfect negative correlation.
            - 0: no correlation.
            r_value = cov(x,y)/sqrt(var(x)*var(y))

            No explanation is provided here for p_value and std_err,
            although they must be included for the unpacking of
            the returned linregress tuple.

            About the linear regression mathematical tool:
            The idea is to find the linear formula ax+b for a line
            as close as possible of every points.
            """

            gdp_sorted = np.sort(merged_data['gdp'])
            predicted_life_expectancy = (
                slope * np.log10(gdp_sorted) + intercept
            )
            """
            print(type(predicted_life_expectancy))  # <class 'numpy.ndarray'>
            Now that slope and intercept are calculated,
            it is possible to use them as a model:
            applying them with the formula
            slope * np.log10(gdp_sorted) + intercept
            it provides an array of life expectancies predicted
            by the model.
            As it will plot, we need the array sorted
            (whereas initially, order did not matter).
            """

            ax.plot(
                gdp_sorted,
                predicted_life_expectancy,
                color="red",
                linestyle="--",
                label="Regression Line (log-linear)"
            )

            # ===== Correlation displaying =====
            ax.text(
                0.5, -0.2,
                f"Correlation: {r_value:.2f}",
                fontsize=12,
                color="red",
                ha='center',
                transform=plt.gca().transAxes,
                bbox=dict(
                    facecolor='white',
                    edgecolor='red',
                    alpha=0.8,
                    linestyle='--'
                )
            )

            fig.subplots_adjust(bottom=0.25)
            """To make the correlation displaying visible."""

        # ===== Chart and window title settings =====
        title = f"Life Expectancy vs GDP per country in {YEAR}"
        ax.set_title(title)
        fig.canvas.manager.set_window_title(title)

        ax.set_xscale('log')
        ax.set_xlabel("Gross Domestic Product (USD, log scale)")
        ticks = [300, 1000, 10000]
        labels = ['300', '1k', '10k']
        ax.set_xticks(ticks, labels)

        ax.set_ylabel("Life Expectancy (years)")

        ax.legend(loc="best")

        # ===== Info tooltip cursor =====
        if BONUS:
            def put_kmb_suffix(val: int) -> str:
                """
                Formats a large number with 'k', 'M', or 'B' suffixes.
                """
                for threshold, suffix in [(1e9, 'B'), (1e6, 'M'), (1e3, 'k')]:
                    if val > threshold:
                        return f"{val / threshold:.2f}{suffix}"
                return str(val)

            cursor = mplcursors.cursor(scatter, hover=True)
            """
            print(type(cursor))  # <class 'mplcursors._mplcursors.Cursor'>
            Creates an object linked to the scatter variable.
            Further details just belows.
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

                row = merged_data.iloc[sel.index]
                country = row["country"]
                life_expectancy = row["life_expectancy"]
                population = row["population"]
                gdp = row["gdp"]

                sel.annotation.set(
                    text=(
                        f"{country}\n"
                        f"Life Expectancy: {life_expectancy} years\n"
                        f"GDP per capita: {gdp}\n"
                        f"Population: {put_kmb_suffix(population)}"
                    ),
                    fontsize=10, fontweight="bold")
                sel.annotation.get_bbox_patch().set(alpha=0.6, color="white")
            """
            cursor.connect("add", on_add)
            Without the decorator above the on_add function,
            this line would be used : exactly the same effet.

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

        # ===== Final rendering =====
        DEBUG_BEACON = 1
        if DEBUG and DEBUG_BEACON:
            print("### fig and ax content summary ###")
            print(f"Size: {fig.get_size_inches()} inches")
            print(f"Number of axes: {len(fig.axes)}")

            print("\nAxes summary:")
            print(f"Title: {ax.get_title()}")
            print(f"X-label: {ax.get_xlabel()}")
            print(f"Y-label: {ax.get_ylabel()}")
            print(f"Number of children in Axes: {len(ax.get_children())}")

            print("\nChildren of Axes:")
            for child in ax.get_children():
                print(f"  - {type(child).__name__}: {child}")
            print("### END fig and ax content summary ###")

        plt.show()

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()
