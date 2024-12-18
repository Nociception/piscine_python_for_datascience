    # def __init__(self):
    #     """DOCSTRING"""
        
    #     self.data_frames: dict[str, pd.DataFrame | None] = {
    #         "data_x": None,
    #         "data_y": None,
    #         "data_point_size": None,
    #         "extra_data_x": None,
    #         "extra_data_y": None,
    #     }
    #     self.title: str | None = None
    #     self.data_point_size_divider: int = None





    #     self.x_range: range | None = None
    #     self.x_label: str | None = None
    #     self.x_unit: str | None = None
        
        
    #     self.y_label: str | None = None
    #     self.y_unit: str | None = None
        
        
    #     self.common_column: str | None = None
    #     self.precomputed_data: dict[int | float, TimeDiv] = {}

    #     self.corr_log: list | np.ndarray = []
    #     self.corr_lin: list | np.ndarray = []
        
    #     self.tracked_element: str = "None"

    #     self.cursor_container: dict[
    #         str, mplcursors.cursor.Cursor | None
    #         ] = {
    #         "log": None,
    #         "lin": None
    #     }
    #     self.correlation_cursor_container: dict[
    #         str, mplcursors.cursor.Cursor | None
    #         ] = {
    #         "corr_log": None,
    #         "corr_lin": None
    #     }
    #     # TO MERGE ?
        
    #     self.fig: Figure | None = None
    #     self.axes: dict[str, Axes] | None = None
    #     self.cbar: Colorbar | None = None
    #     self.slider: Slider | None = None
    #     self.ax_box_tracker: Axes | None = None
    #     self.text_box_tracker: TextBox | None = None
        
    #     # definetly set that way (adjustable in future versions)
    #     self.colored_extra_data: str = "extra_data_x"