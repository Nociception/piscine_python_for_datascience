import pandas as pd
from pandas import DataFrame


def load(path: str) -> DataFrame | None:
    """
    Loads a CSV file, prints its dimensions,
    and returns its content as a DataFrame.

    Args:
        path (str): The file path to the CSV.

    Returns:
        DataFrame | None: The loaded dataset or None if an error occurred.
    """

    try:
        if not path.endswith(".csv"):
            raise ValueError("The file must be a CSV.")

        data = pd.read_csv(path)

        # print(f"Loading dataset of dimensions {data.shape}")
        # Deactivated for this exercise

        return data

    except FileNotFoundError:
        print(f"Error: File not found at path '{path}'.")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None
