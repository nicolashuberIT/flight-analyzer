import pytest
import sys
import os
import pandas as pd
from typing import List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.helpers.FileConverter import FileConverter


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
        "tests/assets/FileConverter/test.xlsx",
        "tests/assets/FileConverter/test_output.csv",
    )


def test_init(converter) -> None:
    """
    Tests the __init__ method.

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    assert (
        converter.excel_file == "tests/assets/FileConverter/test.xlsx",
        "The excel_file attribute is not correct.",
    )
    assert (
        converter.output_file == "tests/assets/FileConverter/test_output.csv",
        "The output_file attribute is not correct.",
    )


def test_read_excel_file(converter) -> None:
    """
    Tests the read_excel_file method.

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    assert isinstance(
        converter.read_excel_file(), pd.DataFrame
    ), "The returned object is not a Pandas DataFrame."


def test_filter_dataframe(converter) -> None:
    """
    Tests the filter_dataframe method. Are columns with 'altitudeMode' equal to 'clampToGround' removed?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_excel_file()
    df = converter.filter_dataframe(df)
    assert df[
        df["altitudeMode"] == "clampToGround"
    ].empty, "The DataFrame is not filtered correctly."


def test_split_and_reorder_columns(converter) -> None:
    """
    Tests the split_and_reorder_columns method. Are the columns split and reordered correctly?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_excel_file()
    df = converter.filter_dataframe(df)
    df = converter.split_and_reorder_columns(df)
    assert df.columns.tolist() == [
        "timestamp",
        "altitude",
        "horizontal",
        "vertical",
        "distance",
        "WKT",
    ], "The columns are not split and reordered correctly."


def test_remove_static_speeds(converter) -> None:
    """
    Tests the remove_static_speeds method. Are static  horizontal speeds removed?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_excel_file()
    df = converter.filter_dataframe(df)
    df = converter.split_and_reorder_columns(df)
    df = converter.remove_static_speeds(df)
    assert df[
        df["horizontal"] == "0"
    ].empty, "The static horizontal speeds are not removed."


def test_extract_coordinates(converter) -> None:
    """
    Tests the extract_coordinates method. Are the coordinates extracted correctly?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_excel_file()
    df = converter.filter_dataframe(df)
    df = converter.split_and_reorder_columns(df)
    df = converter.remove_static_speeds(df)
    df = converter.extract_coordinates(df)
    assert "coordinates_a" in df.columns, "The coordinates are not extracted correctly."


def test_extract_coordinates_a(converter) -> None:
    """
    Tests the extract_coordinates_a method. Are the coordinates extracted correctly?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_excel_file()
    df = converter.filter_dataframe(df)
    df = converter.split_and_reorder_columns(df)
    df = converter.remove_static_speeds(df)
    df = converter.extract_coordinates(df)
    df = converter.extract_coordinates_a(df)
    assert (
        "longitude" in df.columns
    ), "The coordinates are not extracted correctly to the longitude row."
    assert (
        "latitude" in df.columns
    ), "The coordinates are not extracted correctly to the latitude row."


def test_clean_up_coordinates(converter) -> None:
    """
    Tests the clean_up_coordinates method. Are the coordinates cleaned up correctly?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_excel_file()
    df = converter.filter_dataframe(df)
    df = converter.split_and_reorder_columns(df)
    df = converter.remove_static_speeds(df)
    df = converter.extract_coordinates(df)
    df = converter.extract_coordinates_a(df)
    df = converter.clean_up_coordinates(df)
    assert (
        df["longitude"].iloc[0] == 9.303066
    ), "The longitude is not cleaned up correctly."
    assert (
        df["latitude"].iloc[0] == 47.2074
    ), "The latitude is not cleaned up correctly."


def test_remove_units(converter) -> None:
    """
    Tests the remove_units method. Are the units removed correctly?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_excel_file()
    df = converter.filter_dataframe(df)
    df = converter.split_and_reorder_columns(df)
    df = converter.remove_static_speeds(df)
    df = converter.extract_coordinates(df)
    df = converter.extract_coordinates_a(df)
    df = converter.clean_up_coordinates(df)
    df = converter.remove_units(df)
    assert isinstance(df["altitude"].iloc[0], float), "The altitude is not a float."
    assert isinstance(
        df["horizontal"].iloc[0], float
    ), "The horizontal speed is not a float."
    assert isinstance(
        df["vertical"].iloc[0], float
    ), "The vertical speed is not a float."
    assert isinstance(df["distance"].iloc[0], float), "The distance is not a float."


def test_convert_horizontal_speed(converter: FileConverter) -> None:
    df = converter.read_excel_file()
    df = converter.filter_dataframe(df)
    df = converter.split_and_reorder_columns(df)
    df = converter.remove_static_speeds(df)
    df = converter.extract_coordinates(df)
    df = converter.extract_coordinates_a(df)
    df = converter.clean_up_coordinates(df)
    df = converter.remove_units(df)
    test_speed = df["horizontal"].iloc[2]
    df = converter.convert_horizontal_speed(df)
    assert (
        test_speed / 3.6 == df["horizontal"].iloc[2]
    ), "The horizontal speed is not converted correctly."


def test_export_to_csv(converter: FileConverter) -> None:
    """
    Tests the export_to_csv method. Is the DataFrame exported to a CSV file correctly?

    Parameters:
    - converter: the FileConverter object to be tested

    Returns:
    - None
    """
    df = converter.read_excel_file()
    df = converter.filter_dataframe(df)
    df = converter.split_and_reorder_columns(df)
    df = converter.remove_static_speeds(df)
    df = converter.extract_coordinates(df)
    df = converter.extract_coordinates_a(df)
    df = converter.clean_up_coordinates(df)
    df = converter.remove_units(df)
    df = converter.convert_horizontal_speed(df)
    custom_headers: List[str] = [
        "timestamp [UTC]",
        "relative altitude [m]",
        "horizontal velocity [m/s]",
        "vertical velocity [m/s]",
        "distance to takeoff [km]",
        "longitude",
        "latitude",
    ]
    converter.export_to_csv(df, custom_headers)
    assert os.path.exists(
        "tests/assets/FileConverter/test_output.csv"
    ), "The CSV file is not exported correctly."
