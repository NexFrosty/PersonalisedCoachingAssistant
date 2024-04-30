import os
import csv
import datetime
import numpy as np
import pandas as pd
from typing import Union, List, Dict

from data_collection.collect_data import collect_data

from ._processor import *


def get_past_season(npast=1):
    curr = datetime.datetime.now()
    year = curr.year
    month = curr.month
    if month <= 6:
        year -= 1
    year -= npast
    season = f"{year}/{str(year + 1)[-2:]}"
    return season


def get_current_season():
    return get_past_season(npast=0)


def get_file_location(position, season="2022-23") -> str:
    """Get the location of the csv file base on the position and the season.

    :param position: Position of the player.
    :type position: Literal["defender"] | Literal["forward"] | Literal["midfielder"] | Literal["goalkeeper"]
    :param season: The season, defaults to "2022-23"
    :type season: str, optional
    :raise ValueError: If the position is invalid, raise this error.
    :return: String to the file location.
    :rtype: str
    """
    position = position.lower()
    valid = ["midfielder", "goalkeeper", "forward", "defender"]
    if position not in valid:
        vstr = ", ".join(valid)
        raise ValueError(f"Invalid position. Position must be either {vstr}")
    filepath = f"data/{season}/{position.lower()}_raw_data.csv"
    if os.path.exists(filepath):
        return filepath

    collect_data(season.replace("-", "/"), position=position)


# NOTE: This function is still experimental. There is no use at the moment.
def get_data(filename: str = None, position: str = None) -> pd.DataFrame:
    """Retrieve data either from using webscrapping or from local file. If filename is given, then the data will be retrieved from local file. If position is given, it will retrieve from webscrapping method.
    If both parameters are give, it will try to retrieve from local file first and if file does not exist, it will do webscrapping.

    :param filename: Local file to retrieve data from, defaults to None
    :type filename: str, optional
    :param position: A string position ['defender', 'midfielder', 'forward', 'goalkeeper'], defaults to None
    :type position: str, optional
    :raises TypeError: Raise error if no argument is provided.
    :raises FileNotFoundError: Raise error if file does not exist and position argument is None.
    :return: Pandas dataframe consist of the data.
    :rtype: pd.DataFrame
    """

    if filename is None and position is None:
        raise TypeError(f"get_data() require either filename or position.")

    mode = None
    if filename is not None:
        mode = "read_file"
        try:
            return pd.DataFrame(filename)
        except FileNotFoundError:
            mode = "retrieve" if position is not None else None

    if position is not None and mode == "retrieve":
        # TODO: Do webscrapping
        raise NotImplementedError(
            "get_data() function does not implement webscrapping yet."
        )

    if mode is None:
        raise FileNotFoundError(f"{filename} does not exist.")


def read_data_list(filename: str) -> List[Dict]:
    """Read data from filename.

    :param filename: Filename to read data from.
    :type filename: str
    :return: A list of dict containing the attributes and values
    :rtype: list[dict]
    """
    reader = csv.DictReader(open(filename, "r"))
    return list(reader)


class DataHandler:
    """Handles data processing from given filename. If filename is None, then the data must be loaded before trying getting the data, otherwise None will be given.

    To load data after the handler initialization, use `load_data_from_csv' method to load new data from csv file.

    :param filename: Filename to retrieve the data, defaults to None
    :type filename: str | None, optional
    """

    def __init__(self, processor: BaseDataProcessor, filename: Union[str, None] = None):
        self._df = None
        self._data_list = None
        self._processor = processor
        if filename is not None:
            self.load_data_from_csv(filename)

    def load_data_from_csv(self, filename: str):
        """Load data from CSV file.

        :param filename: Filename to read from.
        :type filename: str
        """
        self._data_list = read_data_list(filename)

    def get_data(self) -> List[Dict]:
        """Retrive processed data.

        :return: A list of dictionary consist of attribute name as keys and processed data as values.
        :rtype: list[dict]
        """
        data_list = [self._processor(data).data for data in self._data_list]
        return data_list

    def get_pd_data(self) -> pd.DataFrame:
        """Retieve processed data as pandas.DataFrame.

        :return: pandas dataframe object containing processed data.
        :rtype: pd.DataFrame
        """
        data_list = self.get_data()
        return pd.DataFrame(data_list)

    def get_attributes(self) -> Union[List[str], None]:
        """Get the attributes after the data been processed.

        :return: List of attributes
        :rtype: list[str]
        """
        data = self.get_data()
        return list(data[0].keys())

    def get_normalized_data(self) -> pd.DataFrame:
        """Return the normalized DataFrame

        :return: A pd.DataFrame with normalize value 0 - 100
        :rtype: pd.DataFrame
        """
        data = self.get_pd_data()
        for attr in data.columns:
            data[attr] = (
                (data[attr] - data[attr].min())
                / (data[attr].max() - data[attr].min())
                * 100
            )
        return data
