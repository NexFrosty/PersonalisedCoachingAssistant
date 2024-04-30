import os
import csv
from typing import Union, List, Tuple, Dict
from dataclasses import dataclass, field, asdict


@dataclass
class TrainingInfo:
    name: str
    description: str = field(repr=False)
    position: str
    attributes: List[str]

    def __post_init__(self):
        self.description = self.description.replace("|n|", "\n")
        self.position = self.position.lower()

        if type(self.attributes) == str:
            _to_remove = "[]\"'"
            for c in _to_remove:
                self.attributes = self.attributes.replace(c, "")
            self.attributes = self.attributes.split(",")
            self.attributes = list(map(str.strip, self.attributes))

    def get(self) -> Dict[str, str]:
        """Get the dictionary version of the data.

        :return: A dictioanry containing the information of the training.
        :rtype: dict[str, str]
        """
        d = self.description.replace("\\n", "|n|").replace("\n", "|n|")
        return {
            "name": self.name,
            "description": d,
            "position": self.position,
            "attributes": self.attributes,
        }


class TrainingHandler:
    """This class handles the training information."""

    def __init__(self, filename: str = None):
        """Initialize the TrainingHandler.

        :param filename: A csv file, defaults to None
        :type filename: str, optional
        """
        self.training_list: List[TrainingInfo] = []
        if filename is not None:
            self.load(filename)

    def load(self, filename: str):
        """Load the training information from a csv file.

        :param filename: The name of the csv file to load.
        :type filename: str
        """
        self.filename = filename
        if not os.path.exists(os.path.dirname(self.filename)):
            os.makedirs(os.path.dirname(self.filename))

        if not os.path.exists(self.filename):
            with open(self.filename, "w"):
                pass
        with open(self.filename, "r") as file:
            reader = csv.DictReader(file)
            self._load_data(list(reader))

    def save(self):
        """Save the data into the loaded csv file.

        :raises Exception: If no file is loaded, raises an exception.
        """
        if self.filename is None:
            raise Exception(
                "Could not save because TrainingHandler does not load any file yet."
            )
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, self.training_list[0].get().keys())
            writer.writeheader()
            writer.writerows([training.get() for training in self.training_list])
        print(
            f"[TrainingHandler]   Successfully save all {len(self.training_list)} training info"
        )

    def add_training_info(self, new_training: TrainingInfo, save=False):
        """Add training information into the training list handler.

        :param new_training: A TrainingInfo object.
        :type new_training: TrainingInfo
        :param save: If true, this method will automatically call the save method, defaults to False
        :type save: bool, optional
        """
        self.training_list.append(new_training)
        if save:
            self.save()

    def retrieve(
        self,
        attributes: Union[str, List[str], Tuple[str]],
        position: str = None,
    ) -> Union[List[TrainingInfo], None]:
        """Retrieve the training information base on the given attributes.

        :param attributes: A single attribute string or  a list of attributes to retrieve the training information.
        :type attributes: str | list[str] | tuple[str]
        :param position: Optional filter to retrieve the training information, defaults to None
        :type position: str, optional
        :raises TypeError: If argument attributes is not a list or tuple.
        :return: A list of TrainingInfo objects based on the attributes/position filters. Return None if no training info found.
        :rtype: list[TrainingInfo] | None
        """
        if type(attributes) == str:
            attributes = [attributes]

        if type(attributes) not in [list, tuple]:
            raise TypeError("attributes must be list or tuple")

        if not self.training_list:
            return

        filtered_info = []
        # NOTE: The done set can be remove and replace with positions filter
        done = set()
        attributes = list(map(str.lower, attributes))
        for attrs in attributes:
            for info in self.training_list:
                if position is not None and position.lower() != info.position.lower():
                    continue
                info_attribute = list(map(str.lower, info.attributes))
                if attrs in info_attribute:
                    if info.name in done:
                        continue
                    done.add(info.name)
                    filtered_info.append(info)

        return filtered_info

    def _load_data(self, data: List[Dict]):
        """Load the data into the training list from the reader as a list of TrainingInfo objects.

        :param data: List of dictionary that contains info to be load as TrainingInfo objects.
        :type data: list
        """
        self.training_list = [TrainingInfo(**training) for training in data]
        print("[TrainingHandler]   Data Loaded")


Trainer = TrainingHandler
