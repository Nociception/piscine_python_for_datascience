"""
Navigate back keyboard short cut: ctrl alt -
"""

from load_csv import load
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.colorbar import Colorbar
import matplotlib.collections as mplcollec
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.widgets import Slider, TextBox
from matplotlib.colors import Normalize, LinearSegmentedColormap
from typing import Callable

from scipy.stats import linregress
import mplcursors
from fuzzywuzzy import process



class LinReg:  # A GARDER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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

# A GARDER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
        
        gini_year = None
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


def get_points_color(data: pd.DataFrame) -> list[str]:
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


def plot_scatter(
        ax: plt.Axes,
        data: pd.DataFrame,
        points_color: list[str],
        tracked_country: list[str]
        ) -> mplcollec.PathCollection:
    """DOCSTRING"""

    scatter = ax.scatter(
        data['gdp'],
        data['life_expectancy'],
        s=data['population'] / 1e6,
        c=points_color,
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
    return scatter


def plot_regressline(
        data: pd.DataFrame,
        is_log_scale: bool,
        ax: plt.Axes,
        color: str,
        year_data: Year
        ) -> None:
    """DOCSTRING"""

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


def set_graph_meta_data(
    year_data: Year,
    is_log_scale: bool,
    ax: plt.Axes,
    color: str,
    ) -> None:
    """Configure les métadonnées du graphique et gère la colorbar."""

    if is_log_scale:
        ax.set_xscale('log')
        ax.set_title(f"Life Expectancy vs Inflation-adjusted GDP per capita at purchasing power parity (PPP) in {year_data.year}")
        ax.set_xlabel("Gross Domestic Product per capita at PPP (USD, log scale)", labelpad=-5)
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


def plot(year_data: Year,
         ax: plt.Axes,
         is_log_scale: bool,
         tracked_country: list[str],
         cursor_container: dict,
         ax_name: str,
         color: str,
         ) -> None:
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
    points_color = get_points_color(data)
    scatter = plot_scatter(ax, data, points_color, tracked_country)
    plot_regressline(data, is_log_scale, ax, color, year_data)

    set_graph_meta_data(
        year_data,
        is_log_scale=is_log_scale,
        ax=ax,
        color=color,
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
           tracked_country: list,
           cbar) -> None:
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
        color="red",
    )

    plot(
        year_data=year_data,
        ax=axes["lin"],
        is_log_scale=False,
        tracked_country=tracked_country,
        cursor_container=cursor_container,
        ax_name="lin",
        color="green",
    )

    if 'gini' in year_data.data.columns:
        if not cbar.ax.get_visible():
            cbar.ax.set_visible(True)
    else:
        if cbar.ax.get_visible():
            cbar.ax.set_visible(False)

    plt.draw()


def add_tracker(text,
                tracked_country,
                ax,
                precomputed_data,
                cursor_container,
                slider,
                cbar):

    tracked_country[0] = text.strip()
    update(slider.val,
           ax,
           precomputed_data,
           cursor_container,
           tracked_country[0],
           cbar
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


def get_data_name(file_name: str) -> str:
    """DOCSTRING"""
    
    # print("get_data_name")
    
    extension = file_name[file_name.index('.'):]
    return file_name[:file_name.index(extension)].replace('_', ' ')
    

def build_colorbar_name(file_name: str) -> str:
    """DOCSTRING"""
    
    data_name = get_data_name(file_name).replace(' ', '_')
    return data_name + '_cbar'


def generate_colorbar(
    fig: plt.Figure,
    ax: plt.Axes,
    data_path: str,
    cmap_colors: list[str]=[
        "green",
        "limegreen",
        "yellow",
        "orange",
        "red",
        "magenta",
        "mediumpurple",
        "darkviolet"
    ],
    vmin: float = 0,
    vmax: float = 100,
    orientation: str = "vertical",
    label_position: str = "left",
    ticks_position: str = "left",
    pad: float = 0.05,
    fraction: float = 0.02,
    aspect: int = 50,
    labelpad: int = 1,
    nb_divs: int = 100
    ) -> plt.colorbar:
    """DOCSTRING"""

    cmap = LinearSegmentedColormap.from_list(
        name=build_colorbar_name(data_path),  
        colors=cmap_colors,
        N=nb_divs
    )

    
    norm = Normalize(vmin=vmin, vmax=vmax)

    
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  

    
    cbar = fig.colorbar(
        sm,
        ax=ax,
        orientation=orientation,
        pad=pad,
        fraction=fraction,
        aspect=aspect
    )

    cbar.set_label(
        label=data_path.replace('_', ' ').split('.')[0],
        labelpad=labelpad
    )
    cbar.ax.yaxis.set_label_position(label_position)
    cbar.ax.yaxis.set_ticks_position(ticks_position)

    return cbar


def build_figure_axes():
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
        right=0.99,
        hspace=0.13,
        wspace=0.2
    )
    return fig, axes


def build_slider(fig, years, update_callback):
    """
    Creates and returns a slider for selecting years.
    
    Args:
        fig (matplotlib.figure.Figure): The figure to add the slider to.
        years (range): The range of years for the slider.
        update_callback (callable): Function to call when the slider value changes.

    Returns:
        Slider: The created slider object.
    """
    ax_slider = fig.add_axes([0.05, 0.01, 0.6, 0.03])
    
    year_slider = Slider(
        ax_slider,
        "Year",
        years.start,
        years.stop,
        valinit=years.start,
        valstep=1,
        color="blue"
    )

    year_slider.on_changed(update_callback)
    
    return year_slider


def dict_printer( # A GARDER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    d: dict,
    values_type: str,
    head_value: int=5
    ) -> None:
    """DOCSTRING"""
    
    if d is None:
        print("The dictionnary does not exist.")
        
        return None

    if values_type == "pd.DataFrame":
        if head_value < 1:
            print("head_value must be greater than 0.")
            
            return None
        for key, value in d.items():
            if value is not None:
                print(f"{key}:\n{value.head(head_value)}\n")

    elif values_type == "cust class":
        for _, value in d.items():
            if value is not None:
                value.show()
    else:
        for key, value in d.items():
            print(f"{key}: {value}")


def var_print_str(
    var_name: str,
    var_value
    ) -> str:
    """DOCSTRING"""

    return f"{var_name}:{var_value} ({type(var_value)})\n"
    


# POO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# POO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# POO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# POO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# POO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# POO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# POO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class DataFrame:
    """DOCSTRING"""

    # === General class elements (init, show, exceptions classes) ===
    def __init__(
        self,
        data_type: str,
        file_path: str,
        short_name: str,
    ):
        """DOCSTRING"""

        if all(
            isinstance(arg, str) for arg in (
                data_type,
                file_path,
                short_name)
            ):
            self.data_type: str = data_type
            self.file_path:str = file_path
            self.data_name:str = get_data_name(file_path)
            self.data_frame:pd.DataFrame = load(file_path)
            self.short_name:str = short_name
        else:
            raise ValueError(
                f"Both data_type and data_type must be str, not:\n"
                f"{var_print_str('data_type', data_type)}\n"
                f"{var_print_str('file_path', file_path)}"
            )

        self.first_column_name: int | float | None = None
        self.last_column_name: int | float | None = None
        self.data_cleaned:bool = False

    def show(self) -> None:
        """DOCSTRING"""
    
        print("\n===== Show Data_Frame object =====")
        print(f"data_type: {self.data_type}")
        print(f"file_path: {self.file_path}")
        print(f"data_name: {self.data_name}")
        print(f"data_frame:\n{self.data_frame}")
        print("===== END Show Data_Frame object END =====\n")

    class DataFrameException(Exception):
        """DOCSTRING"""
        
        pass
    
    class DataFrameNotCleanedException(DataFrameException):
        """DOCSTRING"""
        
        def __init__(
            self,
            msg="DataFrame object still not cleaned.\n"\
                "This exception appears because something has been"\
                " attempted which needs the DataFrame to be cleaned"\
                " before."
        ):
            super().__init__(msg)

    # === Specific class elements ===
    def get_first_last_column_names(self) -> None:
        """DOCSTRING"""
        
        self.first_column_name = int(self.data_frame.columns[1])
        self.last_column_name = int(self.data_frame.columns[-1])
    
    
    def subset_timediv_extraction(
        self,
        timediv: int,
        common_column: str
    ) -> pd.DataFrame | None:
        """DOCSTRING"""

        if timediv in range(self.first_column_name, self.last_column_name):
            df_timediv = self.data_frame[
                    [common_column, str(timediv)]
                ].rename(columns={str(timediv): self.data_name})
            df_timediv[self.data_name] = df_timediv[self.data_name].apply(
                cust_suffixed_string_to_float
            )
            return df_timediv        
        return None


class TimeDiv:
    """DOCSTRING"""
    
    def __init__(
        self,
        timediv_list: list[pd.DataFrame],
        common_column: str,
        div: int
    ):
        """DOCSTRING"""
        
        self.df_dict = {
            "data_x" : timediv_list[0],
            "data_y" : timediv_list[1],
            "data_point_size" : timediv_list[2],
            "extra_data_x" : timediv_list[3],
            "extra_data_y" : timediv_list[4]
        }
        self.common_column: str=common_column
        self.merged_data: pd.DataFrame=self.df_dict['data_x']
        self.div = div
        
        self.lin_reg_log: LinReg | None = None
        self.lin_reg_lin: LinReg | None = None
         
        
    def show(self) -> None:
        """DOCSTRING"""
        
        dict_printer(
            self.df_dict,
            values_type="pd.DataFrame",
            head_value=10
        )
        print(self.merged_data)
        
    

    def safe_df_merge(
        self,
        df_left: pd.DataFrame,
        df_right: pd.DataFrame
    ) -> pd.DataFrame:
        """DOCSTRING"""
        
        if (
                df_left is not None
                and df_right is not None
            ):
                merged_data = pd.merge(
                    df_left, df_right, on=self.common_column
                )
                
                return merged_data
        else:
            return df_left

    def merge(self) -> None:
        """DOCSTRING"""

        for namedf, df in self.df_dict.items():
            if namedf != "data_x":
                self.merged_data = self.safe_df_merge(
                    self.merged_data, df
                )


    def calculate_linregr(
        self,
        log: bool
    ) -> LinReg:
        """DOCSTRING"""

        data_x = self.df_dict['data_x'].iloc[:, 1]

        if log:
            data_x = np.log10(data_x)

        slope, intercept, corr, _, _ = linregress(
            data_x,
            self.df_dict['data_y'].iloc[:, 1]
        )

        data_x_sorted = np.sort(data_x)
        predicted = slope * data_x_sorted + intercept
        
        
        return LinReg(predicted, corr)
        
    def linear_regressions(self) -> None:
        """DOCSTRING"""
        
        self.lin_reg_log = self.calculate_linregr(True)
        self.lin_reg_lin = self.calculate_linregr(False)
    

class Day02Ex03:
    """DOCSTRING"""

    def __init__(self):
        """DOCSTRING"""
        
        self.data_frames: dict[str, pd.DataFrame | None] = {
            "data_x": None,
            "data_y": None,
            "data_point_size": None,
            "extra_data_x": None,
            "extra_data_y": None,
        }
        self.title: str | None = None
        self.data_point_size_divider: int = None

        self.x_range: range | None = None
        self.x_label: str | None = None
        self.x_unit: str | None = None
        
        
        self.y_label: str | None = None
        self.y_unit: str | None = None
        
        
        self.common_column: str | None = None
        self.precomputed_data: dict[int | float, TimeDiv] = {}

        self.corr_log: list[float] | np.ndarray[float] | None = []
        self.corr_lin: list[float] | np.ndarray[float] | None = []
        
        self.tracked_element: list[str | None] = [None]

        self.cursor_container: dict[
            str, mplcursors.cursor.Cursor | None
            ] = {
            "log": None,
            "lin": None
        }
        self.correlation_cursor_container: dict[
            str, mplcursors.cursor.Cursor | None
            ] = {
            "corr_log": None,
            "corr_lin": None
        }
        # TO MERGE ?
        
        self.fig: Figure | None = None
        self.axes: dict[str, Axes] | None = None
        self.cbar: Colorbar | None = None
        self.slider: Slider | None = None
        self.ax_box_tracker: Axes | None = None
        self.text_box_tracker: TextBox | None = None
        
        # definetly set that way (adjustable in future versions)
        self.colored_extra_data: str = "extra_data_x"
        
        

    def show(self):
        """DOCSTRING"""
        
        print("\n=== Show Day02Ex03 object ===")
        
        print("data_frames:")
        # dict_printer(self.data_frames, "cust class")
        
        # print(f"x_range: {self.x_range}")
        
        print("=== END Show Day02Ex03 object END ===\n")


    def add_data_path(
        self,
        data_path: str,
        data_type: str,
        short_name: str
    ) -> None:
        """DOCSTRING"""
        
        if (
            all(isinstance(arg, str) for arg in (
                data_path,
                data_type,
                short_name
                )
            )
            and len(data_path) >= 3
        ):
            self.data_frames[data_type] = DataFrame(
                data_type,
                data_path,
                short_name
            )
        else:
            raise ValueError(
                f"data_path (min length 3),"
                f"data_type and short_name must be str, not:\n"
                f"{var_print_str('data_path', data_path)}\n"
                f"{var_print_str('data_type', data_type)}\n"
                f"{var_print_str('data_type', short_name)}"
            )

    def add_data_x_path(
        self,
        data_x_path: str,
        short_name: str,
        x_label: str,
        x_unit: str
    ) -> None:
        """DOCSTRING"""

        if all(
            isinstance(arg, str) for arg in (
                x_label,
                x_unit,
            )
        ):
            self.add_data_path(
                data_x_path,
                "data_x",
                short_name
            )
            self.x_label = x_label
            self.x_unit = x_unit
        else:
            raise ValueError(
                f"x_label and x_name must be str, not:\n"
                f"{var_print_str('x_label', x_label)}\n"
                f"{var_print_str('x_unit', x_unit)}\n"
            )

    def add_data_y_path(
        self,
        data_y_path: str,
        short_name: str,
        y_label: str,
        y_unit: str
    ) -> None:
        """DOCSTRING"""

        if all(
            isinstance(arg, str) for arg in (
                y_label,
                y_unit,
            )
        ):
            self.add_data_path(
                data_y_path,
                "data_y",
                short_name
            )
            self.y_label = y_label
            self.y_unit = y_unit
        else:
            raise ValueError(
                f"y_label and y_name must be str, not:\n"
                f"{var_print_str('y_label', y_label)}\n"
                f"{var_print_str('y_unit', y_unit)}\n"
            )

    def add_data_point_size_path(
        self,
        data_point_size_path: str,
        short_name: str,
        divider: int | float
    ) -> None:
        """DOCSTRING"""

        if isinstance(divider, (int, float)):
            self.data_point_size_divider = divider
            self.add_data_path(
                data_point_size_path,
                "data_point_size",
                short_name
            )
        else:
            raise TypeError(
                f"divider must be an int or a float, not {divider}"
            )

    def add_extra_data_x_path(
        self,
        extra_data_x_path: str,
        short_name: str
    ) -> None:
        """DOCSTRING"""

        self.add_data_path(
            extra_data_x_path,
            "extra_data_x",
            short_name
        )

    def add_extra_data_y_path(
        self,
        extra_data_y_path: str,
        short_name: str
    ) -> None:
        """DOCSTRING"""

        self.add_data_path(
            extra_data_y_path,
            "extra_data_y",
            short_name
        )

    def add_title(
        self,
        title: str
    ) -> None:
        """DOCSTRING"""
        
        if isinstance(title, str):
            self.title = title
        else:
            raise ValueError(
                f"title must be a string, not {title} ({type(title)})"
            )

    def add_x_range(
        self,
        start: int,
        stop: int
    ) -> None:
        """DOCSTRING"""
        
        if all(isinstance(var, int) for var in (start, stop)):
            self.x_range = range(start, stop + 1)
        else:
            raise ValueError(
                f"start and stop must be int, not {start} and {stop}"
            )

    def add_common_column(
        self,
        common_column: str
    ) -> None:
        """DOCSTRING"""
    
        if isinstance(common_column, str):
            self.common_column = common_column

    
    def clean_data_x(self) -> None:
        """DOCSTRING"""

        df = self.data_frames['data_x']
        if df is not None:
            df.data_frame.sort_values(
                by=self.common_column
                ).reset_index(drop=True)
            df.data_cleaned = True

    def clean_data_y(self) -> None:
        """DOCSTRING"""

        df = self.data_frames['data_y']
        if df is not None:
            df.data_frame.sort_values(
                by=self.common_column
                ).reset_index(drop=True)
            df.data_cleaned = True

    def clean_data_point_size(self) -> None:
        """DOCSTRING"""

        df = self.data_frames['data_point_size']
        if df is not None:
            df.data_frame.sort_values(
                by=self.common_column
                ).reset_index(drop=True)
            df.data_cleaned = True

    def clean_extra_data_x(self) -> None:
        """DOCSTRING"""

        if self.data_frames['extra_data_x'] is not None:
            df = self.data_frames['extra_data_x'].data_frame
            df = df.drop(
                columns=[
                    "Country Code",
                    "Indicator Name",
                    "Indicator Code",
                    "Unnamed: 68"
                ],
                errors="ignore"
            )
            df = df.rename(
                columns={"Country Name": self.common_column}
            )

            data_y_countries = self.data_frames[
                'data_x'
                ].data_frame[self.common_column].unique()
            
            def match_country_name(country):
                """DOCSTRING"""
                
                match, score = process.extractOne(country, data_y_countries)
                return match if score >= 80 else None

            df[self.common_column] = df[self.common_column].apply(
                match_country_name
            )

            df = df.dropna(subset=[self.common_column])
            df = df.drop_duplicates(
                subset=[self.common_column],
                keep="first"
            )
            df = df.sort_values(
                by=self.common_column).reset_index(drop=True)
            
            self.data_frames['extra_data_x'].data_frame = df
            self.data_frames['extra_data_x'].data_cleaned = True
            
    def clean_extra_data_y(self) -> None:
        """DOCSTRING"""
    
        if self.data_frames['extra_data_y'] is not None:
            self.data_frames['extra_data_y'].data_cleaned = True

    def clean_data_frames(self) -> None:
        """DOCSTRING"""
        
        self.clean_data_x()
        self.clean_data_y()
        self.clean_data_point_size()
        self.clean_extra_data_x()
        self.clean_extra_data_y()

    def get_first_last_column_names(self) -> None:
        """DOCSTRING"""
        
        for key, data_frame in self.data_frames.items():
            if data_frame is None:
                continue
            if not data_frame.data_cleaned:
                raise data_frame.DataFrameNotCleanedException(
                    f"The DataFrame '{key}' has not been cleaned."
                )
            data_frame.get_first_last_column_names()
            # print(f"First column in '{key}': {data_frame.first_column_name}")
            # print(f"Last column in '{key}': {data_frame.last_column_name}")

    def subsets_timediv_extraction(
        self,
        timediv: int,
    ) -> list[pd.DataFrame]:
        """DOCSTRING"""

        res = list()
        for df in self.data_frames.values():
            if df is not None:
                res.append(
                    df.subset_timediv_extraction(
                        timediv,
                        self.common_column
                    )
                )
            else:
                res.append(None)
        
        return res

    def precompute_data(self):
        """DOCSTRING"""
        
        self.get_first_last_column_names()
        
        for div in self.x_range:
            # print(div)
            timediv = TimeDiv(
                self.subsets_timediv_extraction(div),
                self.common_column,
                div
            )
            timediv.merge()
            timediv.linear_regressions()
            if div >=  2049:
                print(f"==============={div}=================")
                timediv.show()
                
            
            self.precomputed_data[div] = timediv
            self.corr_log.append(timediv.lin_reg_log.corr)
            self.corr_lin.append(timediv.lin_reg_lin.corr)
            
        self.corr_log = np.array(self.corr_log)
        self.corr_lin = np.array(self.corr_lin)
        

    def build_fig_axes(self) -> None:
        """DOCSTRING"""

        self.fig, self.axes = plt.subplot_mosaic(
            [
                ["log", "log", "log", "corr_log"],
                ["lin", "lin", "lin", "corr_lin"],
            ],
            figsize=(10, 6)
        )
        self.fig.subplots_adjust(
            top=0.97,
            bottom=0.1,
            left=0.05,
            right=0.99,
            hspace=0.13,
            wspace=0.2
        )

    def build_colorbar(
        self,
        ax: Axes,
        extra_data: DataFrame,
    ) -> None:
        """DOCSTRING"""
        
        cmap_colors: list[str] = [
            "green",
            "limegreen",
            "yellow",
            "orange",
            "red",
            "magenta",
            "mediumpurple",
            "darkviolet"
        ]
        vmin: float = 0
        vmax: float = 100
        orientation: str = "vertical"
        label_position: str = "left"
        ticks_position: str = "left"
        pad: float = 0.05
        fraction: float = 0.02
        aspect: int = 50
        labelpad: int = 1
        nb_divs: int = 100

        cmap = LinearSegmentedColormap.from_list(
            name=extra_data.data_name,
            colors=cmap_colors,
            N=nb_divs
        )
        norm = Normalize(vmin=vmin, vmax=vmax)
        sm = ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        
        self.cbar = self.fig.colorbar(
            sm,
            ax=ax,
            orientation=orientation,
            pad=pad,
            fraction=fraction,
            aspect=aspect
        )
        self.cbar.set_label(
            label=extra_data.data_name,
            labelpad=labelpad
        )
        self.cbar.ax.yaxis.set_label_position(label_position)
        self.cbar.ax.yaxis.set_ticks_position(ticks_position)

    def get_points_color(
        self,
        data: pd.DataFrame
    ) -> list[str]:
        """DOCSTRING (extra_data_x)"""

        extra_data_colored_name = self.data_frames[
            self.extra_data_colored].data_name
        if extra_data_colored_name in data.columns:
            colors = ["green", "yellow", "orange", "red", "purple"]
            gray = (0.5, 0.5, 0.5, 1.0)
            cmap = LinearSegmentedColormap.from_list(
                "cmap_name",
                colors,
                N=100
            )
            # gini_values = data['gini']
            colored_extra_data_values = data[extra_data_colored_name]
            norm = Normalize(vmin=0, vmax=100)
            colors = [
                cmap(norm(g)) if not np.isnan(g) else gray
                for g in colored_extra_data_values
            ]
        else:
            colors = ['blue'] * len(data)

        return colors

    def plot_scatter(
        self,
        ax: Axes,
        data: pd.DataFrame,
        points_color: list[str],
    ) -> mplcollec.PathCollection:
        """DOCSTRING"""

        pt_size_s_name = self.data_frames["data_point_size"].short_name
        scatter = ax.scatter(
            data[self.data_frames["data_x"].data_name],
            data[self.data_frames["data_y"].data_name],
            s=data[
                self.data_frames["data_point_size"].data_name
                ] / self.data_point_size_divider,
            c=points_color,
            alpha=0.7,
            label=f"{self.common_column.title()} ({pt_size_s_name}-sized)"
        )
        
        if self.tracked_element:
            highlighted = data[
                data[self.common_column].str.contains(
                    self.tracked_element,
                    case=False,
                    na=False
                )
            ]
            if not highlighted.empty:
                ax.scatter(
                    highlighted[self.data_frames["data_x"].data_name],
                    highlighted[self.data_frames["data_y"].data_name],
                    s=highlighted[
                        self.data_frames["data_point_size"].data_name
                        ] / self.data_point_size_divider,
                    color='cyan',
                    label=f"Tracked: {self.tracked_element}",
                    edgecolor='black'
            )
        return scatter

    def plot_regressline(
            self,
            timediv: TimeDiv,
            is_log_scale: bool,
            ax: Axes,
            color: str            
    ) -> None:
        """DOCSTRING"""

        regression = (
            timediv.lin_reg_log
            if is_log_scale
            else timediv.lin_reg_lin
        )
        
        reg_line_type = 'log-linear' if is_log_scale else 'linear'
        ax.plot(
            np.sort(
                timediv.merged_data[self.data_frames["data_x"].data_name]
            ),
            regression.predicted,
            color=color,
            linestyle='--',
            label=f"Regression Line ({reg_line_type})"
                  f" - Corr: {regression.corr:.2f}"
        )

    def set_graph_meta_data(
        self,
        timediv: TimeDiv,
        is_log_scale: bool,
        ax: Axes,
        color: str
    ) -> None:
        """DOCSTRING"""

        if is_log_scale:
            ax.set_xscale('log')
            ax.set_title(f"{self.title} in {timediv.div}")
            ax.set_xlabel(
                f"{self.x_label} ({self.x_unit}, log scale)",
                labelpad=-5
            )
        else:
            ax.set_xlabel(f"{self.x_label} ({self.x_unit})")
        ax.set_ylabel(f"{self.y_label} ({self.y_unit})")
        
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

    def plot(  # STILL TOO LARGE
        self,
        timediv: TimeDiv,
        ax: Axes,
        is_log_scale: bool,
        ax_name: str,
        color: str
    ) -> None:
        """DOCSTRING"""

        data = timediv.merged_data
        points_color = self.get_points_color(data)
        scatter = self.plot_scatter(
            ax,
            data,
            points_color)
        self.plot_regressline(
            timediv,
            is_log_scale,
            ax,
            color,
        )
        set_graph_meta_data(
            timediv,
            is_log_scale=is_log_scale,
            ax=ax,
            color=color,
        )
    
        if (
            ax_name in self.cursor_container
            and self.cursor_container[ax.name]
        ):
            try:
                self.cursor_container[ax_name].remove()
                self.cursor_container[ax_name] = None
            except Exception as e:
                print(
                    f"Warning: Failed to remove cursor on "
                    f"{ax_name}: {e}"
                )
        
        cursor = mplcursors.cursor(
            scatter,
            hover=True
        )
        
        def put_kmb_suffix(val: int) -> str:
            """
            Formats a large number with 'k', 'M', or 'B' suffixes.
            """
            for threshold, suffix in [
                (1e9, 'B'), (1e6, 'M'), (1e3, 'k')
                ]:
                if val > threshold:
                    return f"{val / threshold:.2f}{suffix}"
            return str(val)
    
        @cursor.connect("add")
        def on_add(sel):
            idx = sel.index
            row = data.iloc[idx]

            data_x_name = data[self.data_frames["data_x"].data_name]
            data_y_name = data[self.data_frames["data_y"].data_name]
            data_point_size_name = data[
                self.data_frames["data_point_size"].data_name
            ]
            extra_data_x_text = 'N/A'
            extra_data_x_name = data[
                self.data_frames["extra_data_x"].data_name
            ]
            
            if extra_data_x_name in row:
                extra_data_x_value = row[extra_data_x_name]
                if extra_data_x_value == extra_data_x_value:
                    extra_data_x_text = extra_data_x_value

            sel.annotation.set(
                text=(
                    f"{row[self.common_column]}\n"
                    
                    f"{self.data_frames['data_x'].short_name}: "
                    f"{put_kmb_suffix(row[data_x_name])} "
                    f"{self.x_unit}\n"
                    
                    f"{self.data_frames['data_y'].short_name}: "
                    f"{row[data_y_name]:.1f} "
                    f"{self.y_unit}\n"
                    
                    f"{self.data_frames['data_point_size'].short_name}: "
                    f"{put_kmb_suffix(row[data_point_size_name])}\n"
                    
                    f"{self.data_frames['extra_data_x'].short_name}:"
                    f"{extra_data_x_text}"
                ),
                fontsize=10,
                fontweight="bold"
            )
            sel.annotation.get_bbox_patch().set(alpha=0.6, color="white")

        self.cursor_container[ax_name] = cursor

    def update(
        self,
    ) -> None:
        """DOCSTRING"""

        print("DEBUT UPDATE FUNCTION")
        print(type(self.slider))

        timediv = self.precomputed_data[self.slider.val]

        self.axes["log"].cla()
        self.axes["lin"].cla()

        self.plot(
            timediv=timediv,
            ax=self.axes['log'],
            is_log_scale=True,
            ax_name="log",
            color="red"
        )
        self.plot(
            timediv=timediv,
            ax=self.axes['lin'],
            is_log_scale=False,
            ax_name="lin",
            color="green"
        )

        extra_data_x_name = self.data_frames["extra_data_x"].data_name
        if extra_data_x_name in timediv.merged_data.columns:
            if not self.cbar.ax.get_visible():
                self.cbar.ax.set_visible(True)
        else:
            if self.cbar.ax.get_visible():
                self.cbar.ax.set_visible(False)

        plt.draw()

        print("FIN UPDATE FUNCTION")


    def build_slider(
        self,
        timediv_type: str,
        update_callback_function: Callable
    ) -> None:
        """DOCSTRING"""

        ax_slider = self.fig.add_axes([0.05, 0.01, 0.6, 0.03])
    
        self.slider = Slider(
            ax_slider,
            timediv_type.title(),
            self.x_range.start,
            self.x_range.stop,
            valinit=self.x_range.start,
            valstep=1,
            color="blue"
        )
        self.slider.on_changed(update_callback_function)


    def add_curve_interactivity(
        self,
    ) -> None:
        """DOCSTRING"""
        
        for name in ["corr_log", "corr_lin"]:
            if name in self.axes:
                ax = self.axes[name]

                if name in self.correlation_cursor_container and self.correlation_cursor_container[name]:
                    try:
                        self.correlation_cursor_container[name].remove()
                        self.correlation_cursor_container[name] = None
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

                    self.correlation_cursor_container[name] = cursor


    def add_tracker(
        self,
        text: str
    ) -> None:
        """DOCSTRING"""
        
        self.tracked_element[0] = text.strip()
        
        self.update()
        
        self.add_curve_interactivity(
            ["corr_log", "corr_lin"]
        )
    

    def build_tracker(self) -> None:
        """DOCSTRING"""
        
        self.ax_box_tracker = self.fig.add_axes([0.79, 0.005, 0.2, 0.05])
        self.text_box_tracker = TextBox(
            self.ax_box_tracker,
            f"Track {self.common_column}"
        )
        
        self.text_box_tracker.on_submit(self.add_tracker)


    def plot_corr_graph(
        self,
        ax: Axes,
        corr: np.ndarray[float],
        label: str,
        color: str
    ) -> None:
        """DOCSTRING"""
        
        ax.plot(
            np.array(self.x_range),
            corr,
            label=f"{label} correlation",
            color=color
        )

        ax.set_xlabel(self.x_unit, labelpad=0)
        ax.set_xlim(self.x_range.start, self.x_range.stop - 1)
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


    def build_mpl_windows(
        self,
        timediv_type: str
    ) -> None:
        """DOCSTRING"""
        
        print("DEBUT BUILD_MPL_WINDOWS FUNCTION")
        
        self.build_fig_axes()
        
        self.build_colorbar(
            ax=self.axes["log"],
            extra_data=self.data_frames['extra_data_x']
        )


        print(f"AVANT: {type(self.slider)}")
        self.build_slider(
            timediv_type=timediv_type,
            update_callback_function=self.update)
        print(f"APRES: {type(self.slider)}")
        
        self.build_tracker()
            
        self.plot_corr_graph(
            self.axes["corr_log"],
            self.corr_log,
            "log",
            "red"
        )
        self.plot_corr_graph(
            self.axes["corr_lin"],
            self.corr_lin,
            "lin",
            "green"
        )
        
        print("FIN BUILD_MPL_WINDOWS FUNCTION")
        

    def pltshow(self) -> None:
        """DOCSTRING"""
        
        if self.fig is not None:
            plt.show()
        else:
            raise RuntimeError(
                "Figure not initialized."
                " Make sure build_figure_axes Day02Ex03"
                "method has beed called before."
            )







def main() -> None:
    """Main function to run the interactive visualization."""
    
    SWITCH = 0
    
    try:
        if not SWITCH:
            exo03 = Day02Ex03()
        
            exo03.add_data_x_path(
                "income_per_person_gdppercapita_ppp_inflation_adjusted.csv",
                short_name="GDP per capita",
                x_label="Gross Domestic Product per capita at PPP",
                x_unit="USD"
            )
            exo03.add_data_y_path(
                "life_expectancy_years.csv",
                short_name="life_expectancy",
                y_label="Life expectancy",
                y_unit="year"
            )
            exo03.add_data_point_size_path(
                "population_total.csv",
                short_name="population",
                divider=1e6
            )
            exo03.add_extra_data_x_path(
                "Gini_coefficient.csv",
                short_name="Gini Coefficient"
            )
            # exo03.add_extra_data_y_path(
            #     "",
            #     short_name=""
            # )
            exo03.add_title(
                "Life Expectancy"\
                " VS "\
                "Inflation-adjusted GDP per capita "\
                "at purchasing power parity (PPP)"
            )

            exo03.add_x_range(start=1900, stop=2049)
            exo03.add_common_column('country')
        
            exo03.clean_data_frames()
            exo03.precompute_data()
            
            exo03.build_mpl_windows(
                timediv_type="year"
            )
            
            
            exo03.update()
            
            exo03.add_curve_interactivity()
            
            # exo03.show()
            
            exo03.pltshow()
        
        
    except ValueError as error:
        print(f"{type(error).__name__}: {error}")
    # except Exception as error:
    #     print(f"An unexpected error occurred: {error}")
    
    if SWITCH:
        # === Data computing ===
        data_y_path = "life_expectancy_years.csv"
        data_x_path = "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
        data_point_size_path = "population_total.csv"
        extra_data_x_path = "Gini_coefficient.csv"
        # extra_data_y_path = "Gini_coefficient.csv"

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
        fig, axes = build_figure_axes()
        
        cbar = generate_colorbar(
            fig=fig,
            ax=axes["log"],
            data_path=extra_data_x_path,
        )

        year_slider = build_slider(
            fig,
            years,
            lambda slider_val: update(
                slider_val,
                axes,
                precomputed_data,
                cursor_container,
                tracked_country[0],
                cbar
            )
        )
    ##################################################################################

        # === TextBox for country tracking ===
        ax_box_tracker = fig.add_axes([0.79, 0.005, 0.2, 0.05])
        text_box_tracker = TextBox(ax_box_tracker, "Track Country")
        text_box_tracker.on_submit(
            lambda text: (
                add_tracker(
                    text,
                    tracked_country,
                    axes,
                    precomputed_data,
                    cursor_container,
                    year_slider,
                    cbar
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
            slider_val=years.start,
            axes=axes,
            precomputed_data=precomputed_data,
            cursor_container=cursor_container,
            tracked_country=tracked_country[0],
            cbar=cbar
        )

        add_curve_interactivity(
            axes,
            ["corr_log", "corr_lin"],
            correlation_cursor_container
        )

        plt.show()


if __name__ == "__main__":
    main()