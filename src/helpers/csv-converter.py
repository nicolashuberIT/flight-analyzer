# %%

import pandas as pd
import re


class FileConverter:
    """
    Converts a CSV file to a Pandas DataFrame.

    To run this script, use Jupyter Notebook and copy the following code:

    Converter = FileConverter("path/to/input/file.xlsx", "path/to/output/file.csv")
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
        df[["timestamp", "altitude", "horizontal", "vertical", "distance"]] = df[
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
        df["WKT"] = df["WKT"].astype(str)  # Ensure 'WKT' is treated as a string
        coordinates_raw = df.apply(self.extract_coordinates_raw, axis=1)
        df = pd.concat([df, coordinates_raw], axis=1)
        df = df.drop("WKT", axis=1)
        df = df.drop("coordinates_b", axis=1)

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
        print(df)
        df.to_csv(self.output_file, index=False)


# %%
