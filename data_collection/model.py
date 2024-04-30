from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

goalkeeper_data = [
    "Saves",
    "Penalties Saved",
    "Punches",
    "Catches",
    "Sweeper clearances",
    "Goal Kicks",
    "Clean sheets",
    "Passes",
    "Passes per match",
]

defender_data = [
    "Tackle success %",
    "Clearances",
    "Headed Clearance",
    "Duels won",
    "Duels lost",
    "Aerial battles won",
    "Aerial battles lost",
    "Cross accuracy %",
    "Passes",
    "Passes per match",
]

midfielder_data = [
    "Goals",
    "Headed goals",
    "Goals with right foot",
    "Goals with left foot",
    "Shooting accuracy %",
    "Cross accuracy %",
    "Tackle success %",
    "Duels won",
    "Duels lost",
    "Aerial battles won",
    "Aerial battles lost",
    "Passes",
    "Passes per match",
]

forward_data = [
    "Goals",
    "Headed goals",
    "Goals with right foot",
    "Goals with left foot",
    "Shooting accuracy %",
    "Passes",
    "Passes per match",
]

data_model = {
    "defender": defender_data,
    "forward": forward_data,
    "midfielder": midfielder_data,
    "goalkeeper": goalkeeper_data,
}


class DataExtractor:
    def __init__(self, dom_table: WebElement):
        self.__stats = dom_table.find_elements(By.CLASS_NAME, "normalStat")

    def get_stats(self, filter_fn: list[str] | None = None):
        if filter_fn is not None:
            filter_fn = [f.lower() for f in filter_fn]

        data = {}
        for stat in self.__stats:
            stat_data = stat.find_element(By.CLASS_NAME, "stat").text
            stat_name, stat_value = stat_data.split("\n")
            if filter_fn is not None and stat_name.lower() not in filter_fn:
                continue
            stat_value = stat.find_element(By.CLASS_NAME, "allStatContainer").text
            data[stat_name] = stat_value

        return data
