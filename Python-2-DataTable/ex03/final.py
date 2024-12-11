import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.widgets import Slider, TextBox
from matplotlib.colors import Normalize, LinearSegmentedColormap
from scipy.stats import linregress
import mplcursors
from fuzzywuzzy import process



class LinReg:
    def __init__(self,
                 predicted: np.ndarray,
                 corr: float):
        self.predicted = predicted
        self.corr = corr


class Year:
    def __init__(self,
                 year:int,
                 data:pd.DataFrame):
        self.year = year
        self.data = data
        self.lin_reg_log: LinReg = None
        self.lin_reg_lin: LinReg = None


    def calculate_linregr(self, log: bool) -> LinReg:
        """DOCSTRING"""

        slope, intercept, corr, _, _ = linregress(
            np.log10(self.data['gdp']) if log else self.data['gdp'],
            self.data['life_expectancy']
        )

        gdp_sorted = np.sort(self.data['gdp'])

        # === Predicted life expectancy
        if log:
            predicted = slope * np.log10(gdp_sorted) + intercept
        else:
            predicted = slope * gdp_sorted + intercept

        return LinReg(predicted, corr)


    def linear_regressions(self) -> None:
        """DOCSTRING"""
        self.lin_reg_log = self.calculate_linregr(True)
        self.lin_reg_lin = self.calculate_linregr(False)

    def show(self) -> None:
        print("\n===== Show Year Object =====")
        print(f"self.year:\n{self.year}")
        print(f"self.data:\n{self.data}")
        print("\n===== END Show Year Object END =====")


def cust_suffixed_string_to_float(value) -> float:
    factors = {'k': 1e3, 'M': 1e6, 'B': 1e9}
    try:
        if isinstance(value, str) and value[-1] in factors:
            return float(value[:-1]) * factors[value[-1]]
        return float(value)
    except (ValueError, TypeError):
        return np.nan


def clean_extra_data_x(extra_data_x: pd.DataFrame, data_y: pd.DataFrame) -> pd.DataFrame:
    extra_data_x = extra_data_x.drop(
        columns=[
            "Country Code",
            "Indicator Name",
            "Indicator Code",
            "Unnamed: 68"
        ],
        errors="ignore"
    )

    extra_data_x = extra_data_x.rename(columns={"Country Name": "country"})

    data_y_countries = data_y["country"].unique()

    def match_country_name(country):
        match, score = process.extractOne(country, data_y_countries)
        return match if score >= 80 else None

    extra_data_x["country"] = extra_data_x["country"].apply(match_country_name)

    extra_data_x = extra_data_x.dropna(subset=["country"])

    extra_data_x = extra_data_x.drop_duplicates(subset=["country"], keep="first")

    extra_data_x = extra_data_x.sort_values(by="country").reset_index(drop=True)

    
    return extra_data_x


def precompute_data(
    years: range,
    data_y: pd.DataFrame,
    data_x: pd.DataFrame,
    data_point_size: pd.DataFrame,
    extra_data_x: pd.DataFrame,
    # extra_data_y: pd.DataFrame
    ) -> tuple[
            dict[int, 'Year'],
            np.ndarray[np.float64],
            np.ndarray[np.float64]
        ]:
    """DOCSTRING"""

    data_x = data_x.sort_values(by="country").reset_index(drop=True)
    data_y = data_y.sort_values(by="country").reset_index(drop=True)
    data_point_size = data_point_size.sort_values(by="country").reset_index(drop=True)
    
    extra_data_x_cleaned = clean_extra_data_x(extra_data_x, data_x)
    # extra_data_x_cleaned.to_csv("clean_data.csv", index=False)

    precomputed_data = dict()
    corr_log = list()
    corr_lin = list()
    for year in years:
        year_col = str(year)

        # ===== Subsets extraction =====
        life_expectancy_year = data_y[['country', year_col]].rename(
            columns={year_col: 'life_expectancy'}
        )
        gdp_year = data_x[['country', year_col]].rename(columns={year_col: 'gdp'})
        pop_year = data_point_size[['country', year_col]].rename(columns={year_col: 'population'})
        if year >= 1960 and year <= 2023:
            gini_year = extra_data_x_cleaned[['country', year_col]].rename(columns={year_col: 'gini'})

        # === Parsing from string to computable data (float)
        gdp_year['gdp'] = gdp_year['gdp'].apply(
            cust_suffixed_string_to_float
        )
        pop_year['population'] = pop_year['population'].apply(
            cust_suffixed_string_to_float
        )
        if year >= 1960 and year <= 2023:
            gini_year['gini'] = gini_year['gini'].apply(
                cust_suffixed_string_to_float
            )

        # ===== Subsets merge =====
        merged_data = pd.merge(life_expectancy_year, gdp_year, on='country')
        merged_data = pd.merge(merged_data, pop_year, on='country')
        merged_data = merged_data.dropna()
        if year >= 1960 and year <= 2023:
            merged_data = pd.merge(merged_data, gini_year, on='country')

        # === Year object creation and linear regression computation ===
        year_object = Year(year, merged_data)
        year_object.linear_regressions()

        # if year in [1950, 2000, 2010, 2040]:
        #     print(f"\nmerged_data {year}:\n{merged_data}")
        #     year_object.show()

        # === Data storage in the res variables ===
        precomputed_data[year] = year_object
        corr_log.append(year_object.lin_reg_log.corr)
        corr_lin.append(year_object.lin_reg_lin.corr)

    corr_log = np.array(corr_log)
    corr_lin = np.array(corr_lin)
    return precomputed_data, corr_log, corr_lin


def get_points_colors(data: pd.DataFrame) -> list[str]:
    """DOCSTRING (extra_data_x)"""

    if 'gini' in data.columns:
        colors = ["green", "yellow", "orange", "red", "purple"]
        gray = (0.5, 0.5, 0.5, 1.0)
        cmap = LinearSegmentedColormap.from_list("custom_gini", colors, N=100)
        gini_values = data['gini']
        norm = Normalize(vmin=0, vmax=100)
        colors = [
            cmap(norm(g)) if not np.isnan(g) else gray
            for g in gini_values
        ]
    else:
        colors = ['blue'] * len(data)

    return colors


def plot_scatter() -> None:
    """DOCSTRING"""
    


def plot(year_data: Year,
         ax: plt.Axes,
         is_log_scale: bool,
         tracked_country: list,
         cursor_container: dict,
         ax_name: str,
         color: str) -> None:
    """
    Plot the scatterplot and regression line for a given axis.
    Args:
        year_data (Year): Year object containing data and regression info.
        ax (matplotlib.axes.Axes): Axis to draw the plot on.
        is_log_scale (bool): Whether to use a logarithmic scale for GDP.
        tracked_country (str): Country to highlight if specified.
        cursor_container (dict): Dictionary to store active cursors per axis.
        ax_name (str): Name of the axis for managing cursors.
    """

    data = year_data.data
    points_colors = get_points_colors(data)

    # === Scatter part ===
    scatter = ax.scatter(
        data['gdp'],
        data['life_expectancy'],
        s=data['population'] / 1e6,
        c=points_colors,
        alpha=0.7,
        label="Countries (population-weighted)"
    )
    if tracked_country:
        highlighted = data[data['country'].str.contains(tracked_country, case=False, na=False)]
        if not highlighted.empty:
            ax.scatter(
                highlighted['gdp'],
                highlighted['life_expectancy'],
                s=highlighted['population'] / 1e6,
                color='cyan',
                label=f"Tracked: {tracked_country}",
                edgecolor='black'
            )

    # === Regression line part===
    regression = (year_data.lin_reg_log
                  if is_log_scale
                  else year_data.lin_reg_lin)
    ax.plot(
        np.sort(data['gdp']),
        regression.predicted,
        color=color,
        linestyle='--',
        label=f"Regression Line ({'log-linear' if is_log_scale else 'linear'})"
              f" - Corr: {regression.corr:.2f}"
    )

    if is_log_scale:
        ax.set_xscale('log')
        ax.set_title(f"Life Expectancy vs Inflation-adjusted GDP per capita at purchasing power parity (PPP) in {year_data.year}")
        ax.set_xlabel(
            "Gross Domestic Product per capita at PPP (USD, log scale)",
            labelpad=-5)
    else:
        ax.set_xlabel("Gross Domestic Product per capita at PPP (USD)")
    ax.set_ylabel("Life Expectancy (years)")
    
    ax.legend(loc="best")

    ax.text(
        0.5,
        0.5,
        "LOG" if is_log_scale else "LINEAR",
        transform=ax.transAxes,
        fontsize=100,
        color=color,
        alpha=0.08,
        ha="center", va="center",
        weight="bold",
    )

    if ax_name in cursor_container and cursor_container[ax_name]:
        try:
            cursor_container[ax_name].remove()
            cursor_container[ax_name] = None
        except Exception as e:
            print(f"Warning: Failed to remove cursor on {ax_name}: {e}")

    cursor = mplcursors.cursor(scatter, hover=True)

    def put_kmb_suffix(val: int) -> str:
        """
        Formats a large number with 'k', 'M', or 'B' suffixes.
        """
        for threshold, suffix in [(1e9, 'B'), (1e6, 'M'), (1e3, 'k')]:
            if val > threshold:
                return f"{val / threshold:.2f}{suffix}"
        return str(val)

    @cursor.connect("add")
    def on_add(sel):
        idx = sel.index
        row = data.iloc[idx]

        gini_text = 'N/A'
        if 'gini' in row:
            gini_value = row['gini']
            if gini_value == gini_value:
                gini_text = gini_value

        sel.annotation.set(
            text=(
                f"{row['country']}\n"
                f"Life Expectancy: {row['life_expectancy']:.1f} years\n"
                f"GDP: {put_kmb_suffix(row['gdp'])}\n"
                f"Population: {put_kmb_suffix(row['population'])}\n"
                f"Gini Index: {gini_text}"
            ),
            fontsize=10,
            fontweight="bold"
        )
        sel.annotation.get_bbox_patch().set(alpha=0.6, color="white")

    cursor_container[ax_name] = cursor

def update(slider_val: int,
           axes: dict,
           precomputed_data: dict,
           cursor_container: dict,
           tracked_country: list) -> None:
    """
    Update all axes when the slider value changes.
    Args:
        val (float): Slider value.
        axes (dict): Dictionary of axes.
        slider (Slider): Year slider.
        precomputed_data (dict): Precomputed data for all years.
        cursor_container (dict): Dictionary of active cursors per axis.
        tracked_country (str): Country to track if specified.
    """

    year_data = precomputed_data[slider_val]

    axes["log"].cla()
    axes["lin"].cla()

    plot(
        year_data=year_data,
        ax=axes["log"],
        is_log_scale=True,
        tracked_country=tracked_country,
        cursor_container=cursor_container,
        ax_name="log",
        color="red"
    )

    plot(
        year_data=year_data,
        ax=axes["lin"],
        is_log_scale=False,
        tracked_country=tracked_country,
        cursor_container=cursor_container,
        ax_name="lin",
        color="green"
    )

    plt.draw()


def add_tracker(text,
                tracked_country,
                ax,
                precomputed_data,
                cursor_container,
                slider):

    tracked_country[0] = text.strip()
    update(slider.val,
           ax,
           precomputed_data,
           cursor_container,
           tracked_country[0]
    )


def corr_graph_settings(ax, years, corr, label, color) -> None: 
    """DOCSTRING"""
    
    ax.plot(
        np.array(years),
        corr,
        label=f"{label} correlation",
        color=color
    )

    ax.set_xlabel("Year", labelpad=0)
    ax.set_xlim(years.start, years.stop - 1)
    ax.set_ylabel("Correlation Coefficient")
    ax.set_ylim(0, 1)

    ax.text(
        0.5,
        0.5,
        label.upper(),
        transform=ax.transAxes,
        fontsize=30,
        color=color,
        alpha=0.08,
        ha="center", va="center",
        weight="bold",
    )

    ax.legend()


def add_curve_interactivity(axes: dict, correlation_axes: list, cursor_container: dict) -> None:
    """
    Adds interactivity to the correlation curves,
    showing the closest point on hover.

    Args:
        axes (dict): Dictionary of axes.
        correlation_axes (list): List of axes names to target for interactivity.
        cursor_container (dict): Dictionary to store active cursors for correlation graphs.
    """
    for name in correlation_axes:
        if name in axes:
            ax = axes[name]

            if name in cursor_container and cursor_container[name]:
                try:
                    cursor_container[name].remove()
                    cursor_container[name] = None
                except Exception as e:
                    print(f"Warning: Failed to remove cursor on {name}: {e}")

            for line in ax.get_lines():
                cursor = mplcursors.cursor(line, hover=True)

                @cursor.connect("add")
                def on_add(sel):
                    x, y = sel.target
                    sel.annotation.set(
                        text=f"Year: {x:.0f}\nCorr: {y:.2f}",
                        fontsize=10,
                        fontweight="bold"
                    )
                    sel.annotation.get_bbox_patch().set(alpha=0.8, color="white")

                cursor_container[name] = cursor


def main() -> None:
    """Main function to run the interactive visualization."""
    
    # === Data computing ===
    data_y_path = "life_expectancy_years.csv"
    data_x_path = "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
    data_point_size_path = "population_total.csv"
    extra_data_x_path = "Gini_index.csv"
    # extra_data_y_path = "Gini_index.csv"

    data_y = pd.read_csv(data_y_path)
    data_x = pd.read_csv(data_x_path)
    data_point_size = pd.read_csv(data_point_size_path)
    extra_data_x = pd.read_csv(extra_data_x_path)
    # extra_data_y = pd.read_csv(extra_data_y_path)

    INITIAL_YEAR = 1900
    FINAL_YEAR = 2050
    years = range(INITIAL_YEAR, FINAL_YEAR + 1)

    precomputed_data, corr_log, corr_lin = precompute_data(
        years,
        data_y,
        data_x,
        data_point_size,
        extra_data_x,
        # extra_data_y
    )

    cursor_container = {"log": None, "lin": None}
    correlation_cursor_container = {"corr_log": None, "corr_lin": None}
    tracked_country = [None]

    # === Figure and Axes setup ===
    fig, axes = plt.subplot_mosaic(
        [
            ["log", "log", "log", "corr_log"],
            ["lin", "lin", "lin", "corr_lin"],
        ],
        figsize=(10, 6)
    )
    fig.subplots_adjust(
        top=0.97,
        bottom=0.1,
        left=0.05,
        right=0.95,
        hspace=0.13,
        wspace=0.2
    )

    # === Slider ===
    ax_slider = plt.axes([0.05, 0.01, 0.6, 0.03])
    year_slider = Slider(
        ax_slider,
        "Year",
        INITIAL_YEAR,
        FINAL_YEAR,
        valinit=INITIAL_YEAR,
        valstep=1,
        color="blue"
    )
    year_slider.on_changed(
        lambda slider_val:
            update(
                slider_val,
                axes,
                precomputed_data,
                cursor_container,
                tracked_country[0]
            ),
    )

    # === TextBox for country tracking ===
    ax_box_tracker = plt.axes([0.75, 0.005, 0.2, 0.05])
    text_box_tracker = TextBox(ax_box_tracker, "Track Country")
    text_box_tracker.on_submit(
        lambda text: (
            add_tracker(
                text,
                tracked_country,
                axes,
                precomputed_data,
                cursor_container,
                year_slider
            ),
            add_curve_interactivity(
                axes,
                ["corr_log", "corr_lin"],
                correlation_cursor_container
            )
        )
    )

    # === Right-side correlation graphs ===
    corr_graph_settings(axes["corr_log"], years, corr_log, "log", "red")
    corr_graph_settings(axes["corr_lin"], years, corr_lin, "lin", "green")

    # === First update call (in order to make everything work at start) ===
    update(
        INITIAL_YEAR,
        axes,
        precomputed_data,
        cursor_container,
        tracked_country[0]
    )

    add_curve_interactivity(
        axes,
        ["corr_log", "corr_lin"],
        correlation_cursor_container
    )

    plt.show()


if __name__ == "__main__":
    main()