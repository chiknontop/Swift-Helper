"""
A Helper File with Various Functions.
"""

import json
from pathlib import Path


def resolve_path() -> str:
    """
    Gets the Current Directory Path.

    Returns
    --------
    :class:`str`
        The Current Directory Path.
    """
    return str(Path(__file__).parents[1])


def read_json(file_path: str) -> dict:
    """
    Reads a JSON File and Returns the Data.

    Parameters
    ----------
    file_path: :class:`str`
        The Location of the File.
    
    Raises
    ------
    :class:`FileNotFoundError`
        File Path must be Invalid.

    Returns
    --------
    :class:`dict`
        The JSON.
    """
    with open(file_path, "r") as File:
        data = json.load(File)
    return data


def write_json(file_path: str, data: dict) -> None:
    """
    Writes Data to a JSON File.

    Parameters
    ----------
    file_path: :class:`str`
        The Location of the File.
    
    data: :class:`dict`
        The Data to Write to the File.
    """

    with open(file_path, "w") as File:
        json.dump(data, File, indent=4)

