from core.ols import OLS
import pandas as pd


def export_ols_data_to_csv(start_date: str, end_date: str, file_path: str):
    """
    Export OLS data to a CSV file.

    :param start_date: Start date for the data retrieval in YYYY-MM-DD format.
    :param end_date: End date for the data retrieval in YYYY-MM-DD format.
    :param file_path: Path to save the CSV file.
    """
    ols = OLS()
    df = ols.get_ols_dataframe(start_date=start_date, end_date=end_date)

    # Save DataFrame to CSV
    df.to_csv(file_path, index=False)
    print(f"Data exported to {file_path}")


def get_ols_dataframe(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch OLS data from Google Analytics 4 and return it as a DataFrame.

    :param start_date: Start date for the data retrieval in YYYY-MM-DD format.
    :param end_date: End date for the data retrieval in YYYY-MM-DD format.
    :return: DataFrame containing the OLS data.
    """
    ols = OLS()
    df = ols.get_ols_dataframe(start_date=start_date, end_date=end_date)
    return df
