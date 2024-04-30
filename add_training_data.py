"""A simple cli tools to collect training data"""

from typing import List, Dict
from engine import trainer


DEFLOC = "data/training/"


def main():
    training_handler = trainer.TrainingHandler()
    filename = get_filename()

    training_handler.load(filename)
    while True:
        training_data = get_training_info_data()
        register_new_training(training_handler, training_data)

        cont = input("Continue [Y|n]: ") or "Y"
        if cont.lower() == "n":
            break

    training_handler.save()


def get_filename() -> str:
    filename = input("Enter training filename: ")
    if not filename.startswith(DEFLOC):
        filename = DEFLOC + filename
    if not filename.endswith(".csv"):
        filename = filename + ".csv"
    return filename


def get_training_info_data() -> Dict:
    keys = trainer.TrainingInfo.__annotations__.keys()
    r = {}
    for key in keys:
        if key == "attributes":
            r[key] = get_list_of_attribtues()
        else:
            r[key] = input(f"{key.capitalize()}: ")
    return r


def get_list_of_attribtues() -> List[str]:
    attr = input("Attributes [seperated by comma (,)]: ")
    return attr.split(",")


def register_new_training(handler: trainer.TrainingHandler, training_info: Dict):
    new_info = trainer.TrainingInfo(**training_info)
    handler.add_training_info(new_info)


def print_welcome_message():
    msg = """Welcome, please make sure you enter correct filename so that this program able to properly save the training file data.

The program will repeatly ask for the training data until you decide to not continue. Therefore, this might be crude but good way to register the training data so that we can use it in the ES program afterwards.
For filename, you don't need to specify the exact location since it will be automatically saved in the 'data/training/' directory.
If there is a newline need to be added for example in the description, use '\\n'.
"""
    print(msg)


if __name__ == "__main__":
    print_welcome_message()
    main()
