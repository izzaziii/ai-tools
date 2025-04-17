import pandas as pd
import logging
import time
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Configure logging at module level
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

class BOReport:
    def __init__(
        self, file_path: str = r"Z:\FUNNEL with PROBABILITY TRACKING_Teefa.xlsx"
    ):
        self.file_path = file_path
        self.df = self.read_file()

    def read_file(self) -> pd.DataFrame:
        """Read the Excel file and return a DataFrame."""
        start_time = time.time()
        logging.info(
            f"Started reading file {self.file_path} at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        try:
            df = pd.read_excel(self.file_path, engine="openpyxl")
            elapsed_time = time.time() - start_time
            logging.info(
                f"File {self.file_path} read successfully in {elapsed_time:.2f} seconds."
            )
            return df
        except Exception as e:
            logging.error(
                f"Error reading file {self.file_path}. Check VPN connection.\n Error: {e}"
            )
            raise


if __name__ == "__main__":
    # Logging is already configured at module level
    bo_report = BOReport()
    df = bo_report.df
    print(df.head())
