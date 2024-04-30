import os
import sys
import pandas as pd
from rich.console import Console

from . import scrapper

console = Console()
print = console.print

# ROOT_DIR = os.path.dirname(sys.argv[0])
# DATA_DIR = os.path.join(ROOT_DIR, "data")
DATA_DIR = "data"


def process_collection(position_name, season, save_to):
    position_name = position_name.lower()
    data = scrapper.collect_data(position=position_name, season=season)
    in_data = []
    for _name, _value in data.items():
        d = {"name": _name} | _value
        in_data.append(d)
    df = pd.DataFrame(in_data)
    print(df.head())
    filename = os.path.join(save_to, f"{position_name}_raw_data.csv")
    df.to_csv(filename, index=False)


def collect_data(season: str, save_to: str = None, position: str = None):
    if save_to is None:
        _data_dir = os.path.join(DATA_DIR, season.replace("/", "-"))
    else:
        _data_dir = save_to
    if not os.path.exists(_data_dir):
        os.makedirs(_data_dir)

    if position is None:
        to_collect = ["defender", "midfielder", "goalkeeper", "forward"]
    else:
        to_collect = [position]
    for position_name in to_collect:
        print(f"Processing data collection for {position_name}...")
        process_collection(position_name, season, _data_dir)
    print("All process complete!", style="bold green")


if __name__ == "__main__":
    collect_data("2022/23")
