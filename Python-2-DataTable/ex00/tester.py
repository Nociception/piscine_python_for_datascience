from load_csv import load


def main() -> None:
    """Tester for the load function from load_csv.py"""
    print(load("life_expectancy_years.csv"))


if __name__ == "__main__":
    main()
