import pandas as pd
import matplotlib.pyplot as plt
from load_csv import load

# Read before anything
"""
This file contains two part:
    - first: uncommented run-ready code,
    designed to fullfill the subject requirement.
    - second: commented code, for two files (separated with a big blank):
        They are separated with block a @ lines such as:
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@ file_name.py @@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        - explained.py: an explained code file.
        Contains the mandatory part,
        and a personnal bonus (as the subject does not contain
        any real bonus).

        - poo.py: a poo code file for a data vizualisation
        from 1800 to 2050.
        The idea is to compare the correlation
        whether log scale usage or not.
        The population dataset from previous exercise is also used.
        An extra data set must be download here :
        https://data.worldbank.org/indicator/SI.POV.GINI

        Copy paste in a new file the commented code, and then
        uncomment it in the new file.
"""

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

Do you see a correlation between life span and gross domestic product?
"""


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

        # Checking
        year_col = str(YEAR)
        assert year_col in data_y.columns, (
            f"The year {YEAR} is not available in {data_y_path}."
        )
        assert year_col in data_x.columns, (
            f"The year {YEAR} is not available in {data_x_path}."
        )

        # Extraction
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

        # extracted data merging
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

        # matplotlib figure settings
        plt.figure(figsize=(10, 6))
        plt.scatter(
            x=merged_data['gdp'],
            y=merged_data['life_expectancy'],
            label="Countries"
        )
        plt.xscale('log')
        plt.title(f"Life Expectancy vs GDP per country in {YEAR}")
        plt.xlabel("GDP per person at PPP inflation adjusted (USD, log scale)")
        plt.ylabel("Life Expectancy (years)")
        plt.gcf().canvas.manager.set_window_title(
            f"Life Expectancy vs GDP ({YEAR})"
        )

        ticks = [300, 1000, 10000]
        labels = ['300', '1k', '10k']
        plt.xticks(ticks, labels)

        plt.legend(loc="best")

        plt.show()

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@ explained.py @@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# """
# Many MULTILINE STRINGS in this file.
# Once you read one (or not), remind to FOLD it in order to avoid
# flood during your reading.
# For instance, try with this one (featur available on VSCode):
# click on the little down arrow between the line number 1,
# and the three " " " to fold this multiline string.
# Hope you have somehting similar, dear vim users <3

# You can also fold DOCSTRING, little if (debug related),
# and little functions, theoretically well named.

# As this file is explained, many text written can flood
# and make your reading experience painful.
# """

# import pandas as pd
# import matplotlib.pyplot as plt
# import mplcursors
# from load_csv import load
# from scipy.stats import linregress
# import numpy as np


# def main() -> None:
#     """
#     Main function to load data, process it, and visualize life expectancy
#     versus GDP for a specific year.

#     This function performs the following steps:
#     1. Loads three datasets:
#         - Life expectancy data (life_expectancy_years.csv)
#         - GDP data:
#           income_per_person_gdppercapita_ppp_inflation_adjusted.csv
#         - Population data (population_total.csv)
#     2. Selects data for the specified year (`YEAR`).
#     3. Processes and merges the datasets to prepare for visualization.
#     4. Generates a scatter plot:
#         - X-axis: GDP (logarithmic scale)
#         - Y-axis: Life expectancy
#         - Point size: Proportional to population
#     5. Customizes the plot with dynamic ticks and labels.
#     6. Adds interactive tooltips displaying the country name on hover.

#     Key Variables:
#         YEAR (int): The year for which the data is visualized.
#         DEBUG (int): Set to 1 to enable debug prints; otherwise 0.
#         BONUS (int): Set to 1 to enable the bonus part; otherwise 0.

#     Exception Handling:
#         - Raises an `AssertionError`
#         if the selected year is not available in the datasets.
#         - Catches and prints unexpected errors.
#     """

#     BONUS = 1  # switch it between 0 or 1 to enable the bonus part.

#     DEBUG = 0
#     DEBUG_BEACON = 1
#     """
#     Concerns all the debug print, for knowing what variable content
#     at many code critical steps.
#     All debug print are conditionned as such:
#     if DEBUG and DEBUG_BEACON:
#         print(...)

#     DEBUG: switch it between 0 or 1 to enable debug prints.
#     Initially set to 0.
#     This variable is set here and nowhere else.
#     0: no debug print will be display at all.
#     1: allows debug prints to be display ; adjusted with DEBUG_BEACON

#     DEBUG_BEACON:switch it between 0 or 1 to adjust debug prints.
#     This variable can be set again before every debug print.
#     Initially, they all are set on 1.
#     Set 0 or 1 anywhere,
#     according to which debug prints you would like to see.
#     """

#     data_y_path = "life_expectancy_years.csv"
#     data_x_path = "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
#     if BONUS:
#         data_point_size_path = "population_total.csv"
#     YEAR = 1900

#     try:
#         data_y = load(data_y_path)
#         data_x = load(data_x_path)
#         if BONUS:
#             data_point_size = load(data_point_size_path)

#         if DEBUG and DEBUG_BEACON:
#             print("\n### DEBUG ###\n"
#                   "function: main from projection_life.py\n"
#                   f"data_y_path: {data_y_path}\n"
#                   f"data_y:\n{data_y.head()}\n"
#                   f"data_y.shape:\n{data_y.shape}\n"
#                   f"data_x_path: {data_x_path}\n"
#                   f"data_x:\n{data_x.head()}\n"
#                   f"data_x.shape:\n{data_x.shape}\n")
#             if BONUS:
#                 print(f"data_point_size_path: {data_point_size_path}\n"
#                       f"data_point_size:\n{data_point_size.head()}\n"
#                       f"data_point_size.shape:\n{data_point_size.shape}\n")
#             print(f"\nYEAR: {YEAR}"
#                   "\n### DEBUG END###\n")

#         # ===== Checking year_col presence in each df =====
#         year_col = str(YEAR)
#         assert year_col in data_y.columns, (
#             f"The year {YEAR} is not available in {data_y_path}."
#         )
#         assert year_col in data_x.columns, (
#             f"The year {YEAR} is not available in {data_x_path}."
#         )
#         if BONUS:
#             assert year_col in data_point_size.columns, (
#                 f"{YEAR} is not available in {data_point_size_path}."
#             )

#         # ===== Subsets extraction =====
#         life_expectancy_year = data_y[['country', year_col]].rename(
#             columns={year_col: 'life_expectancy'}
#         )
#         DEBUG_BEACON = 1
#         if DEBUG and DEBUG_BEACON:
#             print("life_expectancy_year.head():"
#                   f"\n{life_expectancy_year.head()}\n")
#         """
#         life_expectancy_year = data_y[['country', year_col]]
#         is the way to extract some specific columns from a df.
#         rename accepts several fields like index, columns, etc...
#         These are values which can contain a dictionnary :
#         keys are the column's names to replace
#         values are their  substitute
#         """

#         gdp_year = data_x[['country', year_col]].rename(
#             columns={year_col: 'gdp'}
#         )
#         DEBUG_BEACON = 1
#         if DEBUG and DEBUG_BEACON:
#             print(f"gdp_year.head():\n{gdp_year.head()}\n")
#             print(f"gdp_year.shape:\n{gdp_year.shape}\n")

#         if BONUS:
#             def parsing_value(value: str) -> int:
#                 """
#                 Parses a human-readable string representing a
#                 large number (e.g., "5k", "3M", "2B") into an integer value.

#                 Args:
#                     value (str): The human-readable string to parse.

#                 Returns:
#                     int: The parsed integer value.
#                     Returns -1 if an error occurs or the input is invalid.

#                 Raises:
#                     AssertionError: If the input value
#                     is not a valid non-empty string.
#                     Exception: If an unexpected error occurs during parsing.

#                 Examples:
#                     >>> parsing_value("5k")
#                     5000
#                     >>> parsing_value("3M")
#                     3000000
#                     >>> parsing_value("123")
#                     123
#                     >>> parsing_value("invalid")
#                     -1
#                 """

#                 int_value = -1

#                 try:
#                     assert (isinstance(value, str)
#                             and len(value)), (
#                                 "Missing or invalid value."
#                     )

#                     factors = {'k': 1e3,
#                                'M': 1e6,
#                                'B': 1e9}
#                     if value.endswith((tuple(factors))):
#                         int_value = int(
#                             float(value[:-1]) * factors[value[-1]])
#                     else:
#                         int_value = int(value)

#                     return int_value

#                 except AssertionError as error:
#                     print(f"{type(error).__name__}: {error}")
#                     return -1
#                 except Exception as error:
#                     print(f"An unexpected error occurred: {error}")
#                     return -1

#             pop_year = data_point_size[['country', year_col]].rename(
#                 columns={year_col: 'population'})
#             DEBUG_BEACON = 1
#             if DEBUG and DEBUG_BEACON:
#                 print(f"pop_year.head():\n{pop_year.head()}"
#                       "pop_year['population'].head():\n"
#                       f"{pop_year['population'].head()}")
#             pop_year['population'] = pop_year['population'].apply(
#                 parsing_value)
#             DEBUG_BEACON = 1
#             if DEBUG and DEBUG_BEACON:
#                 print(f"pop_year.head():\n{pop_year.head()}\n")
#                 print(f"pop_year.shape:\n{pop_year.shape}\n")

#         # ===== Subsets merge =====
#         merged_data = pd.merge(life_expectancy_year, gdp_year, on='country')
#         if BONUS:
#             merged_data = pd.merge(merged_data, pop_year, on='country')
#         DEBUG_BEACON = 1
#         if DEBUG and DEBUG_BEACON:
#             print(f"merged_data.head():\n{merged_data.head()}\n")
#             print(f"merged_data.shape: {merged_data.shape}")

#         # ===== merged_data tailoring =====
#         merged_data = merged_data.dropna()
#         DEBUG_BEACON = 1
#         if DEBUG and DEBUG_BEACON:
#             print(f"merged_data.head():\n{merged_data.head()}\n")
#             print(f"merged_data.shape: {merged_data.shape}")
#         merged_data['life_expectancy'] = merged_data[
#             'life_expectancy'].astype(float)
#         merged_data['gdp'] = merged_data['gdp'].astype(float)
#         if BONUS:
#             merged_data['population'] = merged_data[
#                 'population'].astype(float)
#         DEBUG_BEACON = 1
#         if DEBUG and DEBUG_BEACON:
#             print(f"merged_data.head():\n{merged_data.head()}\n")

#         # ===== matplotlib settings start from here =====
#         fig, ax = plt.subplots(figsize=(10, 6))
#         """
#         plt.subplots() returns two objects :
#         - a Figure object, which contains everything, like a canvas;
#         it contains among other things Axes objects.
#         It's possible to save a figure with: fig.savefig("savefile.png")
#         - an Axes object, where the charts will be drawn.
#         As we here have only one chart, we will use everytime this
#         variable. As it is a quite usual case, that is probably why
#         these variables fix and ax are not created, and the implicit
#         automation is used.
#         As I prefer explicit objects, I will then use them.
#         They become even more useful when more than one Axes objects
#         is included in a single Figure object; for example:
#             fig, axes = plt.subplots(2, 2, figsize=(10, 8))  # Grille 2x2
#             axes[0, 0].plot(x, y)  # first subplot (top left)
#             axes[0, 1].scatter(x, y)  # second subplot (top right)
#             axes[1, 0].bar(x, y)  # third subplot (bottom left)
#             axes[1, 1].hist(y)  # fourth subplot (bottom right)
#         """

#         scatter = ax.scatter(
#             x=merged_data['gdp'],
#             y=merged_data['life_expectancy'],
#             s=merged_data['population']/1e6 if BONUS else None,
#             alpha=0.7,  # point's transparancy
#             label="Countries (population-weighted)"
#         )
#         """
#         print(f"type(scatter): {type(scatter)}")
#             type(scatter): <class 'matplotlib.collections.PathCollection'>
#         Does two things here:
#         - Creates the scatter object (type showed just above).
#         - Adds it to the ax object.
#         matplotlib scatter allows to realize what the exercise requests.
#         Beyond that requirement, here are some hints about the scatter
#         usage, and why to use it:
#         A df has two numeric columns, without any link.
#         No line order.
#         Then a scatter plot allows to :
#         - see a potential correlation between the two columns
#         - outliers detection
#         - add (if relevant) a third data on the dots
#         """

#         if BONUS:
#             # ===== Linear regression settings =====
#             slope, intercept, r_value, p_value, std_err = linregress(
#                 np.log10(merged_data['gdp']), merged_data['life_expectancy']
#             )
#             """
#             linregress is used here to obtain information about the
#             linear regression between GDP and life expectancy.
#             Here:
#             x = np.log10(merged_data['gdp'])
#             y = merged_data['life_expectancy']
#             n = shape[1] (186: nb of countries with data in 1900)
#             linregress returns three key values among others:
#             - slope: the slope of the regression line.
#             slope = Cov(x,y)/Var(x)
#             Cov stands for covariance:
#             Cov(x,y) = (1/n) * sum[i=1 to n]((x_i-mean(x)) * (y_i-mean(y)))

#             Var for variance:
#             Var(x) = (1/n) * sum[i=1 to n]((x_i-mean(x))**2)
#             - intercept: the y-intercept of this line.
#             This can be represented as: slope * x + intercept (ax+b).
#             intercept = mean(y) - slope * mean(x)
#             - r_value: the Pearson correlation coefficient
#             between the two variables (GDP and life_expectancy).
#             - 1: perfect positive correlation.
#             - -1: perfect negative correlation.
#             - 0: no correlation.
#             r_value = cov(x,y)/sqrt(var(x)*var(y))

#             No explanation is provided here for p_value and std_err,
#             although they must be included for the unpacking of
#             the returned linregress tuple.

#             About the linear regression mathematical tool:
#             The idea is to find the linear formula ax+b for a line
#             as close as possible of every points.
#             """

#             gdp_sorted = np.sort(merged_data['gdp'])
#             predicted_life_expectancy = (
#                 slope * np.log10(gdp_sorted) + intercept
#             )
#             """
#             print(type(predicted_life_expectancy))  # <class 'numpy.ndarray'>
#             Now that slope and intercept are calculated,
#             it is possible to use them as a model:
#             applying them with the formula
#             slope * np.log10(gdp_sorted) + intercept
#             it provides an array of life expectancies predicted
#             by the model.
#             As it will plot, we need the array sorted
#             (whereas initially, order did not matter).
#             """

#             ax.plot(
#                 gdp_sorted,
#                 predicted_life_expectancy,
#                 color="red",
#                 linestyle="--",
#                 label="Regression Line (log-linear)"
#             )

#             # ===== Correlation displaying =====
#             ax.text(
#                 0.5, -0.2,
#                 f"Correlation: {r_value:.2f}",
#                 fontsize=12,
#                 color="red",
#                 ha='center',
#                 transform=plt.gca().transAxes,
#                 bbox=dict(
#                     facecolor='white',
#                     edgecolor='red',
#                     alpha=0.8,
#                     linestyle='--'
#                 )
#             )

#             fig.subplots_adjust(bottom=0.25)
#             """To make the correlation displaying visible."""

#         # ===== Chart and window title settings =====
#         title = f"Life Expectancy vs GDP per country in {YEAR}"
#         ax.set_title(title)
#         fig.canvas.manager.set_window_title(title)

#         ax.set_xscale('log')
#         ax.set_xlabel("Gross Domestic Product (USD, log scale)")
#         ticks = [300, 1000, 10000]
#         labels = ['300', '1k', '10k']
#         ax.set_xticks(ticks, labels)

#         ax.set_ylabel("Life Expectancy (years)")

#         ax.legend(loc="best")

#         # ===== Info tooltip cursor =====
#         if BONUS:
#             def put_kmb_suffix(val: int) -> str:
#                 """
#                 Formats a large number with 'k', 'M', or 'B' suffixes.
#                 """
#                 for threshold, suffix in [
#                     (1e9, 'B'), (1e6, 'M'), (1e3, 'k')
#                 ]:
#                     if val > threshold:
#                         return f"{val / threshold:.2f}{suffix}"
#                 return str(val)

#             cursor = mplcursors.cursor(scatter, hover=True)
#             """
#             print(type(cursor))  # <class 'mplcursors._mplcursors.Cursor'>
#             Creates an object linked to the scatter variable.
#             Further details just belows.
#             """

#             @cursor.connect("add")
#             def on_add(sel):
#                 """
#                 Handles the event triggered by hovering
#                 or selecting a point in the scatter plot.

#                 This function is called when the "add"
#                 event is triggered by mplcursors.
#                 It updates the annotation (tooltip) for the
#                 selected point to display the country name,
#                 with customized text and background styling.

#                 Args:
#                     sel (mplcursors.Selection):
#                         An object representing the selected point.
#                         Contains attributes such as:
#                         - `sel.index`:
#                             Index of the selected
#                             point in the underlying data.
#                         - `sel.annotation`:
#                             Annotation object for customizing the tooltip.

#                 Behavior:
#                     - Retrieves the country name from the `merged_data`
#                     DataFrame using `sel.index`.
#                     - Sets the annotation text to the country name.
#                     - Customizes the annotation's appearance
#                     (font, size, and background).
#                 """

#                 row = merged_data.iloc[sel.index]
#                 country = row["country"]
#                 life_expectancy = row["life_expectancy"]
#                 population = row["population"]
#                 gdp = row["gdp"]

#                 sel.annotation.set(
#                     text=(
#                         f"{country}\n"
#                         f"Life Expectancy: {life_expectancy} years\n"
#                         f"GDP per capita: {gdp}\n"
#                         f"Population: {put_kmb_suffix(population)}"
#                     ),
#                     fontsize=10, fontweight="bold")
#                 sel.annotation.get_bbox_patch().set(alpha=0.6, color="white")
#             """
#             cursor.connect("add", on_add)
#             Without the decorator above the on_add function,
#             this line would be used : exactly the same effet.

#             What is sel ?
#             mplcursors sends a Selection object (as defined in the library)
#             to the event manager function just below.

#             When the event add is launched
#             (by hovering a point with the mouse):
#             mplcursors gets the elements about the selected/hovered point,
#             and stores them into the Selection object, referred as sel.

#             sel.index :
#                 Allows to retrieve the data from the df.
#             sel.annotation :
#                 Automatically created by matplotlib for each point.
#                 Can be modified, as the on_add function does.
#             """

#         # ===== Final rendering =====
#         DEBUG_BEACON = 1
#         if DEBUG and DEBUG_BEACON:
#             print("### fig and ax content summary ###")
#             print(f"Size: {fig.get_size_inches()} inches")
#             print(f"Number of axes: {len(fig.axes)}")

#             print("\nAxes summary:")
#             print(f"Title: {ax.get_title()}")
#             print(f"X-label: {ax.get_xlabel()}")
#             print(f"Y-label: {ax.get_ylabel()}")
#             print(f"Number of children in Axes: {len(ax.get_children())}")

#             print("\nChildren of Axes:")
#             for child in ax.get_children():
#                 print(f"  - {type(child).__name__}: {child}")
#             print("### END fig and ax content summary ###")

#         plt.show()

#     except AssertionError as error:
#         print(f"{type(error).__name__}: {error}")
#     except Exception as error:
#         print(f"An unexpected error occurred: {error}")


# if __name__ == "__main__":
#     main()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@ poo.py @@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# """
# Long file here. Here are some tips:
# - It is highly recommanded to use a code editor which allows
# to fold/unfold functions/methods/classes/if/triple quoted docstrings.
# VSCode allows this feature with the little arrow between the line
# number and the beginning of the foldable line.
# Try with this triple quoted string!
# Global code blocks folding (available on VSCode):
# ctrl+K then ctrl+[indent level ; I suggest 2 for this file]

# After a ctr+clic on a function/method,
# navigate back with the keyboard short cut: ctrl alt -

# Enable or disable debugging:
# in the debug function,
# by switching on 0 or 1 the second condition in the if
# (if debug and 1:)

# Still to do:
# - readme
# - video
# - LinkedIn presentation
# """

# from functools import wraps
# from fuzzywuzzy import process
# import inspect
# from load_csv import load
# import matplotlib
# from matplotlib.animation import FuncAnimation
# from matplotlib.axes import Axes
# from matplotlib.figure import Figure
# from matplotlib.colorbar import Colorbar
# import matplotlib.collections as mplcollec
# from matplotlib.collections import PathCollection
# import matplotlib.pyplot as plt
# from matplotlib.cm import ScalarMappable
# from matplotlib.widgets import Slider, TextBox, Button
# from matplotlib.colors import Normalize, LinearSegmentedColormap
# import mplcursors
# import numpy as np
# import pandas as pd
# from scipy.stats import linregress
# from typing import Callable
# import typeguard

# if matplotlib.get_backend() != 'TkAgg':
#     matplotlib.use('TkAgg')


# def debug(
#     function_name: str,
#     debug: int,
#     step="START"
# ) -> None:
#     """
#     Prints debug information for a function,
#     including its name and the current step (if written).

#     Usage:
#         Copy the line below the if 0 into any function
#         for debugging.
#         No need to write on your own the function name.
#         You also can specify a STEP about the function/method
#         instructions.

#     Parameters:
#         function_name (str):
#             The name of the function to debug.
#         debug (int):
#             The debug level. If non-zero, the debug information is printed.
#         step (str):
#             The current step in the function's execution
#             (e.g., "START" or "END").
#     """

#     if 0:  # Do not switch to 1.
#         debug(inspect.currentframe().f_code.co_name, 1)  # copy this line

#     if debug and 1:
#         print(f"DEBUG: {step} current function -> {function_name}")


# def debug_decorator(func: Callable) -> Callable:
#     """
#     A decorator to print debug information
#     before and after a function's execution.

#     Parameters:
#         func (Callable): The function to wrap with debug logging.

#     Usage:
#         Copy that:
#             @debug_decorator
#         above a function/method definition.

#     Returns:
#         Callable: The wrapped function with debug logging enabled.
#     """

#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         function_name = func.__name__
#         debug_level = 1
#         if debug_level:
#             print(f"DEBUG: START current function -> {function_name}")
#         result = func(*args, **kwargs)
#         if debug_level:
#             print(f"DEBUG: END current function -> {function_name}")
#         return result
#     return wrapper


# def timediv_test_value():
#     """
#     As we were told not to use any global variable,
#     here is this "function" useful for debug.
#     """

#     return 1800


# def target_test_value():
#     """
#     As we were told not to use any global variable,
#     here is this "function" useful for debug.
#     """

#     return "Norway"


# def cust_suffixed_string_to_float(value) -> float:
#     """
#     Converts a string with custom suffixes (k, M, B) to a float.

#     Parameters:
#         value (str or numeric):
#         The input value to convert.
#         Strings can have suffixes 'k', 'M', or 'B'.

#     Returns:
#         float: The numeric value after conversion,
#         or NaN if conversion fails.
#     """

#     factors = {'k': 1e3, 'M': 1e6, 'B': 1e9}
#     try:
#         if isinstance(value, str) and value[-1] in factors:
#             return float(value[:-1]) * factors[value[-1]]
#         return float(value)
#     except (ValueError, TypeError):
#         return np.nan


# def dict_printer(
#     d: dict,
#     values_type: str,
#     head_value: int = 5
# ) -> None:
#     """
#     Prints the contents of a dictionary based on the type of its values.

#     Parameters:
#         d (dict):
#             The dictionary to print.
#         values_type (str):
#             The expected type of the dictionary's values
#             ("pd.DataFrame", "cust class", or others).
#         head_value (int):
#             For DataFrame values, the number of rows to display.
#             Must be greater than 0.
#     """

#     if d is None:
#         print("The dictionnary does not exist.")
#         return None

#     if values_type == "pd.DataFrame":
#         if head_value < 1:
#             print("head_value must be greater than 0.")
#             return None
#         for key, value in d.items():
#             if value is not None:
#                 print(f"{key}:\n{value}\n")

#     elif values_type == "cust class":
#         for _, value in d.items():
#             if value is not None:
#                 value.show()

#     else:
#         for key, value in d.items():
#             print(f"{key}: {value}")


# def get_data_name(file_name: str) -> str:
#     """
#     Extracts the base name from a file path,
#     removing the extension and replacing underscores with spaces.

#     Parameters:
#         file_name (str): The full file path or name.

#     Returns:
#         str: The extracted base name with spaces instead of underscores.
#     """

#     extension = file_name[file_name.index('.'):]
#     return file_name[:file_name.index(extension)].replace('_', ' ')


# def put_kmb_suffix(val: float) -> str:
#     """
#     Converts a numeric value to a string with
#     'k', 'M', or 'B' suffix for thousands, millions, or billions.

#     Parameters:
#         val (float): The numeric value to convert.

#     Returns:
#         str: The formatted string with an appropriate suffix,
#         or the original number as a string if below 1,000.
#     """

#     for threshold, suffix in [
#         (1e9, 'B'), (1e6, 'M'), (1e3, 'k')
#     ]:
#         if val > threshold:
#             return f"{val / threshold:.2f}{suffix}"
#     return str(val)


# def var_print_str(
#     var_name: str,
#     var_value
# ) -> str:
#     """
#     Formats a variable's name and value as a string, including its type.

#     Parameters:
#         var_name (str): The name of the variable.
#         var_value (Any): The value of the variable.

#     Returns:
#         str:
#             A string representation of
#             the variable's name, value, and type.
#     """

#     return f"{var_name}:{var_value} ({type(var_value)})\n"


# class LinReg:
#     """
#     Represents the results of a linear regression analysis.

#     Attributes:
#         corr (float):
#             The correlation coefficient of the regression.
#         predicted (np.ndarray):
#             The predicted values resulting from the regression.
#         pvalue (float):
#             The p-value indicating the significance of the correlation.
#     """

#     def __init__(self,
#                  predicted: np.ndarray,
#                  corr: float,
#                  pvalue: float):
#         """
#         Initializes a LinReg object with regression results.

#         Parameters:
#             corr (float):
#                 The correlation coefficient of the regression.
#             predicted (np.ndarray):
#                 The predicted values from the regression model.
#             pvalue (float):
#                 The p-value indicating the significance of the regression.
#         """

#         self.predicted: np.ndarray = predicted
#         self.corr: float = corr
#         self.pvalue: float = pvalue

#     def show(self) -> None:
#         """The class show method for a LinReg class object"""

#         print("\n=== SHOW LinReg class object (START) ===")

#         print(f"Correlation Coefficient (corr): {self.corr:.4f}")
#         print(f"P-Value (pvalue): {self.pvalue:.4e}")

#         print("\nPredicted Values (predicted):")
#         print(self.predicted)

#         print("\n=== SHOW LinReg class object (END) ===")


# class DataFrame:
#     """
#     Represents a data structure to handle and process
#     CSV or other tabular data.

#     Attributes:
#         data_cleaned (bool):
#             Indicates if the data has been cleaned.
#         data_frame (pd.DataFrame):
#             The loaded pandas DataFrame containing the data.
#         data_name (str):
#             The name of the data derived from the file path.
#         data_type (str):
#             The type of data (e.g., 'numerical', 'categorical').
#         file_path (str):
#             The path to the file containing the data.
#         first_column_name (int | float | None):
#             The name of the first data column (used for time ranges).
#         last_column_name (int | float | None):
#             The name of the last data column (used for time ranges).
#         short_name (str):
#             A shorter, descriptive name for the data.
#     """

#     def __init__(
#         self,
#         data_type: str,
#         file_path: str,
#         short_name: str,
#     ):
#         """
#         Initializes a DataFrame object
#         and loads data from the provided file.

#         Parameters:
#             data_type (str):
#                 The type of data (e.g., 'numerical', 'categorical').
#             file_path (str):
#                 The path to the file containing the data.
#             short_name (str):
#                 A shorter, descriptive name for the data.

#         Raises:
#             ValueError: If any parameter is not a string.
#         """

#         if all(
#             isinstance(arg, str) for arg in (
#                 data_type,
#                 file_path,
#                 short_name)
#         ):
#             self.data_type: str = data_type
#             self.file_path: str = file_path
#             self.data_name: str = get_data_name(file_path)
#             self.short_name: str = short_name
#             self.data_frame: pd.DataFrame = load(file_path)
#         else:
#             raise ValueError(
#                 f"Both data_type and data_type must be str, not:\n"
#                 f"{var_print_str('data_type', data_type)}\n"
#                 f"{var_print_str('file_path', file_path)}"
#             )

#         self.first_column_name: int | float | None = None
#         self.last_column_name: int | float | None = None
#         self.data_cleaned: bool = False

#     def show(self) -> None:
#         """The class show method for a DataFrame class object"""

#         print("\n=== SHOW DataFrame class object (START) ===")

#         print("\n--- General Information ---")
#         print(f"Data Type: {self.data_type}")
#         print(f"File Path: {self.file_path}")
#         print(f"Data Name: {self.data_name}")
#         print(f"Short Name: {self.short_name}")

#         print("\n--- Column Information ---")
#         print(f"First Column Name: {self.first_column_name}")
#         print(f"Last Column Name: {self.last_column_name}")

#         print("\n--- Data Cleaning Status ---")
#         print(f"Data Cleaned: {self.data_cleaned}")

#         print("\n--- DataFrame Content ---")
#         print(self.data_frame)

#         print("\n=== SHOW DataFrame class object (END) ===")

#     class DataFrameException(Exception):
#         """
#         A base exception class for errors related to the DataFrame class.
#         """
#         pass

#     class DataFrameNotCleanedException(DataFrameException):
#         """
#         Exception raised when an operation requiring
#         a cleaned DataFrame is attempted.

#         Attributes:
#             msg (str): A descriptive message about the error.
#         """

#         def __init__(
#             self,
#             msg="DataFrame object still not cleaned.\n"
#                 "This exception appears because something has been"
#                 " attempted which needs the DataFrame to be cleaned"
#                 " before."
#         ):
#             """DOCSTRING"""

#             super().__init__(msg)

#     def get_first_last_column_names(self) -> None:
#         """
#         Extracts and sets the first and last
#         column names as integer or float values.
#         """

#         self.first_column_name = int(self.data_frame.columns[1])
#         self.last_column_name = int(self.data_frame.columns[-1])

#     def subset_timediv_extraction(
#         self,
#         timediv: int,
#         common_column: str
#     ) -> pd.DataFrame | None:
#         """
#         Extracts a subset of the DataFrame for a specific time division.

#         Parameters:
#             timediv (int):
#                 The time division (year or other) to extract.
#             common_column (str):
#                 The name of the common column (e.g., 'country').

#         Returns:
#             pd.DataFrame | None:
#                 A subset DataFrame with the time division and common column,
#                 or None if the time division is not within the valid range.
#         """

#         if (
#             timediv in range(
#                 self.first_column_name, self.last_column_name + 1
#             )
#         ):
#             df_timediv = self.data_frame[
#                     [common_column, str(timediv)]
#                 ].rename(columns={str(timediv): self.data_name})
#             df_timediv[self.data_name] = df_timediv[self.data_name].apply(
#                 cust_suffixed_string_to_float
#             )

#             return df_timediv

#         return None


# class TimeDiv:
#     """
#     Represents a specific time division for
#     data processing, merging, and analysis.

#     Attributes:
#         common_column (str):
#             The column common across all DataFrames,
#             used for merging (e.g., 'country').
#         df_dict (dict[str, pd.DataFrame]):
#             Dictionary containing the individual DataFrames
#             for data_x, data_y, etc.
#         div (int):
#             The specific division of time
#             (e.g., a year) this instance represents.
#         lin_reg_lin (LinReg | None):
#             Linear regression results for the linear scale.
#         lin_reg_log (LinReg | None):
#             Linear regression results for the logarithmic scale.
#         merged_data (pd.DataFrame | None):
#             The merged DataFrame combining all relevant data.
#     """

#     def __init__(
#         self,
#         timediv_list: list[pd.DataFrame],
#         common_column: str,
#         div: int
#     ):
#         """
#         Initializes a TimeDiv object.

#         Parameters:
#             timediv_list (list[pd.DataFrame]):
#                 A list of DataFrames for data_x, data_y, data_point_size,
#                 extra_data_x, and extra_data_y.
#             common_column (str):
#                 The column common to all DataFrames,
#                 used for merging (e.g., 'country').
#             div (int):
#                 The specific division of time (e.g., a year)
#                 this instance represents.
#         """

#         self.df_dict: dict[str, pd.DataFrame] = {
#             "data_x": timediv_list[0],
#             "data_y": timediv_list[1],
#             "data_point_size": timediv_list[2],
#             "extra_data_x": timediv_list[3],
#             "extra_data_y": timediv_list[4]
#         }
#         self.common_column: str = common_column
#         self.div: int = div

#         self.merged_data: pd.DataFrame | None = None
#         self.lin_reg_log: LinReg | None = None
#         self.lin_reg_lin: LinReg | None = None

#     def show(
#         self,
#         head_value: int = 5
#     ) -> None:
#         """The class show method for a TimeDiv class object"""

#         print("\n=== SHOW TimeDiv class object (START) ===")

#         print("\n--- General Information ---")
#         print(f"Time Division: {self.div}")
#         print(f"Common Column: {self.common_column}")

#         print("\n--- DataFrames Dictionary (df_dict) ---")
#         for key, df in self.df_dict.items():
#             print(f"{key}:")
#             if df is not None:
#                 print(df.head(head_value))
#             else:
#                 print("None")

#         print("\n--- Merged Data ---")
#         if self.merged_data is not None:
#             print(self.merged_data.head(head_value))
#         else:
#             print("No merged data available.")

#         print("\n--- Linear Regression Results ---")
#         if self.lin_reg_log:
#             print("\nLogarithmic Scale Regression:")
#             self.lin_reg_log.show()
#         else:
#             print("No logarithmic regression available.")

#         if self.lin_reg_lin:
#             print("\nLinear Scale Regression:")
#             self.lin_reg_lin.show()
#         else:
#             print("No linear regression available.")

#         print("\n=== SHOW TimeDiv class object (END) ===")

#     def merge(self) -> None:
#         """
#         Crucial step for this program, then long detailed docstring:

#         Merges the DataFrames in `df_dict` into
#         a single unified DataFrame (`merged_data`),
#         retaining only rows with complete data across
#         all required DataFrames.

#         Steps:
#         1. **Validation**:
#             Ensures that essential DataFrames
#             (`data_x`, `data_y`, and `data_point_size`)
#             exist in `df_dict`.
#             Raises a `ValueError` if any of them is missing.

#         2. **Index Alignment**:
#             Temporarily sets the `common_column` as the index
#             for key DataFrames to align data rows consistently.

#         3. **Filtering**:
#             Creates a mask to identify rows where all
#             essential DataFrames contain valid (non-null) data,
#             and applies this mask to filter out incomplete rows.

#         4. **Data Merging**:
#             Iteratively merges `data_x` with
#             other DataFrames (`data_y`, `data_point_size`,
#             `extra_data_x`, `extra_data_y`) based on the `common_column`,
#             using an inner join to retain only
#             rows present in all included DataFrames.

#         5. **Final Output**:
#             Resets the index of the merged DataFrame for
#             a clean result, ready for analysis.

#         The resulting `merged_data` contains only rows with consistent,
#         valid entries across the relevant DataFrames,
#         ensuring high-quality data for further processing.

#         Raises:
#             ValueError:
#                 If any of the required DataFrames
#                 (`data_x`, `data_y`, `data_point_size`) is missing.
#         """

#         for key in ['data_x', 'data_y', 'data_point_size']:
#             if self.df_dict[key] is None:
#                 raise ValueError(f"Essential DataFrame '{key}' is missing.")

#         for key in ['data_x', 'data_y', 'data_point_size']:
#             self.df_dict[key] = self.df_dict[key].set_index(
#                 self.common_column
#             )

#         mask = (
#             ~self.df_dict['data_x'].iloc[:, 0].isna() &
#             ~self.df_dict['data_y'].iloc[:, 0].isna() &
#             ~self.df_dict['data_point_size'].iloc[:, 0].isna()
#         )

#         for key in ['data_x', 'data_y', 'data_point_size']:
#             self.df_dict[key] = self.df_dict[key].loc[
#                 mask.reindex(self.df_dict[key].index, fill_value=False)
#                 ].reset_index()

#         self.merged_data = self.df_dict['data_x']
#         for key in [
#             'data_y',
#             'data_point_size',
#             'extra_data_x',
#             'extra_data_y'
#         ]:
#             if self.df_dict[key] is not None:
#                 self.merged_data = pd.merge(
#                     self.merged_data,
#                     self.df_dict[key],
#                     on=self.common_column,
#                     how='inner'
#                 )

#         self.merged_data.reset_index(drop=True, inplace=True)

#     def harmonize_for_regression(self) -> tuple[np.ndarray]:
#         """
#         Extracts and returns the x and y values
#         from `merged_data` as numpy arrays.

#         Returns:
#             tuple[np.ndarray]:
#                 A tuple with x-axis (independent)
#                 and y-axis (dependent) values.

#         Raises:
#             ValueError:
#                 If `merged_data` is None,
#                 meaning `merge` has not been called.
#         """

#         if self.merged_data is None:
#             raise ValueError(
#                 "Merged data is not available. Did you call `merge()`?"
#             )

#         return (
#             self.merged_data.iloc[:, 1].to_numpy(),
#             self.merged_data.iloc[:, 2].to_numpy()
#         )

#     def calculate_linregr(
#             self,
#             log: bool
#     ) -> LinReg:
#         """
#         Performs linear regression on x and y data,
#         with an optional logarithmic transformation on x.

#         Args:
#             log (bool):
#                 If True, applies a base-10 logarithmic
#                 transformation to x-axis values.

#         Returns:
#             LinReg:
#                 The regression result,
#                 including predicted values, correlation, and p-value.
#         """

#         data_x, data_y = self.harmonize_for_regression()

#         if log:
#             data_x = np.log10(data_x)

#         slope, intercept, corr, pvalue, _ = linregress(data_x, data_y)
#         data_x_sorted = np.sort(data_x)
#         predicted = slope * data_x_sorted + intercept

#         return LinReg(predicted, corr, pvalue)

#     def linear_regressions(self) -> None:
#         """
#         Computes and stores both logarithmic and
#         linear regressions for the data.

#         Saves the results in `lin_reg_log` and `lin_reg_lin`.
#         """

#         self.lin_reg_log = self.calculate_linregr(log=True)
#         self.lin_reg_lin = self.calculate_linregr(log=False)


# class Day02Ex03:
#     """
#     Main class to manage data visualization for Day02 Exercise 03.

#     Attributes:
#         anim (FuncAnimation | None):
#             Animation instance for the visual updates.
#         ax_box_tracker (Axes | None):
#             Axes object for the text box tracker.
#         axes (dict[str, Axes] | None):
#             Dictionary of Axes for different plots.
#         cbar (Colorbar | None):
#             Colorbar instance for the scatter plot.
#         cmap_colors (list[str]):
#             Colors used for the colormap.
#         common_column (str | None):
#             Common column name shared across datasets.
#         corr_log (list | np.ndarray):
#             Correlation coefficients for logarithmic scale.
#         corr_lin (list | np.ndarray):
#             Correlation coefficients for linear scale.
#         correlation_cursor_container
#         (dict[str, mplcursors.cursor.Cursor | None]):
#             Cursors for interactive correlation plots.
#         current_frame (int | None):
#             Current frame value during animation.
#         cursor_container (dict[str, mplcursors.cursor.Cursor | None]):
#             Cursors for the main scatter plots.
#         data_frames (dict[str, pd.DataFrame | None]):
#             Dictionary storing loaded data.
#         data_point_size_divider (int):
#             Divider used to scale point sizes in scatter plots.
#         fig (Figure | None):
#             Matplotlib figure instance.
#         first_running (bool):
#             Indicates whether the animation is running for the first time.
#         init_value (int | None):
#             Initial value for the slider.
#         pause_ax (Axes | None):
#             Axes object for the pause button.
#         pause_button (Button | None):
#             Button widget for pausing the animation.
#         play_ax (Axes | None):
#             Axes object for the play button.
#         play_button (Button | None):
#             Button widget for starting the animation.
#         precomputed_data (dict[int | float, TimeDiv]):
#             Precomputed data for each time division.
#         pvalue_log (list | np.ndarray):
#             P-values for logarithmic regression.
#         pvalue_lin (list | np.ndarray):
#             P-values for linear regression.
#         running_mode (bool):
#             Indicates if the animation is running.
#         slider (Slider | None):
#             Slider widget for selecting time divisions.
#         slider_title_text (str | None):
#             Title text for the slider.
#         timediv_range (range | None):
#             Range of time divisions available in the data.
#         text_box_tracker (TextBox | None):
#             Text box for tracking user input.
#         timediv_type (str | None):
#             Type of time division (e.g., "year").
#         title (str | None):
#             Title of the visualization.
#         tracked_element (str):
#             Name of the tracked element in the visualization.
#         x_label (str | None):
#             Label for the x-axis.
#         x_unit (str | None):
#             Unit for the x-axis.
#         y_label (str | None):
#             Label for the y-axis.
#         y_unit (str | None):
#             Unit for the y-axis.
#         colored_extra_data (str):
#             Name of the extra data column used for coloring points.
#     """

#     def __init__(self):
#         """Initializes the Day02Ex03 object with default values."""

#         self.anim: FuncAnimation | None = None
#         self.ax_box_tracker: Axes | None = None
#         self.axes: dict[str, Axes] | None = None
#         self.cbar: Colorbar | None = None
#         self.cmap_colors: list[str] = [
#             "green",
#             "limegreen",
#             "yellow",
#             "orange",
#             "red",
#             "magenta",
#             "mediumpurple",
#             "darkviolet"
#         ]
#         self.common_column: str | None = None
#         self.corr_log: list | np.ndarray = []
#         self.corr_lin: list | np.ndarray = []
#         self.correlation_cursor_container: dict[
#             str, mplcursors.cursor.Cursor | None
#         ] = {
#             "corr_log": None,
#             "pvalue_log": None,
#             "corr_lin": None,
#             "pvalue_lin": None,
#         }
#         self.current_frame: int | None = None
#         self.cursor_container: dict[
#             str, mplcursors.cursor.Cursor | None
#             ] = {
#             "log": None,
#             "lin": None
#         }
#         self.data_frames: dict[str, pd.DataFrame | None] = {
#             "data_x": None,
#             "data_y": None,
#             "data_point_size": None,
#             "extra_data_x": None,
#             "extra_data_y": None,
#         }
#         self.data_point_size_divider: int = None
#         self.fig: Figure | None = None
#         self.first_running: bool = False
#         self.init_value: int | None = None
#         self.interval_between_two_frames: int = 100
#         self.pause_ax: Axes | None = None
#         self.pause_button: Button | None = None
#         self.play_ax: Axes | None = None
#         self.play_button: Button | None = None
#         self.precomputed_data: dict[int | float, TimeDiv] = {}
#         self.pvalue_log: list | np.ndarray = []
#         self.pvalue_lin: list | np.ndarray = []
#         self.running_mode: bool = False
#         self.slider: Slider | None = None
#         self.slider_title_text: str | None = None
#         self.timediv_range: range | None = None
#         self.text_box_tracker: TextBox | None = None
#         self.timediv_type: str | None = None
#         self.title: str | None = None
#         self.tracked_element: str = "None"
#         self.x_label: str | None = None
#         self.x_unit: str | None = None
#         self.y_label: str | None = None
#         self.y_unit: str | None = None

#         # definetly set that way (adjustable in future versions)
#         self.colored_extra_data: str = "extra_data_x"

#     def show(self):
#         """The class show method for a Day02Ex03 class object"""

#         print("\n=== SHOW Day02Ex03 object (START) ===")

#         print("\n--- General Settings ---")
#         print(f"Title: {self.title}")
#         print(f"Timediv Range: {self.timediv_range}")
#         print(f"Timediv Type: {self.timediv_type}")
#         print(f"Initial Value: {self.init_value}")
#         print(f"Running Mode: {self.running_mode}")
#         print(f"First Running: {self.first_running}")

#         print("\n--- Labels and Units ---")
#         print(f"X Label: {self.x_label}")
#         print(f"X Unit: {self.x_unit}")
#         print(f"Y Label: {self.y_label}")
#         print(f"Y Unit: {self.y_unit}")

#         print("\n--- Correlation and P-Values ---")
#         print(f"Correlation (Log): {self.corr_log}")
#         print(f"P-Values (Log): {self.pvalue_log}")
#         print(f"Correlation (Lin): {self.corr_lin}")
#         print(f"P-Values (Lin): {self.pvalue_lin}")

#         print("\n--- Tracking ---")
#         print(f"Tracked Element: {self.tracked_element}")

#         print("\n--- Data Frames ---")
#         dict_printer(self.data_frames, values_type="cust class")

#         print("\n--- Color Map and Color Bar ---")
#         print(f"Color Map Colors: {self.cmap_colors}")
#         print(f"Colored Extra Data: {self.colored_extra_data}")
#         print(f"Color Bar: {self.cbar}")

#         print("\n--- Interactive Elements ---")
#         print(f"Slider: {self.slider}")
#         print(f"Slider Title Text: {self.slider_title_text}")
#         print(f"Play Button: {self.play_button}")
#         print(f"Pause Button: {self.pause_button}")
#         print(f"Tracker Text Box: {self.text_box_tracker}")

#         print("\n--- Axes and Figures ---")
#         print(f"Figure: {self.fig}")
#         print(f"Axes: {self.axes}")

#         print("\n=== SHOW Day02Ex03 object (END) ===\n")

#     def add_data_path(
#         self,
#         data_path: str,
#         data_type: str,
#         short_name: str
#     ) -> None:
#         """
#         Adds a data path to the data_frames dictionary.

#         Args:
#             data_path (str):
#                 Path to the dataset file.
#             data_type (str):
#                 Type of the data (e.g., "data_x", "data_y").
#             short_name (str):
#                 Shortened name for the dataset.

#         Raises:
#             ValueError:
#                 If any argument is not a valid string or
#                 `data_path` is too short.
#         """

#         if (
#             all(
#                 isinstance(arg, str) for arg in (
#                 data_path,
#                 data_type,
#                 short_name
#                 )
#             )
#             and len(data_path) >= 3
#         ):
#             self.data_frames[data_type] = DataFrame(
#                 data_type,
#                 data_path,
#                 short_name
#             )
#         else:
#             raise ValueError(
#                 f"data_path (min length 3),"
#                 f"data_type and short_name must be str, not:\n"
#                 f"{var_print_str('data_path', data_path)}\n"
#                 f"{var_print_str('data_type', data_type)}\n"
#                 f"{var_print_str('data_type', short_name)}"
#             )

#     @typeguard.typechecked
#     def add_data_x_path(
#         self,
#         data_x_path: str,
#         short_name: str,
#         x_label: str,
#         x_unit: str
#     ) -> None:
#         """
#         Adds the X-axis dataset and related metadata.

#         Args:
#             data_x_path (str):
#                 File path for the X-axis dataset.
#             short_name (str):
#                 Abbreviated name for the dataset, used in legends or labels.
#             x_label (str):
#                 Label for the X-axis.
#             x_unit (str):
#                 Unit associated with the X-axis values.
#         """

#         self.add_data_path(
#             data_x_path,
#             "data_x",
#             short_name
#         )
#         self.x_label = x_label
#         self.x_unit = x_unit

#     @typeguard.typechecked
#     def add_data_y_path(
#         self,
#         data_y_path: str,
#         short_name: str,
#         y_label: str,
#         y_unit: str
#     ) -> None:
#         """
#         Adds the Y-axis dataset and related metadata.

#         Args:
#             data_y_path (str):
#                 File path for the Y-axis dataset.
#             short_name (str):
#                 Abbreviated name for the dataset, used in legends or labels.
#             y_label (str):
#                 Label for the Y-axis.
#             y_unit (str):
#                 Unit associated with the Y-axis values.
#         """

#         self.add_data_path(
#             data_y_path,
#             "data_y",
#             short_name
#         )
#         self.y_label = y_label
#         self.y_unit = y_unit

#     @typeguard.typechecked
#     def add_data_point_size_path(
#         self,
#         data_point_size_path: str,
#         short_name: str,
#         divider: int | float
#     ) -> None:
#         """
#         Adds the dataset for determining the size of scatter plot points.

#         Args:
#             data_point_size_path (str):
#                 File path for the dataset controlling point sizes.
#             short_name (str):
#                 Abbreviated name for the dataset, used in legends or labels.
#             divider (int | float):
#                 Scaling factor to adjust the point sizes.
#         """

#         self.data_point_size_divider = divider
#         self.add_data_path(
#             data_point_size_path,
#             "data_point_size",
#             short_name
#         )

#     @typeguard.typechecked
#     def add_extra_data_x_path(
#         self,
#         extra_data_x_path: str,
#         short_name: str
#     ) -> None:
#         """
#         Adds an additional dataset related to
#         the X-axis for coloring or metadata.

#         Args:
#             extra_data_x_path (str):
#                 File path for the additional X-axis dataset.
#             short_name (str):
#                 Abbreviated name for the dataset, used in legends or labels.
#         """

#         self.add_data_path(
#             extra_data_x_path,
#             "extra_data_x",
#             short_name
#         )

#     @typeguard.typechecked
#     def add_extra_data_y_path(
#         self,
#         extra_data_y_path: str,
#         short_name: str
#     ) -> None:
#         """
#         Adds an additional dataset related to
#         the Y-axis for coloring or metadata.

#         Args:
#             extra_data_y_path (str):
#                 File path for the additional Y-axis dataset.
#             short_name (str):
#                 Abbreviated name for the dataset, used in legends or labels.
#         """

#         self.add_data_path(
#             extra_data_y_path,
#             "extra_data_y",
#             short_name
#         )

#     @typeguard.typechecked
#     def add_title(
#         self,
#         title: str
#     ) -> None:
#         """
#         Sets the title for the visualization.

#         Args:
#             title (str): The title of the visualization.
#         """

#         self.title = title

#     @typeguard.typechecked
#     def add_timediv_range(
#         self,
#         start: int,
#         stop: int,
#         init_value: int,
#         type: str
#     ) -> None:
#         """
#         Defines the range of time divisions for the visualization.

#         Args:
#             start (int):
#                 Starting value for the time division.
#             stop (int):
#                 Ending value for the time division.
#             init_value (int):
#                 Initial time division to be displayed.
#             type (str):
#                 Label for the type of time division (e.g., "year").
#         """

#         self.timediv_range = range(start, stop + 1)
#         self.timediv_type = type
#         self.init_value = init_value
#         self.current_frame = init_value

#     @typeguard.typechecked
#     def add_common_column(
#         self,
#         common_column: str
#     ) -> None:
#         """
#         Sets the common column name shared across datasets.

#         Args:
#             common_column (str):
#                 Column name that links datasets together.
#         """

#         self.common_column = common_column

#     @typeguard.typechecked
#     def set_autoplay_at_start(
#         self,
#         autoplay_at_start: bool
#     ) -> None:
#         """
#         Configures whether the animation starts automatically.

#         Args:
#             autoplay_at_start (bool):
#                 True to start the animation automatically; False otherwise.
#         """

#         self.first_running = autoplay_at_start

#     def clean_data_x(self) -> None:
#         """
#         Cleans the DataFrame associated with `data_x`.

#         - Sorts the DataFrame by the `common_column`.
#         - Resets the index to ensure a clean sequential order.
#         - Marks the DataFrame as cleaned.

#         Raises:
#             ValueError: If `data_x` is not properly initialized.
#         """

#         df = self.data_frames['data_x']
#         if df is not None:
#             df.data_frame.sort_values(
#                 by=self.common_column
#                 ).reset_index(drop=True)
#             df.data_cleaned = True

#     def clean_data_y(self) -> None:
#         """
#         Cleans the DataFrame associated with `data_y`.

#         - Sorts the DataFrame by the `common_column`.
#         - Resets the index to ensure a clean sequential order.
#         - Marks the DataFrame as cleaned.

#         Raises:
#             ValueError: If `data_y` is not properly initialized.
#         """

#         df = self.data_frames['data_y']
#         if df is not None:
#             df.data_frame.sort_values(
#                 by=self.common_column
#                 ).reset_index(drop=True)
#             df.data_cleaned = True

#     def clean_data_point_size(self) -> None:
#         """
#         Cleans the DataFrame associated with `data_point_size`.

#         - Sorts the DataFrame by the `common_column`.
#         - Resets the index to ensure a clean sequential order.
#         - Marks the DataFrame as cleaned.

#         Raises:
#             ValueError: If `data_point_size` is not properly initialized.
#         """

#         df = self.data_frames['data_point_size']
#         if df is not None:
#             df.data_frame.sort_values(
#                 by=self.common_column
#                 ).reset_index(drop=True)
#             df.data_cleaned = True

#     def clean_extra_data_x(self) -> None:
#         """
#         Cleans the DataFrame associated with `extra_data_x`.

#         - Removes irrelevant columns such as
#         'Country Code', 'Indicator Name',
#         'Indicator Code', and 'Unnamed: 68'.
#         - Renames the 'Country Name' column to match `common_column`.
#         - Matches country names in `extra_data_x` with those in `data_x`,
#         using fuzzy matching to align similar names.
#         - Drops rows with unmatched or duplicate entries in `common_column`.
#         - Sorts the DataFrame by `common_column`.
#         - Marks the DataFrame as cleaned.

#         Raises:
#             ValueError: If `extra_data_x` is not properly initialized.

#         Notes:
#             - A match is considered valid if the similarity score is >= 80.
#         """

#         if self.data_frames['extra_data_x'] is not None:
#             df = self.data_frames['extra_data_x'].data_frame
#             df = df.drop(
#                 columns=[
#                     "Country Code",
#                     "Indicator Name",
#                     "Indicator Code",
#                     "Unnamed: 68"
#                 ],
#                 errors="ignore"
#             )
#             df = df.rename(
#                 columns={"Country Name": self.common_column}
#             )

#             data_y_countries = self.data_frames[
#                 'data_x'
#                 ].data_frame[self.common_column].unique()

#             def match_country_name(country):
#                 """DOCSTRING"""

#                 match, score = process.extractOne(country, data_y_countries)
#                 return match if score >= 80 else None

#             df[self.common_column] = df[self.common_column].apply(
#                 match_country_name
#             )

#             df = df.dropna(subset=[self.common_column])
#             df = df.drop_duplicates(
#                 subset=[self.common_column],
#                 keep="first"
#             )
#             df = df.sort_values(
#                 by=self.common_column).reset_index(drop=True)

#             self.data_frames['extra_data_x'].data_frame = df
#             self.data_frames['extra_data_x'].data_cleaned = True

#     def clean_extra_data_y(self) -> None:
#         """
#         Marks the DataFrame associated with `extra_data_y` as cleaned.

#         - Simply sets the `data_cleaned` attribute to True, as no
#         specific cleaning steps are defined for this DataFrame so far.

#         Raises:
#             ValueError: If `extra_data_y` is not properly initialized.
#         """

#         if self.data_frames['extra_data_y'] is not None:
#             self.data_frames['extra_data_y'].data_cleaned = True

#     def clean_data_frames(self) -> None:
#         """
#         Cleans all associated DataFrames in the `data_frames` attribute.

#         - Sequentially calls individual cleaning methods:
#             - `clean_data_x`
#             - `clean_data_y`
#             - `clean_data_point_size`
#             - `clean_extra_data_x`
#             - `clean_extra_data_y`

#         Raises:
#             ValueError:
#                 If any DataFrame is missing or improperly initialized.
#         """

#         self.clean_data_x()
#         self.clean_data_y()
#         self.clean_data_point_size()
#         self.clean_extra_data_x()
#         self.clean_extra_data_y()

#     def get_first_last_column_names(self) -> None:
#         """
#         Retrieves and stores the first and
#         last column names for each DataFrame.

#         - Iterates over all DataFrames in `data_frames`.
#         - Checks if each DataFrame has been cleaned before proceeding.
#         - Calls the `get_first_last_column_names` method for each DataFrame.

#         Raises:
#             DataFrameNotCleanedException: If any DataFrame is not cleaned
#             before this operation.
#         """

#         for key, data_frame in self.data_frames.items():
#             if data_frame is None:
#                 continue
#             if not data_frame.data_cleaned:
#                 raise data_frame.DataFrameNotCleanedException(
#                     f"The DataFrame '{key}' has not been cleaned."
#                 )
#             data_frame.get_first_last_column_names()

#     def subsets_timediv_extraction(
#         self,
#         timediv: int,
#     ) -> list[pd.DataFrame]:
#         """
#         Extracts subsets of data for a given
#         time division across all DataFrames.

#         Args:
#             timediv (int):
#                 The time division for which data should be extracted.

#         Returns:
#             list[pd.DataFrame]:
#                 A list of DataFrames, one for each entry in `data_frames`.
#                 If a DataFrame is `None`,
#                 its corresponding subset will also be `None`.
#         """

#         res = list()
#         for df in self.data_frames.values():
#             if df is not None:
#                 res.append(
#                     df.subset_timediv_extraction(
#                         timediv,
#                         self.common_column
#                     )
#                 )
#             else:
#                 res.append(None)

#         return res

#     def precompute_data(self):
#         """
#         Precomputes and stores data for all time divisions.

#         Extracts subsets for each time division.
#         Merges the subsets into a single DataFrame for each division.
#         Calculates linear regressions for both logarithmic and linear scales.
#         Fills attributes for correlation coefficients and p-values over time.

#         Raises:
#             ValueError:
#                 If the data is not properly cleaned or initialized.
#         """

#         self.get_first_last_column_names()

#         for div in self.timediv_range:
#             timediv = TimeDiv(
#                 self.subsets_timediv_extraction(div),
#                 self.common_column,
#                 div
#             )
#             timediv.merge()
#             timediv.linear_regressions()

#             self.precomputed_data[div] = timediv
#             self.corr_log.append(timediv.lin_reg_log.corr)
#             self.pvalue_log.append(timediv.lin_reg_log.pvalue)
#             self.corr_lin.append(timediv.lin_reg_lin.corr)
#             self.pvalue_lin.append(timediv.lin_reg_lin.pvalue)

#         self.corr_log = np.array(self.corr_log)
#         self.pvalue_log = np.array(self.pvalue_log)
#         self.corr_lin = np.array(self.corr_lin)
#         self.pvalue_lin = np.array(self.pvalue_lin)

#     def build_fig_axes(self) -> None:
#         """
#         Sets up the main figure and axes for visualization.

#         - Creates a mosaic layout with two scatter plots (log and linear)
#         and two correlation graphs.
#         - Adjusts spacing dynamically based on the figure size.
#         - Connects a resize event to maintain responsiveness.

#         Notes:
#             Adjustments are tailored for a default figure size of (10, 6).
#         """

#         fig_w, fig_h = 10, 6

#         self.fig, self.axes = plt.subplot_mosaic(
#             [
#                 ["log", "log", "log", "corr_log"],
#                 ["lin", "lin", "lin", "corr_lin"],
#             ],
#             figsize=(fig_w, fig_h)
#         )

#         def on_resize(event):
#             fig_width, fig_height = self.fig.get_size_inches()
#             scale = min(fig_width / fig_w, fig_height / fig_h)
#             self.fig.subplots_adjust(
#                 top=0.96,
#                 bottom=0.1,
#                 left=0.05,
#                 right=0.99,
#                 hspace=0.13 * scale,
#                 wspace=0.2 * scale
#             )
#             plt.draw()

#         self.fig.canvas.mpl_connect('resize_event', on_resize)

#         self.fig.subplots_adjust(
#             top=0.96,
#             bottom=0.1,
#             left=0.05,
#             right=0.99,
#             hspace=0.13,
#             wspace=0.2
#         )

#     def build_colorbar(
#         self,
#         ax: Axes,
#         extra_data: DataFrame,
#     ) -> None:
#         """
#         Adds a colorbar to the specified axis based on extra data.

#         Args:
#             ax (Axes):
#                 The axis to which the colorbar will be added.
#             extra_data (DataFrame):
#                 The data to use for determining color scaling.

#         Notes:
#             - The colorbar is based on a linear segmented colormap.
#             - The default range for values is 0 to 100.
#         """

#         vmin: float = 0
#         vmax: float = 100
#         orientation: str = "vertical"
#         label_position: str = "right"
#         ticks_position: str = "left"
#         pad: float = 0.05
#         fraction: float = 0.02
#         aspect: int = 50
#         labelpad: int = 1
#         nb_divs: int = 100
#         cmap = LinearSegmentedColormap.from_list(
#             name=extra_data.data_name,
#             colors=self.cmap_colors,
#             N=nb_divs
#         )
#         norm = Normalize(vmin=vmin, vmax=vmax)
#         sm = ScalarMappable(cmap=cmap, norm=norm)
#         sm.set_array([])
#         self.cbar = self.fig.colorbar(
#             sm,
#             ax=ax,
#             orientation=orientation,
#             pad=pad,
#             fraction=fraction,
#             aspect=aspect
#         )
#         self.cbar.set_label(
#             label=extra_data.data_name,
#             labelpad=labelpad
#         )
#         self.cbar.ax.yaxis.set_label_position(label_position)
#         self.cbar.ax.yaxis.set_ticks_position(ticks_position)

#     def get_points_color(
#         self,
#         data: pd.DataFrame
#     ) -> list[str]:
#         """
#         Determines the colors for scatter plot points based on extra data.

#         Args:
#             data (pd.DataFrame):
#                 The data for which colors need to be assigned.

#         Returns:
#             list[str]: A list of RGBA tuples for each data point.
#             Points without extra data are assigned a default blue color.
#         """

#         extra_data_colored_name = self.data_frames[
#             self.colored_extra_data].data_name
#         if extra_data_colored_name in data.columns:
#             colors = self.cmap_colors
#             gray = (0.5, 0.5, 0.5, 1.0)
#             cmap = LinearSegmentedColormap.from_list(
#                 "cmap_name",
#                 colors,
#                 N=100
#             )
#             colored_extra_data_values = data[extra_data_colored_name]
#             norm = Normalize(vmin=0, vmax=100)
#             colors = [
#                 cmap(norm(g)) if not np.isnan(g) else gray
#                 for g in colored_extra_data_values
#             ]

#         else:
#             colors = ['blue'] * len(data)

#         return colors

#     def plot_scatter(
#         self,
#         ax: Axes,
#         data: pd.DataFrame,
#         points_color: list[str],
#     ) -> mplcollec.PathCollection:
#         """
#         Plots a scatter graph with optional
#         highlighting of a tracked element.

#         Args:
#             ax (Axes):
#                 The axis on which to plot the scatter graph.
#             data (pd.DataFrame):
#                 The data to plot.
#             points_color (list[str]):
#                 The color of each point.

#         Returns:
#             mplcollec.PathCollection:
#                 The collection of scatter plot points.

#         Highlights:
#             - Uses circle sizes proportional to the `data_point_size`.
#             - Highlights the tracked element in cyan if specified.
#         """

#         pt_size_s_name = self.data_frames["data_point_size"].short_name
#         scatter = ax.scatter(
#             data[self.data_frames["data_x"].data_name].values,
#             data[self.data_frames["data_y"].data_name].values,
#             s=data[
#                 self.data_frames["data_point_size"].data_name
#                 ].values / self.data_point_size_divider,
#             c=points_color,
#             alpha=0.7,
#             label=f"{self.common_column.title()} ({pt_size_s_name}-sized)"
#         )

#         if self.tracked_element:
#             highlighted = data[
#                 data[self.common_column].str.contains(
#                     self.tracked_element,
#                     case=False,
#                     na=False
#                 )
#             ]
#             if not highlighted.empty:
#                 ax.scatter(
#                     highlighted[self.data_frames["data_x"].data_name],
#                     highlighted[self.data_frames["data_y"].data_name],
#                     s=highlighted[
#                         self.data_frames["data_point_size"].data_name
#                         ] / self.data_point_size_divider,
#                     color='cyan',
#                     label=f"Tracked: {self.tracked_element}",
#                     edgecolor='black'
#                 )
#         return scatter

#     def plot_regressline(
#             self,
#             timediv: TimeDiv,
#             is_log_scale: bool,
#             ax: Axes,
#             color: str
#     ) -> None:
#         """
#         Plots the regression line on the specified axis.

#         Args:
#             timediv (TimeDiv):
#                 The time division containing regression data.
#             is_log_scale (bool):
#                 Whether the regression is log-scaled.
#             ax (Axes):
#                 The axis on which to plot the regression line.
#             color (str):
#                 The color of the regression line.

#         Notes:
#             - The regression line is dashed and
#             annotated with its correlation coefficient.
#             - Points with NaN values are filtered out before plotting.
#         """

#         x = np.sort(
#                 timediv.merged_data[self.data_frames["data_x"].data_name])
#         regression = (
#             timediv.lin_reg_log
#             if is_log_scale
#             else timediv.lin_reg_lin
#         )
#         y = regression.predicted

#         mask = ~np.isnan(x) & ~np.isnan(y)
#         x_cleaned = x[mask]
#         y_cleaned = y[mask]

#         reg_line_type = 'log-linear' if is_log_scale else 'linear'
#         ax.plot(
#             x_cleaned,
#             y_cleaned,
#             color=color,
#             linestyle='--',
#             label=f"Regression Line ({reg_line_type})"
#                   f" - Corr: {regression.corr:.2f}"
#         )

#     def set_graph_meta_data(
#         self,
#         timediv: TimeDiv,
#         is_log_scale: bool,
#         ax: Axes,
#         color: str
#     ) -> None:
#         """
#         Sets metadata (titles, labels, scales) for a scatter plot.

#         Args:
#             timediv (TimeDiv):
#                 The time division for which the graph is being set.
#             is_log_scale (bool):
#                 Whether the graph is log-scaled.
#             ax (Axes):
#                 The axis to set metadata for.
#             color (str):
#                 The highlight color for text annotations.

#         Notes:
#             - Adds bold watermark text indicating "LOG" or "LINEAR" scaling.
#             - Titles and labels are set dynamically based on the scale type.
#         """

#         if is_log_scale:
#             ax.set_xscale('log')
#             ax.set_title(f"{self.title} in {timediv.div}")
#             ax.set_xlabel(
#                 f"{self.x_label} ({self.x_unit}, log scale)",
#                 labelpad=-5
#             )
#         else:
#             ax.set_xlabel(f"{self.x_label} ({self.x_unit})")
#         ax.set_ylabel(f"{self.y_label} ({self.y_unit})")

#         ax.legend(loc="best")

#         ax.text(
#             0.5,
#             0.5,
#             "LOG" if is_log_scale else "LINEAR",
#             transform=ax.transAxes,
#             fontsize=100,
#             color=color,
#             alpha=0.08,
#             ha="center", va="center",
#             weight="bold",
#         )

#     def manage_cursor(
#         self,
#         ax_name: str,
#         scatter: PathCollection,
#         data: pd.DataFrame
#     ) -> None:
#         """
#         Adds interactivity with a cursor to a scatter plot.

#         Args:
#             ax_name (str):
#                 Name of the axis.
#             scatter (PathCollection):
#                 The scatter plot collection.
#             data (pd.DataFrame):
#                 The data corresponding to the scatter plot.

#         Notes:
#             - Annotations display detailed information for each point.
#             - Removes existing cursors on the axis before adding a new one.
#         """

#         if (
#             ax_name in self.cursor_container
#             and self.cursor_container[ax_name]
#         ):
#             try:
#                 self.cursor_container[ax_name].remove()
#                 self.cursor_container[ax_name] = None
#             except Exception as e:
#                 print(
#                     f"Warning: Failed to remove cursor on "
#                     f"{ax_name}: {e}"
#                 )

#         cursor = mplcursors.cursor(
#             scatter,
#             hover=True
#         )

#         @cursor.connect("add")
#         def on_add(sel):
#             """
#             Handles the addition of cursor annotations for scatter plots.

#             Args:
#                 sel (mplcursors.Selection):
#                     The selection object for the hovered data point.

#             Functionality:
#                 - Retrieves the index and data of the selected point.
#                 - Formats and displays an annotation with relevant details:
#                 x-value, y-value, point size, and extra data (if available).
#                 - Styles the annotation box for clarity.
#                 - Ensures robust handling of missing or invalid data.

#             Raises:
#                 KeyError:
#                     If a required column is missing in the DataFrame.
#                 Exception:
#                     For unexpected errors during the annotation process.
#             """

#             idx = sel.index

#             try:
#                 row = data.iloc[idx]
#                 data_x_name = self.data_frames["data_x"].data_name
#                 data_y_name = self.data_frames["data_y"].data_name
#                 data_point_size_name = self.data_frames[
#                     "data_point_size"].data_name
#                 extra_data_x_text = 'N/A'
#                 extra_data_x_name = self.data_frames[
#                     "extra_data_x"].data_name

#                 if (
#                     extra_data_x_name in row.index
#                     and pd.notna(row[extra_data_x_name])
#                 ):
#                     extra_data_x_text = f"{row[extra_data_x_name]:.2f}"

#                 sel.annotation.set(
#                     text=(
#                         f"{row[self.common_column]}\n"
#                         f"{self.data_frames['data_x'].short_name}: "
#                         f"{put_kmb_suffix(row[data_x_name])} {self.x_unit}\n"
#                         f"{self.data_frames['data_y'].short_name}: "
#                         f"{row[data_y_name]:.1f} {self.y_unit}\n"
#                         f"{self.data_frames['data_point_size'].short_name}: "
#                         f"{put_kmb_suffix(row[data_point_size_name])}\n"
#                         f"{self.data_frames['extra_data_x'].short_name}: "
#                         f"{extra_data_x_text}"
#                     ),
#                     fontsize=10,
#                     fontweight="bold"
#                 )
#                 sel.annotation.get_bbox_patch().set(alpha=0.6, color="white")

#             except KeyError as e:
#                 print(f"KeyError during cursor annotation: {e}")
#             except Exception as e:
#                 print(f"Unexpected error during cursor annotation: {e}")

#         self.cursor_container[ax_name] = cursor

#     def plot(
#         self,
#         timediv: TimeDiv,
#         ax: Axes,
#         is_log_scale: bool,
#         ax_name: str,
#         color: str
#     ) -> None:
#         """
#         Plots a scatter graph, regression line, and adds interactivity.

#         Args:
#             timediv (TimeDiv): The time division data to plot.
#             ax (Axes): The axis to plot on.
#             is_log_scale (bool): Whether the graph uses a log scale.
#             ax_name (str): The name of the axis.
#             color (str): The highlight color for the regression line.

#         Notes:
#             - Combines scatter plots,
#             regression lines, and cursor interactivity.
#         """

#         data = timediv.merged_data
#         points_color = self.get_points_color(data)
#         scatter = self.plot_scatter(
#             ax,
#             data,
#             points_color)
#         self.plot_regressline(
#             timediv,
#             is_log_scale,
#             ax,
#             color,
#         )
#         self.set_graph_meta_data(
#             timediv,
#             is_log_scale=is_log_scale,
#             ax=ax,
#             color=color,
#         )

#         self.manage_cursor(
#             ax_name,
#             scatter,
#             data
#         )

#     def update_color_point_from_extra_data(
#         self,
#         timediv: TimeDiv
#     ) -> None:
#         """
#         Updates the visibility of the colorbar
#         based on the presence of extra data.

#         Args:
#             timediv (TimeDiv):
#                 The current time division data.

#         Notes:
#             - Hides or shows the colorbar dynamically
#             depending on whether extra data is available.
#         """

#         extra_data_x_name = self.data_frames["extra_data_x"].data_name
#         if extra_data_x_name in timediv.merged_data.columns:
#             if not self.cbar.ax.get_visible():
#                 self.cbar.ax.set_visible(True)
#         else:
#             if self.cbar.ax.get_visible():
#                 self.cbar.ax.set_visible(False)

#     def update_corr_graphs(self) -> None:
#         """
#         Updates the correlation graphs with a vertical line
#         indicating the current slider value.

#         Notes:
#             - Removes any existing vertical lines before adding a new one.
#             - The vertical line highlights the selected year on the graph.
#         """

#         for corr_name, corr_ax in self.axes.items():
#             if "corr" in corr_name:
#                 selected_x = self.slider.val

#                 if hasattr(self, f"{corr_name}_vline"):
#                     getattr(self, f"{corr_name}_vline").remove()

#                 setattr(
#                     self,
#                     f"{corr_name}_vline",
#                     corr_ax.axvline(
#                         x=selected_x,
#                         color="orange",
#                         linestyle="--",
#                         linewidth=0.8
#                     )
#                 )

#     def update(
#         self,
#         slider_val=None
#     ) -> None:
#         """
#         Updates the main plots (scatter and correlation graphs)
#         based on the slider value.

#         Args:
#             slider_val (int, optional):
#                 The current value of the slider. Defaults to None.

#         Notes:
#             - Replots scatter graphs with updated data.
#             - Updates regression lines and correlation graphs.
#             - Adjusts colorbar visibility and correlation graph indicators.
#         """

#         self.axes["log"].cla()
#         self.axes["lin"].cla()

#         if slider_val is None:
#             slider_val = int(self.slider.val)

#         timediv = self.precomputed_data[slider_val]

#         self.plot(
#             timediv=timediv,
#             ax=self.axes['log'],
#             is_log_scale=True,
#             ax_name="log",
#             color="red"
#         )
#         self.plot(
#             timediv=timediv,
#             ax=self.axes['lin'],
#             is_log_scale=False,
#             ax_name="lin",
#             color="green"
#         )

#         self.update_color_point_from_extra_data(timediv)

#         self.update_corr_graphs()

#         plt.draw()

#     def update_slider_title(
#         self,
#         val: int
#     ) -> None:
#         """
#         Updates the title text of the slider to reflect the current year.

#         Args:
#             val (int):
#                 The current slider value.

#         Notes:
#             - Dynamically updates the displayed text with the current year.
#         """

#         self.slider_title_text.set_text(
#             f"{self.timediv_type.title()}: {int(val)}"
#         )
#         self.fig.canvas.draw_idle()

#     def build_slider(
#         self,
#         update_callback_function: Callable
#     ) -> None:
#         """DOCSTRING"""

#         ax_slider = self.fig.add_axes([0.05, 0.01, 0.5, 0.03])
#         self.slider = Slider(
#             ax_slider,
#             "",
#             self.timediv_range.start,
#             self.timediv_range.stop - 1,
#             valinit=self.init_value,
#             valstep=1,
#             color="olive"
#         )
#         self.slider_title_text = ax_slider.text(
#             0.5, 0.3,
#             f"{self.timediv_type.title()}: {int(self.slider.val)}",
#             transform=ax_slider.transAxes,
#             fontsize=10,
#             ha='left'
#         )
#         self.slider.on_changed(self.update_slider_title)
#         self.slider.on_changed(update_callback_function)

#         self.play_ax = self.fig.add_axes([0.56, 0.01, 0.03, 0.03])
#         self.play_button = Button(self.play_ax, '\u25B6')
#         self.play_button.on_clicked(self.start_animation)

#         self.pause_ax = self.fig.add_axes([0.6, 0.01, 0.03, 0.03])
#         self.pause_button = Button(self.pause_ax, r'$\mathbf{| |}$')
#         self.pause_button.on_clicked(self.stop_animation)

#     def start_animation(
#         self,
#         event=None
#     ) -> None:
#         """
#         Starts the animation of the slider and associated plots.

#         Args:
#             event (optional):
#                 The triggering event, typically from a UI interaction.

#         Notes:
#             - If the animation is already running
#             (`self.running_mode` is True), the method does nothing.
#             - The animation iterates over frames
#             starting from the current slider value.
#         """

#         if self.running_mode and not self.first_running:
#             return

#         self.first_running = False
#         self.running_mode = True
#         self.anim = FuncAnimation(
#             self.fig,
#             self.update_slider,
#             frames=range(self.slider.val, self.timediv_range.stop),
#             repeat=True,
#             interval=self.interval_between_two_frames,
#         )
#         plt.draw()

#     def stop_animation(
#         self,
#         event=None
#     ) -> None:
#         """
#         Stops the animation of the slider.

#         Args:
#             event (optional):
#                 The triggering event, typically from a UI interaction.

#         Notes:
#             - If the animation is not running, the method does nothing.
#         """
#         if not self.running_mode:
#             return
#         self.running_mode = False
#         if self.anim is not None:
#             self.anim.pause()

#     def update_slider(self, frame):
#         """
#         Updates the slider value and the current frame
#         during the animation.

#         Args:
#             frame (int):
#                 The current frame value.

#         Notes:
#             - Updates the slider's position
#             and stores the current frame value.
#         """

#         self.slider.set_val(frame)
#         self.current_frame = frame

#     def set_right_side_graphs_cursors(self) -> None:
#         """
#         Adds interactivity (cursors) to the curves
#         in the correlation and p-value graphs.

#         Notes:
#             - Cursors provide hover annotations for
#             correlation and p-value graphs.
#             - Existing cursors are removed before new ones are added.
#         """

#         curve_labels = {
#             "corr_log": ["corr log", "pvalue log"],
#             "corr_lin": ["corr lin", "pvalue lin"],
#         }

#         for ax_name, labels in curve_labels.items():
#             if ax_name in self.axes:
#                 ax = self.axes[ax_name]

#                 for label in labels:
#                     if (
#                         label in self.correlation_cursor_container
#                         and self.correlation_cursor_container[label]
#                     ):
#                         try:
#                             self.correlation_cursor_container[label].remove()
#                             self.correlation_cursor_container[label] = None
#                         except Exception as e:
#                             print(
#                                 f"Warning: Failed to remove"
#                                 f" cursor on {label}: {e}"
#                             )

#                 for line in ax.get_lines():
#                     if line.get_label() in labels:
#                         cursor = mplcursors.cursor(line, hover=True)

#                         @cursor.connect("add")
#                         def on_add(sel, label=line.get_label()):
#                             """
#                             Callback function to handle hover events
#                             on correlation and p-value curves.

#                             Args:
#                                 sel:
#                                     The mplcursors selection object,
#                                     providing details about
#                                     the hovered point.
#                                 label (str):
#                                     The label of the curve being annotated,
#                                     used to distinguish between correlation
#                                     and p-value curves.

#                             Functionality:
#                                 - Retrieves the year (x) and
#                                 the curve value (y) of the hovered point.
#                                 - Sets an annotation displaying the year
#                                 and the value with a prefix
#                                 ('Corr' or 'Pval') based on the curve type.
#                                 - Styles the annotation for better
#                                 visibility and clarity.
#                             """
#                             x, y = sel.target
#                             annotation = (
#                                 "Corr" if "corr" in label else "Pval"
#                             )
#                             sel.annotation.set(
#                                 text=f"Year: {x:.0f}\n{annotation}: {y:.4f}",
#                                 fontsize=10,
#                                 fontweight="bold",
#                             )
#                             sel.annotation.get_bbox_patch().set(
#                                 alpha=0.8,
#                                 color="white"
#                             )

#                         self.correlation_cursor_container[
#                             line.get_label()
#                         ] = cursor

#     def add_tracker(
#         self,
#         text: str
#     ) -> None:
#         """
#         Adds or updates a tracked element to be highlighted in the plots.

#         Args:
#             text (str):
#                 The name of the element to track.

#         Notes:
#             - Updates the main plots to reflect the tracked element.
#             - Resets and re-applies cursors to the right-side graphs.
#         """

#         self.tracked_element = text.strip()
#         self.update()
#         self.set_right_side_graphs_cursors()

#     def build_tracker(self) -> None:
#         """
#         Builds a text box for tracking a specific element in the plots.

#         Notes:
#             - Adds a text box UI element for user input to
#             track a specific data element.
#             - Associates the text box with the `add_tracker`
#             method for interactivity.
#         """

#         self.ax_box_tracker = self.fig.add_axes([0.81, 0.005, 0.18, 0.05])
#         self.text_box_tracker = TextBox(
#             self.ax_box_tracker,
#             f"Track {self.common_column}"
#         )
#         self.text_box_tracker.on_submit(self.add_tracker)

#     def set_and_plot_right_side_graph(
#         self,
#         graph: str
#     ) -> None:
#         """
#         Plots and configures the correlation and
#         p-value graph for a given axis.

#         Args:
#             graph (str):
#                 The name of the graph, either "log" or "lin".

#         Notes:
#             - Configures axis labels, legends, and titles dynamically.
#             - Adds correlation and p-value curves to the specified graph.
#         """

#         ax = self.axes["corr_" + graph]

#         ax.plot(
#             np.array(self.timediv_range),
#             self.corr_log if graph == "log" else self.corr_lin,
#             label="corr " + graph,
#             color="red" if graph == "log" else "green",
#         )
#         ax.plot(
#             np.array(self.timediv_range),
#             self.pvalue_log if graph == "log" else self.pvalue_lin,
#             label="pvalue " + graph,
#             color="purple" if graph == "log" else "olive",
#         )

#         ax.set_xlabel(self.timediv_type, labelpad=-27)
#         ax.set_xlim(self.timediv_range.start, self.timediv_range.stop)
#         ax.set_ylabel("Corr. Coeff. or Pvalue", labelpad=-30, loc="center")
#         ax.set_ylim(-1, 1)
#         ax.set_yticks([-1, -0.75, 0.75, 1])
#         ax.text(
#             0.5,
#             0.5,
#             graph.upper(),
#             transform=ax.transAxes,
#             fontsize=30,
#             color="red" if graph == "log" else "green",
#             alpha=0.08,
#             ha="center",
#             va="center",
#             weight="bold",
#         )
#         ax.legend()

#         if graph == "log":
#             ax.set_title(f"Corr. Coeff. and Pvalue VS {self.timediv_type}")

#     def build_mpl_window(
#         self,
#     ) -> None:
#         """
#         Builds the matplotlib window with all elements,
#         including graphs, sliders, and trackers.

#         Notes:
#             - Sets up axes, colorbars, sliders, and right-side graphs.
#             - Configures dynamic window resizing and graph adjustments.
#         """

#         self.build_fig_axes()

#         self.build_colorbar(
#             ax=self.axes["log"],
#             extra_data=self.data_frames['extra_data_x']
#         )

#         self.build_slider(
#             update_callback_function=self.update)

#         self.build_tracker()

#         self.set_and_plot_right_side_graph("log")
#         self.set_and_plot_right_side_graph("lin")

#         self.fig.canvas.manager.set_window_title(
#             f"{self.data_frames['data_x'].short_name} VS "
#             f"{self.data_frames['data_y'].short_name} for each "
#             f"{self.timediv_type} between "
#             f"{self.timediv_range.start} and "
#             f"{self.timediv_range.stop - 1}"
#         )

#     def pltshow(self) -> None:
#         """
#         Displays the matplotlib window and starts the animation if enabled.

#         Raises:
#             RuntimeError:
#                 If the figure is not initialized before calling this method.

#         Notes:
#             - Ensures the animation starts if `first_running` is True.
#         """

#         if self.fig is not None:
#             if self.first_running:
#                 self.start_animation()
#             plt.show()
#         else:
#             raise RuntimeError(
#                 "Figure not initialized.\n"
#                 "Make sure build_figure_axes Day02Ex03"
#                 "method has beed called before."
#             )

#     @typeguard.typechecked
#     def set_interval_between_two_frames(
#         self,
#         interval: int = 100
#     ) -> None:
#         """
#         Sets the time interval between two frames during the animation.

#         Args:
#             interval (int): the interval, in ms, between two frames.

#         Notes:
#             - A big interval will make the animation slower.
#         """

#         self.interval_between_two_frames = interval


# def main() -> None:
#     """
#     Main function to set up and execute the Day02Ex03 application.

#     Workflow:
#         - Initializes the `Day02Ex03` object.
#         - Adds paths for data and metadata.
#         - Cleans and precomputes data.
#         - Configures the matplotlib window and its elements.
#         - Optionally enables autoplay.
#         - Displays the application window.
#     """

#     try:
#         exo03 = Day02Ex03()

#         exo03.add_data_x_path(
#             "income_per_person_gdppercapita_ppp_inflation_adjusted.csv",
#             short_name="GDP per capita",
#             x_label="Gross Domestic Product per capita at PPP",
#             x_unit="USD"
#         )
#         exo03.add_data_y_path(
#             "life_expectancy_years.csv",
#             short_name="life_expectancy",
#             y_label="Life expectancy",
#             y_unit="year"
#         )
#         exo03.add_data_point_size_path(
#             "population_total.csv",
#             short_name="population",
#             divider=1e6
#         )
#         exo03.add_extra_data_x_path(
#             "Gini_coefficient.csv",
#             short_name="Gini coefficient"
#         )
#         # exo03.add_extra_data_y_path(
#         #     "",
#         #     short_name=""
#         # )
#         exo03.add_title(
#             "Life Expectancy"
#             " VS "
#             "Inflation-adjusted GDP per capita "
#             "at purchasing power parity (PPP)"
#         )
#         exo03.add_timediv_range(
#             start=1800,
#             stop=2050,
#             init_value=1900,
#             type="year",
#         )
#         exo03.add_common_column('country')

#         exo03.clean_data_frames()
#         exo03.precompute_data()

#         exo03.build_mpl_window()
#         exo03.update()
#         exo03.set_right_side_graphs_cursors()
#         exo03.set_autoplay_at_start(True)
#         exo03.set_interval_between_two_frames(200)

#         exo03.pltshow()

#     except ValueError as error:
#         print(f"{type(error).__name__}: {error}")
#     except typeguard.TypeCheckError as error:
#         print(f"{type(error).__name__}: {error}")
#     except Exception as error:
#         print(f"An unexpected error occurred: {error}")


# if __name__ == "__main__":
#     main()
