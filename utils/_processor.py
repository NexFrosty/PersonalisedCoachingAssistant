import math
from abc import ABC, abstractmethod
from typing import List


class BaseDataProcessor(ABC):
    def __init__(self, data: dict):
        self.data = {}
        self.raw_data = {}
        for k, v in data.items():
            if k == "name":
                self.raw_data[k] = v
                continue
            self.raw_data[k] = self._convert_value(v)
        self.raw_data["Appearance"] = self._get_appearnace()
        self._process_data()

    @abstractmethod
    def _process_data(self):
        """Base method to process the raw data."""
        ...

    def _cal_pct(
        self,
        value_name: str,
        total_name: str,
        decimal_places: int = 2,
    ) -> float:
        """Calculate the percentage of 2 values from the raw_data.

        :param value_name: Name for the value from the raw_data.
        :type value_name: str
        :param total_name: Name for the total value from the raw_data.
        :type total_name: str
        :param decimal_places: Determine the decimal places of the result, defaults to 2
        :type decimal_places: int, optional
        :return: A float representing the percentage of the calculation.
        :rtype: float
        """
        pct = self.raw_data[value_name] / self.raw_data[total_name] * 100
        return round(pct, decimal_places)

    def _remove_alphabet(self, value: str) -> str:
        """Remove letters from the value.

        :param value: A string value to filter.
        :type value: str
        :return: A new string containing only numbers and '.'.
        :rtype: str
        """
        value = str(value)
        return "".join(filter(lambda x: x.isdecimal() or x == ".", value))

    def _add_data(self, name: str, value: float = None):
        """Register data. If value is none, then the value will be retrived from the raw_data. This method will automatically filter out alphabet and only consider digits and '.'.

        :param name: Data name to register.
        :type name: str
        :param value: Value to register, defaults to None
        :type value: float, optional
        """
        if value is None:
            value = self.raw_data[name]
        self.data[name] = value

    def _register_data(self, value_name: str, total_name: str):
        """Register a new data into self.data. The data will be retrieved from raw_data.

        :param value_name: Name of the value from raw_data
        :type value_name: str
        :param total_name: Name of the total value from raw_data
        :type total_name: str
        """
        pct = self._cal_pct(value_name, total_name)
        self.data[value_name] = pct

    def _register_data_from_list(self, value_names: List[str], total_name: str):
        """Register a list of values into data retrieved from raw_data.

        :param value_names: A list of names of the value from raw_data.
        :type value_names: list[str]
        :param total_name: Name of the total value from raw_data.
        :type total_name: str
        """
        for name in value_names:
            self._register_data(name, total_name)

    def _get_appearnace(self) -> int:
        """Get the number of the appearnace. This calculation requires 2 data exist inside raw_data which are 'Passes per match' and 'Passes'.

        :return: The number of appearances.
        :rtype: int
        """
        return math.ceil(self.raw_data["Passes"] / self.raw_data["Passes per match"])

    def _cal_cumulative_pct(
        self, target: str, value: str, decimal_places: int = 2
    ) -> float:
        """Calculates the cumulative percentage from raw_data values.
        pct = target / (target + value) * 100

        :param target: The name of the data from the raw_data as pct
        :type target: str
        :param value: Name of the 2nd value from the raw_data.
        :type value: str
        :param decimal_places: Number of decimal places.
        :type decimal_places: int
        :return: target / (target + value) * 100
        :rtype: float
        """
        _won = self.raw_data[target]
        _total = _won + self.raw_data[value]
        _pct = _won / _total * 100
        return round(_pct, decimal_places)

    def _convert_value(self, value: any) -> float:
        """Convert any value to a float if it is valid.

        :param value: A value to convert into a float.
        :type value: Any
        :return: A float after removing illegal characters.
        :rtype: float
        """
        value = float(self._remove_alphabet(value))
        return value

    def _per_match(self, value):
        """Register data based on per match basis.

        :param value: The value name in raw_data
        :type value: str
        :return: a float representing the value per match.
        :rtype: float
        """
        return self.raw_data[value] / self.raw_data["Appearance"]


class GoalkeeperDataProcessor(BaseDataProcessor):
    def __init__(self, data):
        super().__init__(data)

    def _process_data(self):
        to_process = ["Penalties Saved", "Punches", "Catches", "Sweeper clearances"]
        self._register_data_from_list(to_process, "Saves")
        for attr in ["Goal Kicks", "Clean sheets", "Passes per match"]:
            self._add_data(attr)


class DefenderDataProcessor(BaseDataProcessor):
    def __init__(self, data):
        super().__init__(data)

    def _process_data(self):
        self._add_data("Tackle success %")
        self._register_data("Headed Clearance", "Clearances")
        self._register_data("Clearances", "Appearance")
        _name = "Duels"
        self._add_data(_name, self._cal_cumulative_pct(_name + " won", _name + " lost"))
        _name = "Aerial battles"
        self._add_data(_name, self._cal_cumulative_pct(_name + " won", _name + " lost"))
        self._add_data("Cross accuracy %")
        self._add_data("Passes per match")
        self._add_data("Interceptions")


class MidfielderDataProcessor(BaseDataProcessor):
    def __init__(self, data):
        super().__init__(data)

    def _process_data(self):
        to_process = ["Headed goals"]
        self._register_data_from_list(to_process, "Goals")
        self._add_data("Shooting accuracy %")
        self._add_data("Cross accuracy %")
        self._add_data("Tackle success %")
        _name = "Duels"
        self._add_data(_name, self._cal_cumulative_pct(_name + " won", _name + " lost"))
        _name = "Aerial battles"
        self._add_data(_name, self._cal_cumulative_pct(_name + " won", _name + " lost"))
        self._add_data("Passes per match")
        self._add_data("Big Chances Created")


class ForwardDataProcessor(BaseDataProcessor):
    def __init__(self, data):
        super().__init__(data)

    def _process_data(self):
        self._register_data("Headed goals", "Goals")
        self._add_data("Goals")
        self._add_data("Shots on target")
        self._add_data("Shooting accuracy %")
        self._add_data("Passes per match")
        self._add_data("Big Chances Created")
        self._add_data("Big chances missed")
        self._add_data("Freekicks scored")
        self._add_data("Assists")
        self._add_data("Cross accuracy %", self._per_match("Crosses"))


PROCESSOR = {
    "defender": DefenderDataProcessor,
    "forward": ForwardDataProcessor,
    "midfielder": MidfielderDataProcessor,
    "goalkeeper": GoalkeeperDataProcessor,
}
