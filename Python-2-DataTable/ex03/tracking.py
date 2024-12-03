import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox
from scipy.stats import linregress
import mplcursors


def parsing_value(value):
    factors = {'k': 1e3, 'M': 1e6, 'B': 1e9}
    try:
        if isinstance(value, str) and value[-1] in factors:
            return float(value[:-1]) * factors[value[-1]]
        return float(value)
    except (ValueError, TypeError):
        return np.nan


def precalculate_data(years, data_y, data_x, data_point_size):
    precomputed = {}
    for year in years:
        year_col = str(year)

        life_expectancy_year = data_y[['country', year_col]].rename(
            columns={year_col: 'life_expectancy'}
        )
        gdp_year = data_x[['country', year_col]].rename(columns={year_col: 'gdp'})
        pop_year = data_point_size[['country', year_col]].rename(columns={year_col: 'population'})

        gdp_year['gdp'] = gdp_year['gdp'].apply(parsing_value)
        pop_year['population'] = pop_year['population'].apply(parsing_value)

        merged_data = pd.merge(life_expectancy_year, gdp_year, on='country')
        merged_data = pd.merge(merged_data, pop_year, on='country')
        merged_data = merged_data.dropna()
        precomputed[year] = merged_data

    return precomputed


def update(val, ax, slider, precomputed_data, cursor_container, tracked_country):
    year = int(slider.val)
    data = precomputed_data[year]

    ax.cla()

    scatter = ax.scatter(
        data['gdp'], data['life_expectancy'],
        s=data['population'] / 1e6, alpha=0.7, label="Countries (population-weighted)"
    )

    slope, intercept, _, _, _ = linregress(np.log10(data['gdp']), data['life_expectancy'])
    gdp_sorted = np.sort(data['gdp'])
    regression_line = slope * np.log10(gdp_sorted) + intercept

    ax.plot(gdp_sorted, regression_line, color='red', linestyle='--', label="Regression Line (log-linear)")

    if tracked_country:
        highlighted = data[data['country'].str.contains(tracked_country, case=False, na=False)]
        if not highlighted.empty:
            ax.scatter(
                highlighted['gdp'], highlighted['life_expectancy'],
                s=highlighted['population'] / 1e6, color='orange',
                label=f"Tracked: {tracked_country}", edgecolor='black'
            )

    ax.set_title(f"Life Expectancy vs GDP in {year}")
    ax.set_xlabel("Gross Domestic Product (USD, log scale)")
    ax.set_ylabel("Life Expectancy (years)")
    ax.set_xscale('log')
    ax.legend(loc="best")

    for cursor in cursor_container:
        cursor.remove()
    cursor_container.clear()

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

    cursor_container.append(cursor)
    plt.draw()


def add_tracker(text, tracked_country, ax, precomputed_data, cursor_container, slider):
    if tracked_country[0]:
        print(f"Cannot track more than one country! Currently tracking: {tracked_country[0]}")
        return
    tracked_country[0] = text.strip()
    print(f"Tracking: {tracked_country[0]}")
    update(slider.val, ax, slider, precomputed_data, cursor_container, tracked_country[0])


def main():
    data_y_path = "life_expectancy_years.csv"
    data_x_path = "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
    data_point_size_path = "population_total.csv"

    data_y = pd.read_csv(data_y_path)
    data_x = pd.read_csv(data_x_path)
    data_point_size = pd.read_csv(data_point_size_path)

    years = range(1900, 2051)
    precomputed_data = precalculate_data(years, data_y, data_x, data_point_size)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.subplots_adjust(bottom=0.35)

    initial_year = 1900
    scatter = None
    cursor_container = []
    tracked_country = [None]

    ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
    year_slider = Slider(ax_slider, "Year", 1900, 2050, valinit=1900, valstep=1, color="blue")

    ax_box = plt.axes([0.2, 0.22, 0.4, 0.05])
    text_box = TextBox(ax_box, "Track Country")

    text_box.on_submit(lambda text: add_tracker(text, tracked_country, ax, precomputed_data, cursor_container, year_slider))

    year_slider.on_changed(lambda val: update(val, ax, year_slider, precomputed_data, cursor_container, tracked_country[0]))

    update(initial_year, ax, year_slider, precomputed_data, cursor_container, tracked_country[0])
    plt.show()


if __name__ == "__main__":
    main()
