# %%

import re
from typing import List, Tuple
import pandas as pd


class FileConverter:
    """
    It's designed to convert igc data that has been converted to CSV via KML. The program is designed to be used with the processed output of the following websites:

    Utilities:
    - https://igc2kml.com/
    - https://products.aspose.app/gis/conversion/kml-to-csv

    To run this script, use Jupyter Notebook and copy the following code:

    input_file: str = "/Users/nicolas/Downloads/data_file_convertor.xlsx"
    output_file: str = "/Users/nicolas/Downloads/data_file_convertor.csv"

    Converter = FileConverter(input_file, output_file)
    Converter.process_csv()
    """

    def __init__(self, excel_file: str, output_file: str) -> None:
        """
        Initializes the FileConverter class.

        Parameters:
        - excel_file: the path to the CSV file to be converted
        - output_file: the path to the CSV file to be created

        Returns:
        - None
        """
        self.excel_file: str = excel_file
        self.output_file: str = output_file

    def read_excel_file(self) -> pd.DataFrame:
        """
        Reads the Excel file and returns a Pandas DataFrame.

        Parameters:
        - None

        Returns:
        - A Pandas DataFrame
        """
        return pd.read_excel(self.excel_file)

    def filter_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the DataFrame by removing rows with 'altitudeMode' equal to 'clampToGround'.

        Parameters:
        - df: the DataFrame to be filtered

        Returns:
        - A filtered DataFrame
        """
        return df[df["altitudeMode"] != "clampToGround"]

    def split_and_reorder_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Splits the 'name' column into multiple columns and reorders the columns.

        Parameters:
        - df: the DataFrame to be filtered

        Returns:
        - A filtered DataFrame
        """
        df[["timestamp", "altitude", "horizontal", "vertical", "distance"]] = df[
            "name"
        ].str.split(expand=True)
        return df[
            ["timestamp", "altitude", "horizontal", "vertical", "distance", "WKT"]
        ]

    def remove_static_speeds(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes rows with static horizontal speed.

        Parameters:
        - df: the DataFrame to be filtered

        Returns:
        - A filtered DataFrame
        """
        return df[df["horizontal"] != "0"]

    def extract_coordinates_raw(self, row: pd.Series) -> pd.Series:
        """
        Extracts the coordinates from the 'WKT' column of the DataFrame.

        Parameters:
        - row: a row of the DataFrame

        Returns:
        - A Pandas Series containing the coordinates
        """
        line_string: str = row["WKT"]
        match: re.Match = re.search(r"\(([^)]+)", line_string)
        coordinates_str: str = match.group(1)
        coordinates: List[Tuple[str, str]] = [
            tuple(pair.split()[:2]) for pair in coordinates_str.split(",")
        ]
        return pd.Series(coordinates, index=["coordinates_a", "coordinates_b"])

    def extract_coordinates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts coordinates from the 'WKT' column and adds them to the DataFrame.

        Parameters:
        - df: the input DataFrame

        Returns:
        - DataFrame with coordinates added
        """
        df["WKT"] = df["WKT"].astype(str)
        coordinates_raw: pd.DataFrame = df.apply(self.extract_coordinates_raw, axis=1)
        df = pd.concat([df, coordinates_raw], axis=1)
        df = df.drop(["WKT", "coordinates_b"], axis=1)
        return df

    def extract_coordinates_a(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts coordinates from 'coordinates_a' column and adds 'longitude' and 'latitude' columns.

        Parameters:
        - df: the input DataFrame

        Returns:
        - DataFrame with 'longitude' and 'latitude' columns added
        """
        df["coordinates_a"] = df["coordinates_a"].astype(str)
        coordinates_a: pd.DataFrame = df["coordinates_a"].str.split(" ", expand=True)
        df["longitude"] = coordinates_a[0]
        df["latitude"] = coordinates_a[1]
        df = df.drop("coordinates_a", axis=1)
        return df

    def clean_up_coordinates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans up 'longitude' and 'latitude' columns by removing unwanted characters.

        Parameters:
        - df: the input DataFrame

        Returns:
        - DataFrame with 'longitude' and 'latitude' columns cleaned up
        """
        df["longitude"] = (
            df["longitude"].str.replace(r"[\[\]()',]", "", regex=True).astype(float)
        )
        df["latitude"] = (
            df["latitude"].str.replace(r"[\[\]()',]", "", regex=True).astype(float)
        )
        return df

    def remove_units(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes the units from the 'altitude', 'horizontal', 'vertical', and 'distance' columns of the DataFrame.

        Parameters:
        - df: input DataFrame

        Returns:
        - DataFrame with units removed
        """
        df["altitude"] = (
            df["altitude"].str.replace(r"[m]", "", regex=True).astype(float).round(2)
        )
        df["horizontal"] = (
            df["horizontal"]
            .str.replace(r"[kmh]", "", regex=True)
            .astype(float)
            .round(2)
        )
        df["vertical"] = (
            df["vertical"].str.replace(r"[m/s]", "", regex=True).astype(float).round(2)
        )
        df["distance"] = (
            df["distance"].str.replace(r"[km]", "", regex=True).astype(float).round(2)
        )
        return df

    def convert_horizontal_speed(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts horizontal speed to meters per second.

        Parameters:
        - df: the input DataFrame

        Returns:
        - DataFrame with horizontal speed converted
        """
        df["horizontal"] = (df["horizontal"] / 3.6).round(2)
        return df

    # AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
    def export_to_csv(self, df: pd.DataFrame, custom_headers: List[str]) -> None:
        """
        Exports the DataFrame to a CSV file with custom headers.

        Parameters:
        - df: the input DataFrame
        - custom_headers: a list of custom headers

        Returns:
        - None
        """
        df.to_csv(self.output_file, index=False, header=custom_headers)
        print(df)

    # AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
    def process_csv(
        self,
    ) -> None:
        """
        Converts the CSV file to a Pandas DataFrame, cleans up the data, and exports the DataFrame to a CSV file.

        Parameters:
        - None

        Returns:
        - None
        """
        df: pd.DataFrame = self.read_excel_file()

        # Process steps
        df = self.filter_dataframe(df)
        df = self.split_and_reorder_columns(df)
        df = self.remove_static_speeds(df)
        df = self.extract_coordinates(df)
        df = self.extract_coordinates_a(df)
        df = self.remove_units(df)
        df = self.convert_horizontal_speed(df)
        df = self.clean_up_coordinates(df)

        # EXPORT DATAFRAME TO CSV
        custom_headers: List[str] = [
            "timestamp [UTC]",
            "relative altitude [m]",
            "horizontal velocity [m/s]",
            "vertical velocity [m/s]",
            "distance to takeoff [km]",
            "longitude",
            "latitude",
        ]
        self.export_to_csv(df, custom_headers)


# %%
