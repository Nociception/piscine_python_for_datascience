import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox
from scipy.stats import linregress
import mplcursors


def parsing_value(value) -> float:
    factors = {'k': 1e3, 'M': 1e6, 'B': 1e9}
    try:
        if isinstance(value, str) and value[-1] in factors:
            return float(value[:-1]) * factors[value[-1]]
        return float(value)
    except (ValueError, TypeError):
        return np.nan


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
        """DOCSTRING"""
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
        predicted_life_expectancy = slope * np.log10(gdp_sorted) + intercept

        # if not log:
        #     print(f"slope: {slope}; intercept: {intercept}; corr: {corr}")

        return LinReg(predicted_life_expectancy, corr)


    def linear_regressions(self) -> None:
        """DOCSTRING"""
        self.lin_reg_log = self.calculate_linregr(True)
        self.lin_reg_lin = self.calculate_linregr(False)


def precompute_data(years: range,
                    data_y: pd.DataFrame,
                    data_x: pd.DataFrame,
                    data_point_size: pd.DataFrame) -> dict[str:Year]:
    """DOCSTRING"""

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

        gdp_year['gdp'] = gdp_year['gdp'].apply(parsing_value)
        pop_year['population'] = pop_year['population'].apply(parsing_value)

        # ===== Subsets merge =====
        merged_data = pd.merge(life_expectancy_year, gdp_year, on='country')
        merged_data = pd.merge(merged_data, pop_year, on='country')
        merged_data = merged_data.dropna()

        year_object = Year(year, merged_data)
        year_object.linear_regressions()

        precomputed_data[year] = year_object
        corr_log.append(year_object.lin_reg_log.corr)
        corr_lin.append(year_object.lin_reg_lin.corr)

    return precomputed_data, np.array(corr_log), corr_lin


def plot(year_data,
         ax,
         is_log_scale,
         tracked_country,
         cursor_container,
         ax_name):
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

    scatter = ax.scatter(
        data['gdp'],
        data['life_expectancy'],
        s=data['population'] / 1e6,
        alpha=0.7,
        label="Countries (population-weighted)"
    )

    regression = year_data.lin_reg_log if is_log_scale else year_data.lin_reg_lin
    ax.plot(
        np.sort(data['gdp']),
        regression.predicted,
        color='red',
        linestyle='--',
        label=f"Regression Line ({'log-linear' if is_log_scale else 'linear'}) - Corr: {regression.corr:.2f}"
    )

    if tracked_country:
        highlighted = data[data['country'].str.contains(tracked_country, case=False, na=False)]
        if not highlighted.empty:
            ax.scatter(
                highlighted['gdp'],
                highlighted['life_expectancy'],
                s=highlighted['population'] / 1e6,
                color='orange',
                label=f"Tracked: {tracked_country}",
                edgecolor='black'
            )

    if is_log_scale:
        ax.set_xscale('log')
        ax.set_title(f"Life Expectancy vs Inflation-adjusted GDP per capita at purchasing power parity (PPP) in {year_data.year}")
        ax.set_xlabel(
            "Gross Domestic Product (USD, log scale)",
            labelpad=-5)
    else:
        ax.set_xlabel("Gross Domestic Product (USD)")
    ax.set_ylabel("Life Expectancy (years)")
    
    ax.legend(loc="best")

    ax.text(
        0.5,
        0.5,
        "LOG" if is_log_scale else "LINEAR",
        transform=ax.transAxes,
        fontsize=100,
        color="gray",
        alpha=0.08,
        ha="center", va="center",
        weight="bold",
    )

    if ax_name in cursor_container and cursor_container[ax_name]:
        cursor_container[ax_name].remove()

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
        sel.annotation.set(
            text=(
                f"{row['country']}\n"
                f"Life Expectancy: {row['life_expectancy']:.1f} years\n"
                f"GDP: {put_kmb_suffix(row['gdp'])}\n"
                f"Population: {put_kmb_suffix(row['population'])}"
            ),
            fontsize=10, fontweight="bold"
        )
        sel.annotation.get_bbox_patch().set(alpha=0.6, color="white")

    cursor_container[ax_name] = cursor




def update(val, axes, slider, precomputed_data, cursor_container, tracked_country):
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
    year = int(slider.val)
    year_data = precomputed_data[year]

    axes["log"].cla()
    axes["lin"].cla()

    plot(
        year_data=year_data,
        ax=axes["log"],
        is_log_scale=True,
        tracked_country=tracked_country,
        cursor_container=cursor_container,
        ax_name="log"
    )

    plot(
        year_data=year_data,
        ax=axes["lin"],
        is_log_scale=False,
        tracked_country=tracked_country,
        cursor_container=cursor_container,
        ax_name="lin"
    )

    plt.draw()



def add_tracker(text,
                tracked_country,
                ax,
                precomputed_data,
                cursor_container,
                slider):

    tracked_country[0] = text.strip()
    print(f"Tracking: {tracked_country[0]}")
    update(slider.val, ax, slider, precomputed_data, cursor_container, tracked_country[0])




def add_curve_interactivity(axes, correlation_axes):
    """
    Add interactivity to the correlation curves, showing the closest point on hover.
    Args:
        axes (dict): Dictionary of axes.
        correlation_axes (list): List of axes names to target for interactivity.
    """
    for name in correlation_axes:
        if name in axes:
            ax = axes[name]
            for line in ax.get_lines():  
                cursor = mplcursors.cursor(
                    line, hover=True  
                )

                @cursor.connect("add")
                def on_add(sel):
                    x, y = sel.target
                    sel.annotation.set(
                        text=f"Year: {x:.0f}\nCorr: {y:.2f}",
                        fontsize=10,
                        fontweight="bold"
                    )
                    sel.annotation.get_bbox_patch().set(alpha=0.8, color="white")

def main() -> None:

    
    data_y_path = "life_expectancy_years.csv"
    data_x_path = "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
    data_point_size_path = "population_total.csv"

    data_y = pd.read_csv(data_y_path)
    data_x = pd.read_csv(data_x_path)
    data_point_size = pd.read_csv(data_point_size_path)

    INITIAL_YEAR = 1900
    FINAL_YEAR = 2050
    years = range(INITIAL_YEAR, FINAL_YEAR + 1)

    precomputed_data, corr_log, corr_lin = precompute_data(
        years,
        data_y,
        data_x,
        data_point_size
    )

    cursor_container = {"log": None, "lin": None}

    tracked_country = [None]

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

    ax_slider = plt.axes([0.05, 0.01, 0.6, 0.03])
    year_slider = Slider(
        ax_slider,
        "Year",
        INITIAL_YEAR,
        FINAL_YEAR,
        valinit=INITIAL_YEAR,
        valstep=1,
        color="blue")

    year_slider.on_changed(
        lambda val: update(
            val,
            axes,
            year_slider,
            precomputed_data,
            cursor_container,
            tracked_country[0]
        )
    )


    ax_box_tracker = plt.axes([0.75, 0.01, 0.2, 0.05])
    text_box_tracker = TextBox(ax_box_tracker, "Track Country")
    text_box_tracker.on_submit(
        lambda text: add_tracker(
            text,
            tracked_country,
            axes,
            precomputed_data,
            cursor_container,
            year_slider)
    )


    axes["corr_log"].plot(
        np.array(years),
        corr_log,
        label="Log-Linear Correlation",
        color="blue"
    )
    axes["corr_log"].set_xlabel("Year")
    axes["corr_log"].set_ylabel("Correlation Coefficient")
    axes["corr_log"].set_xlim(INITIAL_YEAR, FINAL_YEAR)
    axes["corr_log"].set_ylim(min(corr_log) - 0.1, max(corr_log) + 0.1)
    axes["corr_log"].text(
        0.5,
        0.5,
        "LOG",
        transform=axes["corr_log"].transAxes,
        fontsize=30,
        color="gray",
        alpha=0.08,
        ha="center", va="center",
        weight="bold",
    )
    axes["corr_log"].legend()

    axes["corr_lin"].plot(
        np.array(years),
        corr_lin,
        label="Linear Correlation",
        color="green"
    )
    axes["corr_lin"].set_xlabel("Year")
    axes["corr_lin"].set_ylabel("Correlation Coefficient")
    axes["corr_lin"].set_xlim(INITIAL_YEAR, FINAL_YEAR)
    axes["corr_lin"].set_ylim(min(corr_lin) - 0.1, max(corr_lin) + 0.1)
    axes["corr_lin"].text(
        0.5,
        0.5,
        "LIN",
        transform=axes["corr_lin"].transAxes,
        fontsize=30,
        color="gray",
        alpha=0.08,
        ha="center", va="center",
        weight="bold",
    )
    axes["corr_lin"].legend()


    """
        ax.text(
        0.5,
        0.5,
        "LOG" if is_log_scale else "LINEAR",
        transform=ax.transAxes,
        fontsize=100,
        color="gray",
        alpha=0.08,
        ha="center", va="center",
        weight="bold",
    )
    """


    update(
        INITIAL_YEAR,
        axes,
        year_slider,
        precomputed_data,
        cursor_container,
        tracked_country[0])
    

    

    add_curve_interactivity(
        axes,
        correlation_axes=["corr_log", "corr_lin"]
    )

    
    plt.show()


if __name__ == "__main__":
    main()
