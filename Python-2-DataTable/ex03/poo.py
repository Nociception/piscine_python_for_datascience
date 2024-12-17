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

YEAR_TEST = 2050


def cust_suffixed_string_to_float(value) -> float:
    factors = {'k': 1e3, 'M': 1e6, 'B': 1e9}
    try:
        if isinstance(value, str) and value[-1] in factors:
            return float(value[:-1]) * factors[value[-1]]
        return float(value)
    except (ValueError, TypeError):
        return np.nan


def dict_printer(
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


def get_data_name(file_name: str) -> str:
    """DOCSTRING"""
    
    # print("get_data_name")
    
    extension = file_name[file_name.index('.'):]
    return file_name[:file_name.index(extension)].replace('_', ' ')


def var_print_str(
    var_name: str,
    var_value
    ) -> str:
    """DOCSTRING"""

    return f"{var_name}:{var_value} ({type(var_value)})\n"

class LinReg:
    def __init__(self,
                 predicted: np.ndarray,
                 corr: float):
        self.predicted = predicted
        self.corr = corr

    def show(self) -> None:
        """DOCSTRING"""
        
        print("\n=== SHOW LinReg object ===")
        print(f"self.predicted:\n{self.predicted}")
        print(f"self.corr:\n{self.corr}")
        print("=== SHOW LinReg object FIN\n===")
        

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
            self.file_path: str = file_path
            self.data_name: str = get_data_name(file_path)
            self.short_name: str = short_name
            self.data_frame: pd.DataFrame = load(file_path)
        else:
            raise ValueError(
                f"Both data_type and data_type must be str, not:\n"
                f"{var_print_str('data_type', data_type)}\n"
                f"{var_print_str('file_path', file_path)}"
            )

        self.first_column_name: int | float | None = None
        self.last_column_name: int | float | None = None
        self.data_cleaned: bool = False

    def show(self) -> None:
        """DOCSTRING"""
    
        print("\n===== Show Data_Frame object =====")
        print(f"data_type: {self.data_type}")
        print(f"file_path: {self.file_path}")
        print(f"data_name: {self.data_name}")
        print(f"short_name: {self.short_name}")
        print(f"first_column_name: {self.first_column_name}")
        print(f"last_column_name: {self.last_column_name}")
        print(f"data_cleaned: {self.data_cleaned}")
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

        # if timediv == YEAR_TEST :
        #     print("=== (class DataFrame) DEBUT SUBSET_TIMEDIV_EXTRACTION ===")
        #     print(f"timediv: {timediv}")
        #     self.show()

        if timediv in range(self.first_column_name, self.last_column_name + 1):
            df_timediv = self.data_frame[
                    [common_column, str(timediv)]
                ].rename(columns={str(timediv): self.data_name})
            df_timediv[self.data_name] = df_timediv[self.data_name].apply(
                cust_suffixed_string_to_float
            )
            
            # if timediv == YEAR_TEST :
            #     print(f"timediv: {timediv}")
            #     print(f"df_timediv:\n{df_timediv}")
            #     print("=== (class DataFrame) FIN SUBSET_TIMEDIV_EXTRACTION ===\n")
        
            return df_timediv


        # if timediv == YEAR_TEST :
        #     print("Just before return None")
        #     print("=== (class DataFrame) FIN SUBSET_TIMEDIV_EXTRACTION ===\n")
        
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
        self.div: int = div

        self.lin_reg_log: LinReg | None = None
        self.lin_reg_lin: LinReg | None = None
         
        
    def show(self) -> None:
        """DOCSTRING"""
        
        print("\n=== START Show TimeDiv object ===")
        dict_printer(
            self.df_dict,
            values_type="pd.DataFrame",
            head_value=10
        )

        print(f"common_column: {self.common_column}")
        print(f"div: {self.div}")
        if self.lin_reg_log : self.lin_reg_log.show()
        if self.lin_reg_lin : self.lin_reg_lin.show()
        print(f"merged_data:\n{self.merged_data}")
        print("=== END Show TimeDiv object ===\n")
    

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


        # if self.div == YEAR_TEST:
        #     print(f"=== (class TimeDiv) DEBUT calculate_linregr DEBUT (log:{log})===")
        data_x = self.df_dict['data_x'].iloc[:, 1]
        data_y = self.df_dict['data_y'].iloc[:, 1]
        mask = ~np.isnan(data_x) & ~np.isnan(data_y)
        data_x_cleaned = data_x[mask]
        data_y_cleaned = data_y[mask]

        # if self.div == YEAR_TEST:
        #     print(f"data_x:\n{data_x}")
        #     print(f"data_y:\n{data_y}")
        #     print(f"data_x_cleaned:\n{data_x_cleaned}")
        #     print(f"data_y_cleaned:\n{data_y_cleaned}")

        if log:
            data_x_cleaned = np.log10(data_x_cleaned)

        slope, intercept, corr, _, _ = linregress(
            data_x_cleaned,
            data_y_cleaned
        )

        data_x_sorted = np.sort(data_x_cleaned)
        predicted = slope * data_x_sorted + intercept
        
        # if self.div == YEAR_TEST:
        #     print(f"slope: {slope}")
        #     print(f"intercept: {intercept}")
        #     print(f"data_x_sorted:\n{data_x_sorted}")
        #     print(f"predicted:\n{predicted}")
        #     print(f"=== (class TimeDiv) FIN calculate_linregr FIN (log:{log})===")
        
        return LinReg(predicted, corr)
        
    def linear_regressions(self) -> None:
        """DOCSTRING"""
        
        # if self.div == YEAR_TEST:
        #     print("=== (class TimeDiv) DEBUT linear_regressions DEBUT ===")
        self.lin_reg_log = self.calculate_linregr(True)
        self.lin_reg_lin = self.calculate_linregr(False)
        # if self.div == YEAR_TEST:
        #     print("=== (class TimeDiv) FIN linear_regressions FIN ===")
        
    

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

        self.corr_log: list | np.ndarray = []
        self.corr_lin: list | np.ndarray = []
        
        self.tracked_element: str = "None"

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
        
        print(f"title: {self.title}")
        print(f"data_point_size_divider: {self.data_point_size_divider}")
        print(f"x_range: {self.x_range}")
        print(f"x_label: {self.x_label}")
        print(f"y_label: {self.y_label}")
        print(f"y_unit: {self.y_unit}")
        
        print(f"common_column: {self.common_column}")
        
        
        print(f"corr_log: {self.corr_log}")
        print(f"corr_lin: {self.corr_lin}")
        
        print(f"tracked_element: {self.tracked_element}")
        
        
        
        
        
        
        print("data_frames:")
        dict_printer(self.data_frames, "cust class")
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

        # if timediv == YEAR_TEST :
        #     print("=== (class Day02Ex03) DEBUT SUBSETS_TIMEDIV_EXTRACTION ===")
        #     print(f"timediv: {timediv}")

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
        
        # if timediv == YEAR_TEST :
        #     print("=== (class Day02Ex03) FIN SUBSETS_TIMEDIV_EXTRACTION ===\n")
        
        
        return res

    def precompute_data(self):
        """DOCSTRING"""
        
        self.get_first_last_column_names()
        # self.show()
        
        for div in self.x_range:
            print(div)
            timediv = TimeDiv(
                self.subsets_timediv_extraction(div),
                self.common_column,
                div
            )
            timediv.merge()
            timediv.linear_regressions()
                
            self.precomputed_data[div] = timediv
            self.corr_log.append(timediv.lin_reg_log.corr)
            self.corr_lin.append(timediv.lin_reg_lin.corr)
            
            if div ==  YEAR_TEST:
                print(f"==============={div}=================")
                # timediv.show()
            
            
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
            self.colored_extra_data].data_name
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
        self.set_graph_meta_data(
            timediv,
            is_log_scale=is_log_scale,
            ax=ax,
            color=color,
        )
    
        if (
            ax_name in self.cursor_container
            and self.cursor_container[ax_name]
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

    def update(self) -> None:
        """DOCSTRING"""

        # print(type(self.slider))

        timediv = self.precomputed_data[int(self.slider.val)]

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
        
        self.tracked_element = text.strip()
        
        self.update()
        
        self.add_curve_interactivity()
    

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
        
        
        self.build_fig_axes()
        
        self.build_colorbar(
            ax=self.axes["log"],
            extra_data=self.data_frames['extra_data_x']
        )


        self.build_slider(
            timediv_type=timediv_type,
            update_callback_function=self.update)
        
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
    
    try:
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
            short_name="Gini coefficient"
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

        exo03.add_x_range(start=1800, stop=2050)
        exo03.add_common_column('country')
    
        exo03.clean_data_frames()

    
        exo03.precompute_data()
        # exo03.show()
        
        exo03.build_mpl_windows(
            timediv_type="year"
        )
        
        
        # exo03.update()
        
        # exo03.add_curve_interactivity()
        
        
        exo03.pltshow()
        
        
    except ValueError as error:
        print(f"{type(error).__name__}: {error}")
    # except Exception as error:
    #     print(f"An unexpected error occurred: {error}")
    
    
if __name__ == "__main__":
    main()
