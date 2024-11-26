from load_csv import load
from aff_life import plot_life_expectancy


def main():
    """
    Main function to load the dataset and plot life expectancy.
    """
    dataset_path = "life_expectancy_years.csv"
    dataset = load(dataset_path)
    plot_life_expectancy(dataset, "France")


if __name__ == "__main__":
    main()
