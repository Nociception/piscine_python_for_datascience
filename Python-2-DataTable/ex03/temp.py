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
            "data_x": timediv_list[0],
            "data_y": timediv_list[1],
            "data_point_size": timediv_list[2],
            "extra_data_x": timediv_list[3],
            "extra_data_y": timediv_list[4]
        }
        self.common_column = common_column
        self.div = div

        self.merged_data: pd.DataFrame | None = None
        self.lin_reg_log: LinReg | None = None
        self.lin_reg_lin: LinReg | None = None