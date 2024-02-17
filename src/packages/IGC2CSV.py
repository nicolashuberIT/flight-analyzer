# %%

"""
IGC2CSV.py:

- This python package is available at https://github.com/nicolashuberIT/IGC2CSV.

TESTING NOTICE:

- The original IGC2CSV code was not accompanied by any tests.
- This modified version of the code is tested using the pytest framework. The tests are available in the /tests directory of the repository (https://github.com/nicolashuberIT/IGC2CSV). 
- The tests are written to ensure that the code works as expected and that the modifications do not introduce any regressions.

COPYRIGHT NOTICE: 

- The original IGC2CSV code was created by OverloadUT and there's no explicit license information available in the original repository.
- This code is a modified version of the IGC2CSV code, which has been forked from the original repository at https://github.com/OverloadUT/IGC2CSV.
- This modified version of the code is part of the research project "Fliegen am Limit - Aktive Sicherheit im Gleitschirmsport" conducted by Nicolas Huber, the author of these modifications.
- The modifications include encapsulating the code in a class, adding type hints, and removing the main function to make the code more reusable and testable. Additionally the code has been formatted according to PEP 8 using Black and some additional functionality has been added.
- The modified code is encorporated into the research project in the form of a Python package in the flight-analyzer application, which is part of the research project and is available at https://github.com/nicolashuberIT/flight-analyzer.

©  2017, OverloadUT & 2024, Nicolas Huber.
"""

import os
import datetime
import pandas as pd
from math import radians, sin, cos, asin, sqrt
from typing import List, Dict, Any, Tuple


class IGC2CSV:
    """
    A class to parse IGC files (and generate csv files).
    """

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def __init__(self) -> None:
        """
        Initializes the IGC2CSV class.

        Parameters:
        - None

        Returns:
        - None
        """
        self.recordtypes: Dict[str, Any] = {
            "A": self.logline_A,
            "B": self.logline_B,
            "C": self.logline_NotImplemented,
            "D": self.logline_NotImplemented,
            "E": self.logline_NotImplemented,
            "F": self.logline_NotImplemented,
            "G": self.logline_NotImplemented,
            "H": self.logline_H,
            "I": self.logline_I,
            "J": self.logline_NotImplemented,
            "K": self.logline_NotImplemented,
            "L": self.logline_NotImplemented,
        }

        self.headertypes: Dict[str, Any] = {"FDTE": self.logline_H_FDTE}

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def parse_igc(self, flight: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses the IGC file and returns a flight dictionary.

        Parameters:
        - flight: The flight dictionary to be updated with parsed data.

        Returns:
        - flight: The updated flight dictionary.
        """
        flight["fixrecords"] = []
        flight["optional_records"] = {}

        file = open(flight["igcfile"], "r")

        for line in file:
            line = line.rstrip()
            linetype = line[0]
            self.recordtypes[linetype](line, flight)

        file.close()

        return flight

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def crunch_flight(self, flight: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds calculated fields to the flight dictionary.

        Parameters:
        - flight: The flight dictionary to be updated with calculated data.

        Returns:
        - flight: The updated flight dictionary.
        """
        for index, record in enumerate(flight["fixrecords"]):
            # thisdatetime = datetime.datetime.strptime(record['timestamp'], '')
            record["latdegrees"] = self.lat_to_degrees(record["latitude"])
            record["londegrees"] = self.lon_to_degrees(record["longitude"])

            record["time"] = datetime.time(
                int(record["timestamp"][0:2]),
                int(record["timestamp"][2:4]),
                int(record["timestamp"][4:6]),
                0,
            )

            if index > 0:
                prevrecord = flight["fixrecords"][index - 1]

                if record["time"] < prevrecord["time"]:
                    record["date"] = prevrecord["date"] + datetime.timedelta(days=1)
                else:
                    record["date"] = prevrecord["date"]

                record["datetime"] = datetime.datetime.combine(
                    record["date"], record["time"]
                )
                record["time_delta"] = (
                    record["datetime"] - prevrecord["datetime"]
                ).total_seconds()
                record["running_time"] = (
                    record["datetime"] - flight["datetime_start"]
                ).total_seconds()
                record["distance_delta"] = self.haversine(
                    record["londegrees"],
                    record["latdegrees"],
                    prevrecord["londegrees"],
                    prevrecord["latdegrees"],
                )
                flight["distance_total"] += record["distance_delta"]
                record["distance_total"] = flight["distance_total"]
                record["distance_from_start"] = self.straight_line_distance(
                    record["londegrees"],
                    record["latdegrees"],
                    record["alt-GPS"],
                    flight["fixrecords"][0]["londegrees"],
                    flight["fixrecords"][0]["latdegrees"],
                    flight["fixrecords"][0]["alt-GPS"],
                )
                record["groundspeed"] = (
                    record["distance_delta"] / record["time_delta"] * 3600
                )
                flight["groundspeed_peak"] = max(
                    record["groundspeed"], flight["groundspeed_peak"]
                )
                record["groundspeed_peak"] = flight["groundspeed_peak"]
                record["alt_gps_delta"] = record["alt-GPS"] - prevrecord["alt-GPS"]
                record["alt_pressure_delta"] = (
                    record["pressure"] - prevrecord["pressure"]
                )
                record["climb_speed"] = record["alt_gps_delta"] / record["time_delta"]
                flight["climb_total"] += max(0, record["alt_gps_delta"])
                record["climb_total"] = flight["climb_total"]
                flight["alt_peak"] = max(record["alt-GPS"], flight["alt_peak"])
                flight["alt_floor"] = min(record["alt-GPS"], flight["alt_floor"])
                if "TAS" in flight["optional_records"]:
                    flight["tas_peak"] = max(record["opt_tas"], flight["tas_peak"])
                    record["tas_peak"] = flight["tas_peak"]
            else:
                flight["time_start"] = record["time"]
                flight["datetime_start"] = datetime.datetime.combine(
                    flight["flightdate"], flight["time_start"]
                )
                flight["altitude_start"] = record["alt-GPS"]
                flight["distance_total"] = 0
                flight["climb_total"] = 0
                flight["alt_peak"] = record["alt-GPS"]
                flight["alt_floor"] = record["alt-GPS"]
                flight["groundspeed_peak"] = 0

                record["date"] = flight["flightdate"]
                record["datetime"] = datetime.datetime.combine(
                    record["date"], record["time"]
                )
                record["running_time"] = 0
                record["time_delta"] = 0
                record["distance_delta"] = 0
                record["distance_total"] = 0
                record["groundspeed"] = 0
                record["groundspeed_peak"] = 0
                record["alt_gps_delta"] = 0
                record["alt_pressure_delta"] = 0
                record["climb_speed"] = 0
                record["climb_total"] = 0
                record["distance_from_start"] = 0

                if "TAS" in flight["optional_records"]:
                    flight["tas_peak"] = record["opt_tas"]
                    record["tas_peak"] = 0

        return flight

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def logline_A(self, line: str, flight: Dict[str, Any]) -> None:
        """
        Processes type A records from the IGC file.

        Parameters:
        - line: The line from the IGC file containing type A record.
        - flight: The flight dictionary to be updated with parsed data.

        Returns:
        - None
        """
        flight["manufacturer"] = line[1:]
        return

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def logline_H(self, line: str, flight: Dict[str, Any]) -> None:
        """
        Processes type H records from the IGC file.

        Parameters:
        - line: The line from the IGC file containing type H record.
        - flight: The flight dictionary to be updated with parsed data.

        Returns:
        - None
        """
        try:
            self.headertypes[line[1:5]](line[5:], flight)
        except KeyError:
            print("Header (not implemented): {}".format(line[1:]))
        return

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def logline_H_FDTE(self, line: str, flight: Dict[str, Any]) -> None:
        """
        Processes flight date header records from the IGC file.

        Parameters:
        - line: The line from the IGC file containing flight date header record.
        - flight: The flight dictionary to be updated with parsed data.

        Returns:
        - None
        """
        flight["flightdate"] = datetime.date(
            int(line[4:6]) + 2000, int(line[2:4]), int(line[0:2])
        )
        print("Flight date: {}".format(flight["flightdate"]))

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def logline_I(self, line: str, flight: Dict[str, Any]) -> None:
        """
        Processes type I records from the IGC file.

        Parameters:
        - line: The line from the IGC file containing type I record.
        - flight: The flight dictionary to be updated with parsed data.

        Returns:
        - None
        """
        num = int(line[1:3])
        for i in range(num):
            field = line[3 + 7 * i : 10 + 7 * i]
            flight["optional_records"][field[4:7]] = (
                int(field[0:2]) - 1,
                int(field[2:4]),
            )

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def logline_B(self, line: str, flight: Dict[str, Any]) -> None:
        """
        Processes type B records from the IGC file.

        Parameters:
        - line: The line from the IGC file containing type B record.
        - flight: The flight dictionary to be updated with parsed data.

        Returns:
        - None
        """
        flight["fixrecords"].append(
            {
                "timestamp": line[1:7],
                "latitude": line[7:15],
                "longitude": line[15:24],
                "AVflag": line[24:25] == "A",
                "pressure": int(line[25:30]),
                "alt-GPS": int(line[30:35]),
            }
        )
        for key, record in flight["optional_records"].items():
            flight["fixrecords"][-1]["opt_" + key.lower()] = line[record[0] : record[1]]

        return

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def logline_NotImplemented(self, line: str, flight: Dict[str, Any]) -> None:
        """
        Handles unimplemented record types.

        Parameters:
        - line: The line from the IGC file containing unimplemented record type.
        - flight: The flight dictionary.

        Returns:
        - None
        """
        print("Record Type {} not implemented: {}".format(line[0:1], line[1:]))
        return

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def lat_to_degrees(self, lat: str) -> float:
        """
        Converts latitude from IGC format to degrees.

        Parameters:
        - lat: Latitude in IGC format.

        Returns:
        - Latitude in degrees.
        """
        direction = {"N": 1, "S": -1}
        degrees = int(lat[0:2])
        minutes = int(lat[2:7])
        minutes /= 1000.0
        directionmod = direction[lat[7]]
        return (degrees + minutes / 60.0) * directionmod

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def lon_to_degrees(self, lon: str) -> float:
        """
        Converts longitude from IGC format to degrees.

        Parameters:
        - lon: Longitude in IGC format.

        Returns:
        - Longitude in degrees.
        """
        direction = {"E": 1, "W": -1}
        degrees = int(lon[0:3])
        minutes = int(lon[3:8])
        minutes /= 1000.0
        directionmod = direction[lon[8]]
        return (degrees + minutes / 60.0) * directionmod

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def haversine(self, lon1: float, lat1: float, lon2: float, lat2: float) -> float:
        """
        Calculates the distance between two points using the haversine formula.

        Parameters:
        - lon1: Longitude of point 1.
        - lat1: Latitude of point 1.
        - lon2: Longitude of point 2.
        - lat2: Latitude of point 2.

        Returns:
        - Distance between the two points.
        """
        lon1, lat1, lon2, lat2 = list(map(radians, [lon1, lat1, lon2, lat2]))
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def straight_line_distance(
        self,
        lon1: float,
        lat1: float,
        alt1: float,
        lon2: float,
        lat2: float,
        alt2: float,
    ) -> float:
        """
        Calculates the straight-line distance between two points.

        Parameters:
        - lon1: Longitude of point 1.
        - lat1: Latitude of point 1.
        - alt1: Altitude of point 1.
        - lon2: Longitude of point 2.
        - lat2: Latitude of point 2.
        - alt2: Altitude of point 2.

        Returns:
        - Straight-line distance between the two points.
        """
        a = self.haversine(lon1, lat1, lon2, lat2)
        b = (alt1 - alt2) / 1000.0
        c = sqrt(a**2.0 + b**2.0)
        return c

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def get_output_filename(self, inputfilename: str) -> str:
        """
        Generates an output filename based on the input filename.

        Parameters:
        - inputfilename: Input filename.

        Returns:
        - Output filename.
        """
        head, tail = os.path.split(inputfilename)
        filename, ext = os.path.splitext(tail)
        outputfilename = filename + ".csv"
        return outputfilename

    # AI content (ChatGPT, 02/17/2024), verified and adapted by Nicolas Huber.
    def process_files(self, fileparam: str, export_to_csv: bool) -> None:
        """
        Processes IGC files and generates CSV output or returns a list of dictionaries representing the records.

        Parameters:
        - fileparam: The IGC file or directory to process.
        - export_to_csv: Whether to export to CSV.

        Returns:
        - DataFrame: A pandas DataFrame containing the records
        """
        logbook: List[Dict[str, Any]] = []

        if os.path.isfile(fileparam):
            logbook.append({"igcfile": os.path.abspath(fileparam)})
            print("Single IGC file supplied: {}".format(logbook[-1]["igcfile"]))
        elif os.path.isdir(fileparam):
            for filename in os.listdir(fileparam):
                fileabs = os.path.join(fileparam, filename)
                if not os.path.isfile(fileabs):
                    continue

                root, ext = os.path.splitext(fileabs)
                if ext.lower() == ".igc".lower():
                    logbook.append({"igcfile": os.path.abspath(fileabs)})
        else:
            print("Must indicate a file or directory to process")
            return

        print("{} flights ready to process...".format(len(logbook)))

        for flight in logbook:
            flight = self.parse_igc(flight)

        for flight in logbook:
            flight = self.crunch_flight(flight)

        for flight in logbook:
            flight["outputfilename"] = self.get_output_filename(flight["igcfile"])

            output = open(flight["outputfilename"], "w")
            defaultoutputfields: List[Tuple[str, str, str]] = [
                ("Datetime (UTC)", "record", "datetime"),
                ("Elapsed Time", "record", "running_time"),
                ("Latitude (Degrees)", "record", "latdegrees"),
                ("Longitude (Degrees)", "record", "londegrees"),
                ("Altitude GPS", "record", "alt-GPS"),
                ("Distance Delta", "record", "distance_delta"),
                ("Distance Total", "record", "distance_total"),
                ("Groundspeed", "record", "groundspeed"),
                ("Groundspeed Peak", "record", "groundspeed_peak"),
                ("Altitude Delta (GPS)", "record", "alt_gps_delta"),
                ("Altitude Delta (Pressure)", "record", "alt_pressure_delta"),
                ("Climb Speed", "record", "climb_speed"),
                ("Climb Total", "record", "climb_total"),
                ("Max Altitude (flight)", "flight", "alt_peak"),
                ("Min Altitude (flight)", "flight", "alt_floor"),
                (
                    "Distance From Start (straight line)",
                    "record",
                    "distance_from_start",
                ),
            ]
            outputfields = list(defaultoutputfields)
            if "TAS" in flight["optional_records"]:
                outputfields.append(("True Airspeed", "record", "opt_tas"))
                outputfields.append(("True Airspeed Peak", "record", "tas_peak"))

            records_data = []
            for record in flight["fixrecords"]:
                record_data = {}
                for field in outputfields:
                    if field[1] == "record":
                        record_data[field[0]] = record[field[2]]
                    elif field[1] == "flight":
                        record_data[field[0]] = flight[field[2]]
                records_data.append(record_data)

            if export_to_csv:
                output = open(flight["outputfilename"], "w")
                header = ""
                for field in outputfields:
                    header += field[0] + ","
                output.write(header[:-1] + "\n")

                for record in flight["fixrecords"]:
                    recordline = ""
                    for field in outputfields:
                        if field[1] == "record":
                            recordline += str(record[field[2]]) + ","
                        elif field[1] == "flight":
                            recordline += str(flight[field[2]]) + ","
                    output.write(recordline[:-1] + "\n")
            else:
                os.remove(flight["outputfilename"])

            return pd.DataFrame(records_data)

    def remove_first_row(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Removes the first row from the DataFrame.

        Parameters:
        - data: The DataFrame to be modified.

        Returns:
        - DataFrame: The modified DataFrame.
        """
        return data.iloc[1:]

    def convert_dataframe(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Converts the DataFrame to the format required by the flight-analyzer application.

        Parameters:
        - data: The DataFrame to be converted.

        Returns:
        - DataFrame: The converted DataFrame.
        """
        data_selected = data[
            [
                "Datetime (UTC)",
                "Altitude GPS",
                "Groundspeed",
                "Climb Speed",
                "Distance From Start (straight line)",
                "Longitude (Degrees)",
                "Latitude (Degrees)",
            ]
        ]

        data_selected_renamed = data_selected.rename(
            columns={
                "Datetime (UTC)": "timestamp [UTC]",
                "Altitude GPS": "relative altitude [m]",
                "Groundspeed": "horizontal velocity [m/s]",
                "Climb Speed": "vertical velocity [m/s]",
                "Distance From Start (straight line)": "distance to takeoff [km]",
                "Longitude (Degrees)": "longitude",
                "Latitude (Degrees)": "latitude",
            }
        )

        return data_selected_renamed

    def convert_horizontal_speed(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Converts the groundspeed from km/h to m/s after the DataFrame has been converted to flight-analyzer format.

        Parameters:
        - data: The DataFrame to be modified.

        Returns:
        - DataFrame: The modified DataFrame.
        """
        data["horizontal velocity [m/s]"] = data["horizontal velocity [m/s]"] / 3.6
        return data

    def remove_static_speeds(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Removes static speeds from the DataFrame.

        Parameters:
        - data: The DataFrame to be modified.

        Returns:
        - DataFrame: The modified DataFrame.
        """
        data = data[data["horizontal velocity [m/s]"] > 0]
        return data

    def export_to_flight_analyzer_format(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Converts the DataFrame to the format required by the flight-analyzer application.

        Parameters:
        - data: The DataFrame to be converted.

        Returns:
        - DataFrame: The converted DataFrame.
        """
        data = self.remove_first_row(data)
        data = self.convert_dataframe(data)
        data = self.convert_horizontal_speed(data)
        data = self.remove_static_speeds(data)
        return data

    def export_to_csv(self, data: pd.DataFrame, filename: str) -> None:
        """
        Exports the DataFrame to a CSV file.

        Parameters:
        - data: The DataFrame to be exported.
        - filename: The filename of the CSV file.

        Returns:
        - None
        """
        data.to_csv(filename, index=False)
        return


# %%
