# %%

import pandas as pd
import re


class FileConverter:
    """
    It's designed to convert igc data that has been converted to CSV via KML using https://igc2kml.com/ and https://products.aspose.app/gis/conversion/kml-to-csv. The CSV data must be converted to Excel first in order to be used in this program, which is a manual process.

    To run this script, use Jupyter Notebook and copy the following code:

    Converter = FileConverter("/Users/nicolas/Downloads/test.xlsx", "/Users/nicolas/Downloads/test.csv")
    Converter.processCSV()
    """

    def __init__(self, excel_file, output_file):
        """
        Initializes the FileConverter class.

        Parameters:
        - excel_file: the path to the CSV file to be converted
        - output_file: the path to the CSV file to be created

        Returns:
        - None
        """
        self.excel_file = excel_file
        self.output_file = output_file

    def extract_coordinates_raw(self, row):
        """
        Extracts the coordinates from the 'WKT' column of the DataFrame.

        Parameters:
        - row: a row of the DataFrame

        Returns:
        - A Pandas Series containing the coordinates
        """
        line_string = row["WKT"]
        match = re.search(r"\(([^)]+)", line_string)
        coordinates_str = match.group(1)
        coordinates = [pair.split()[:2] for pair in coordinates_str.split(",")]
        return pd.Series(coordinates, index=["coordinates_a", "coordinates_b"])

    def processCSV(self):
        """
        Converts the CSV file to a Pandas DataFrame, cleans up the data, and exports the DataFrame to a CSV file.

        Parameters:
        - None

        Returns:
        - None
        """
        df = pd.read_excel(self.excel_file)

        # FILTER DATAFRAME
        df = df[df["altitudeMode"] != "clampToGround"]

        # SPLIT 'name' COLUMN INTO MULTIPLE COLUMNS and reorder columns
        df[
            [
                "timestamp",
                "altitude",
                "horizontal",
                "vertical",
                "distance",
            ]
        ] = df[
            "name"
        ].str.split(expand=True)
        df = df[
            [
                "timestamp",
                "altitude",
                "horizontal",
                "vertical",
                "distance",
                "WKT",
            ]
        ]

        # EXTRACT DATA FROM 'WKT' COLUMN
        df["WKT"] = df["WKT"].astype(str)
        coordinates_raw = df.apply(self.extract_coordinates_raw, axis=1)
        df = pd.concat([df, coordinates_raw], axis=1)
        df = df.drop("WKT", axis=1)
        df = df.drop("coordinates_b", axis=1)

        # REMOVE UNITS FROM altitude, horizontal, vertical, and distance COLUMNS
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

        # CONVERT HORIZONTAL SPEED TO METERS PER SECOND
        df["horizontal"] = (df["horizontal"] / 3.6).round(2)

        # EXTRACT COORDINATES FROM 'coordinates_a' COLUMN
        df["coordinates_a"] = df["coordinates_a"].astype(str)
        coordinates_a = df["coordinates_a"].str.split(" ", expand=True)
        df["longitude"] = coordinates_a[0]
        df["latitude"] = coordinates_a[1]
        df = df.drop("coordinates_a", axis=1)

        # CLEAN UP COORDINATES
        df["longitude"] = df["longitude"].str.replace(r"[\[\]',]", "", regex=True)
        df["latitude"] = df["latitude"].str.replace(r"[\[\]',]", "", regex=True)

        # EXPORT DATAFRAME TO CSV
        custom_headers = [
            "timestamp [UTC]",
            "relative altitude [m]",
            "horizontal velocity [m/s]",
            "vertical velocity [m/s]",
            "distance to takeoff [km]",
            "longitude",
            "latitude",
        ]
        df.to_csv(self.output_file, index=False, header=custom_headers)
        print(df)


# %%
