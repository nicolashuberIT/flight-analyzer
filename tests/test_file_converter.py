import os
import sys
import pytest
import pandas as pd
from typing import List

# AI content (ChatGPT, 02/21/2024), verified and adapted by Nicolas Huber.
current_directory = os.path.dirname(__file__)
flight_analyzer_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.insert(0, flight_analyzer_directory)

from src.helpers.file_convertor import FileConverter


@pytest.fixture()
def converter() -> FileConverter:
    """
    Returns a FileConverter object.

    Parameters:
    - None

    Returns:
    - A FileConverter object
    """
    return FileConverter(
        input_file=f"{flight_analyzer_directory}/tests/assets/file_converter/test_file_convertor.xlsx",
        output_file=f"{flight_analyzer_directory}/tests/assets/file_converter/test_file_convertor_output.csv",
    )


def test_init(converter: FileConverter) -> None:
    """
    Tests the __init__ method.

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    assert (
        converter.input_file == "tests/assets/FileConverter/test.xlsx",
        "The excel_file attribute is not correct.",
    )
    assert (
        converter.output_file == "tests/assets/FileConverter/test_output.csv",
        "The output_file attribute is not correct.",
    )


# AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
def test_read_excel_file(converter: FileConverter) -> None:
    """
    Tests the read_excel_file method.

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    assert isinstance(
        converter.read_input_file(), pd.DataFrame
    ), "The returned object is not a Pandas DataFrame."


def test_filter_dataframe(converter: FileConverter) -> None:
    """
    Tests the filter_dataframe method. Are columns with 'altitudeMode' equal to 'clampToGround' removed?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_input_file()
    df = converter.filter_dataframe(df=df)
    assert df[
        df["altitudeMode"] == "absolute"
    ].empty, "The DataFrame is not filtered correctly."


# AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
def test_split_and_reorder_columns(converter: FileConverter) -> None:
    """
    Tests the split_and_reorder_columns method. Are the columns split and reordered correctly?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_input_file()
    df = converter.filter_dataframe(df=df)
    df = converter.split_and_reorder_columns(df=df)
    assert df.columns.tolist() == [
        "timestamp",
        "altitude",
        "horizontal",
        "vertical",
        "distance",
        "WKT",
    ], "The columns are not split and reordered correctly."


# AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
def test_extract_coordinates(converter: FileConverter) -> None:
    """
    Tests the extract_coordinates method. Are the coordinates extracted correctly?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_input_file()
    df = converter.filter_dataframe(df=df)
    df = converter.split_and_reorder_columns(df=df)
    df = converter.remove_static_speeds(df=df)
    df = converter.extract_coordinates(df=df)
    assert "coordinates_a" in df.columns, "The coordinates are not extracted correctly."


# AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
def test_extract_coordinates_a(converter: FileConverter) -> None:
    """
    Tests the extract_coordinates_a method. Are the coordinates extracted correctly?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_input_file()
    df = converter.filter_dataframe(df=df)
    df = converter.split_and_reorder_columns(df=df)
    df = converter.remove_static_speeds(df=df)
    df = converter.extract_coordinates(df=df)
    df = converter.extract_coordinates_a(df=df)
    assert (
        "longitude" in df.columns
    ), "The coordinates are not extracted correctly to the longitude row."
    assert (
        "latitude" in df.columns
    ), "The coordinates are not extracted correctly to the latitude row."


# AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
def test_clean_up_coordinates(converter: FileConverter) -> None:
    """
    Tests the clean_up_coordinates method. Are the coordinates cleaned up correctly?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_input_file()
    df = converter.filter_dataframe(df=df)
    df = converter.split_and_reorder_columns(df=df)
    df = converter.remove_static_speeds(df=df)
    df = converter.extract_coordinates(df=df)
    df = converter.extract_coordinates_a(df=df)
    df = converter.clean_up_coordinates(df=df)
    assert (
        df["longitude"].iloc[0] == 9.30435
    ), "The longitude is not cleaned up correctly."
    assert (
        df["latitude"].iloc[0] == 47.154116
    ), "The latitude is not cleaned up correctly."


# AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
def test_remove_units(converter: FileConverter) -> None:
    """
    Tests the remove_units method. Are the units removed correctly?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_input_file()
    df = converter.filter_dataframe(df=df)
    df = converter.split_and_reorder_columns(df=df)
    df = converter.remove_static_speeds(df=df)
    df = converter.extract_coordinates(df=df)
    df = converter.extract_coordinates_a(df=df)
    df = converter.clean_up_coordinates(df=df)
    df = converter.remove_units(df=df)
    assert isinstance(df["altitude"].iloc[0], float), "The altitude is not a float."
    assert isinstance(
        df["horizontal"].iloc[0], float
    ), "The horizontal speed is not a float."
    assert isinstance(
        df["vertical"].iloc[0], float
    ), "The vertical speed is not a float."
    assert isinstance(df["distance"].iloc[0], float), "The distance is not a float."


# AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
def test_remove_static_speeds(converter: FileConverter) -> None:
    """
    Tests the remove_static_speeds method. Are static  horizontal speeds removed?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_input_file()
    df = converter.filter_dataframe(df=df)
    df = converter.split_and_reorder_columns(df=df)
    df = converter.remove_static_speeds(df=df)
    assert df[
        df["horizontal"] == 0
    ].empty, "The static horizontal speeds are not removed."


# AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
def test_convert_horizontal_speed(converter: FileConverter) -> None:
    df = converter.read_input_file()
    df = converter.filter_dataframe(df=df)
    df = converter.split_and_reorder_columns(df=df)
    df = converter.remove_static_speeds(df=df)
    df = converter.extract_coordinates(df=df)
    df = converter.extract_coordinates_a(df=df)
    df = converter.clean_up_coordinates(df=df)
    df = converter.remove_units(df=df)
    test_speed = df["horizontal"].iloc[2]
    df = converter.convert_horizontal_speed(df)
    assert (
        test_speed / 3.6 == df["horizontal"].iloc[2]
    ), "The horizontal speed is not converted correctly."


# AI content (GitHub Copilot, 01/25/2024), verified and adapted by Nicolas Huber.
def test_export_to_csv(converter: FileConverter) -> None:
    """
    Tests the export_to_csv method. Is the DataFrame exported to a CSV file correctly?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_input_file()
    df = converter.filter_dataframe(df=df)
    df = converter.split_and_reorder_columns(df=df)
    df = converter.remove_static_speeds(df=df)
    df = converter.extract_coordinates(df=df)
    df = converter.extract_coordinates_a(df=df)
    df = converter.clean_up_coordinates(df=df)
    df = converter.remove_units(df=df)
    df = converter.convert_horizontal_speed(df=df)
    custom_headers: List[str] = [
        "timestamp [UTC]",
        "relative altitude [m]",
        "horizontal velocity [m/s]",
        "vertical velocity [m/s]",
        "distance to takeoff [km]",
        "longitude",
        "latitude",
    ]
    converter.export_to_csv(df=df, custom_headers=custom_headers)
    assert os.path.exists(
        converter.output_file
    ), "The CSV file is not exported correctly."
    os.remove(converter.output_file)
