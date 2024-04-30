import tkinter as tk
import customtkinter as ctk
from typing import List, Dict

from . import buttons
from .page import Page
from .widgets import Meter, SilderMeter, CardButton
from engine import trainer
from utils import datahandler
from utils import font as ufont
from utils import image as uimage

_SEASON = "data_new"


class WelcomePage(Page):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, "assets/welcome_page.png", *args, **kwargs)

        ctk.CTkButton(
            self,
            text="ENTER",
            corner_radius=0,
            fg_color="yellow",
            text_color="black",
            command=lambda: self._callback("onclick_enter"),
        ).place(relx=0.5, rely=0.8, anchor="center", relheight=0.05, relwidth=0.1)

    def _callback(self, event):
        if event == "onclick_enter":
            self.parent.change_page(PositionSelectPage)


class PositionSelectPage(Page):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._add_bg()
        self._init_widget()

    def _add_bg(self):
        image = uimage.text_bg_builder("Select Position", self.parent.size)
        self.add_background(image)

    def _init_widget(self):
        f = ufont.RenderFont("assets/fonts/Anton-Regular.ttf")
        txt_img = f.get_render(
            "CHOOSE YOUR POSITION", font_size=100, fill=(255, 255, 0)
        )
        size = txt_img.size
        ctk.CTkLabel(
            self,
            text="",
            image=ctk.CTkImage(txt_img, size=size),
            fg_color=self.fg_color1,
        ).pack(pady=10, expand=True)

        positions = ["goalkeeper", "forward", "midfielder", "defender"]

        button_frame = ctk.CTkFrame(self, fg_color=self.fg_color1)
        button_frame.pack(expand=True)

        button_size = (293, 488)
        self.button_images = {
            pos: self._load_button_image(pos, button_size) for pos in positions
        }
        buttons = {
            pos: ctk.CTkButton(
                button_frame,
                text="",
                image=self.button_images[pos],
                command=lambda arg=pos: self._callback(arg),
            )
            for pos in positions
        }
        for button in buttons.values():
            button.pack(side="left", padx=15)

    def _load_button_image(self, posname, size=None) -> ctk.CTkImage:
        """
        Load and image from filename into ctk.CTkImage

        :param filename: A string to image filename
        :type filename: str
        :param size: A tuple of (width, height). If None, the it will use the original image size. Default None.
        :type size: tuple[int, int]
        :return: ctk.CTkImage object
        :rtype: ctk.CTkImage
        """
        _image = uimage.load_image(f"assets/{posname}_img_button.png", size=size)
        return ctk.CTkImage(dark_image=_image, size=_image.size)

    def _callback(self, event: str):
        """Callback handler for the button.

        :param event: Button id. This is related to the available positions name.
        :type event: str
        """
        self.parent.change_page(DataInputPage, position=event)


class DataInputPage(Page):
    def __init__(self, parent, position=None, **kwargs):
        super().__init__(parent, **kwargs)
        if type(position) is not str:
            raise ValueError("Position must be a str")

        self._data = {}
        self._position = position.lower()
        self._processor = datahandler.PROCESSOR[self._position]
        self._data_handler = datahandler.DataHandler(
            self._processor,
            datahandler.get_file_location(self._position, season=_SEASON),
        )
        self._add_bg()
        self._init_widget()

    def _add_bg(self):
        image = uimage.text_bg_builder(self._position, self.parent.size)
        self.add_background(image)

    def _init_widget(self):
        _container = ctk.CTkFrame(self, fg_color=self.fg_color1)
        _position_label = ctk.CTkLabel(_container, text="")
        _inputs_frame = ctk.CTkFrame(_container, fg_color=self.fg_color2)
        _proceed_button = buttons.create_proceed_button(
            self, lambda: self._callback("proceed")
        )
        _back_button = buttons.create_back_button(self, lambda: self._callback("back"))

        _item_per_column = 6
        for i, attr in enumerate(self._load_data_model()):
            _frame = self._create_input_field(_inputs_frame, attr)
            _frame.grid(column=i // _item_per_column, row=i % _item_per_column, padx=10)

        _font = ufont.RenderFont("assets/fonts/Anton-Regular.ttf")
        _text = f"Fill in data for\n{self._position.upper()}"
        _text = _font.get_render(_text, 100, (255, 255, 0), align="center").rotate(
            -90, expand=True
        )
        _text = ctk.CTkImage(_text, size=_text.size)
        _position_label.configure(image=_text)

        _container.place(relx=0.5, rely=0.5, anchor="c")
        _inputs_frame.pack(side="left", expand=True, anchor="e")
        _position_label.pack(side="left", anchor="w", padx=25)
        _proceed_button.place(relx=0.95, rely=0.95, anchor="e")
        _back_button.place(relx=0.05, rely=0.05, anchor="nw")

    def _load_data_model(self) -> List[str]:
        """
        Get a list of data model

        :return: A list of attributes name for each position
        :rtype: list
        """
        return self._data_handler.get_attributes()

    def _create_input_field(self, parent, name: str) -> ctk.CTkFrame:
        """Create a new input field consist of label, slider and meter.

        :param parent: Where the field will be attached to
        :type parent: tk.Widget
        :param name: The field label
        :type name: str
        :return: A frame containing all input elements
        :rtype: ctk.CTkFrame
        """
        _frame = ctk.CTkFrame(parent, fg_color="transparent")
        _label = ctk.CTkLabel(
            _frame,
            text=name.capitalize(),
            justify="left",
            anchor="w",
            font=("arial", 30),
            fg_color="transparent",
        )
        _slider = ctk.CTkSlider(
            _frame,
            from_=0,
            to=100,
            height=30,
            width=400,
            progress_color="#ffff00",
            button_color="#ffff00",
            command=lambda val, id_=name: self._slider_event(val, id_),
            number_of_steps=100,
        )

        _var = tk.IntVar(value=_slider.get())
        _meter = Meter(
            _frame,
            variable=_var,
            suffix="%",
            text_color="white",
            fg_color="#FFFF00",
        )

        _label.grid(row=0, column=0, columnspan=2, sticky="w")
        _slider.grid(row=1, column=0)
        _meter.grid(row=1, column=1)

        self._data[name] = _var
        return _frame

    def _slider_event(self, val, id_):
        """Slider event handler to update the data coresspond to the slider id_

        :param val: Slider value
        :type val: int | float
        :param id_: Slider ownder
        :type id_: str
        """
        self._data[id_].set(str(int(val)))

    def _callback(self, event):
        """Callback when the proceed button is clicked."""
        if event == "proceed":
            _data = self._get_data_dict()
            self.parent.change_page(ResultPage, data=_data)
        elif event == "back":
            self.parent.change_page(PositionSelectPage)

    def _get_data_dict(self) -> Dict[str, int]:
        """Collect all the data into a dictionary.

        :return: A collection of data
        :rtype: dict[str, int]
        """
        data = self._data.copy()
        data = {k: v.get() for k, v in data.items()}
        return {"position": self._position, "data": data}


class ResultPage(Page):
    def __init__(self, parent, data: Dict, **kwargs):
        super().__init__(parent, **kwargs)
        self._data = data
        self._position = self._data["position"]
        self._processor = datahandler.PROCESSOR[self._position]
        self._data_handler = datahandler.DataHandler(
            self._processor,
            datahandler.get_file_location(self._position, season=_SEASON),
        )

        self._load_threshold()
        self._add_bg()
        self._init_widgets()

    def _add_bg(self):
        image = uimage.text_bg_builder("RESULT", self.parent.size)
        self.add_background(image)

    def _init_widgets(self):
        """Initialize the widgets."""
        _container = ctk.CTkFrame(self, fg_color=self.fg_color1)
        _result_frame = ctk.CTkFrame(_container, fg_color=self.fg_color2)
        _label = self._create_title_widget(_container)

        _proceed_button = buttons.create_proceed_button(
            self, lambda: self._callback("proceed")
        )
        _back_button = buttons.create_back_button(self, lambda: self._callback("back"))

        for i, attr_name in enumerate(self._data["data"].keys()):
            _attr_frame = self._create_attribute_widget(_result_frame, attr_name)
            _attr_frame.grid(row=i % 6, column=i // 6, padx=10)

        _container.place(relx=0.5, rely=0.5, anchor="c")
        _result_frame.pack(side="left", anchor="e")
        _label.pack(side="left", anchor="w", expand=True)
        _proceed_button.place(relx=0.95, rely=0.95, anchor="e")
        _back_button.place(relx=0.05, rely=0.05, anchor="nw")

    def _create_title_widget(self, parent) -> ctk.CTkLabel:
        """Create CTkLabel widget to display page title

        :return: Title label
        :rtype: ctk.CTkLabel
        """
        _font = ufont.RenderFont("assets/fonts/Anton-Regular.ttf")
        _text = _font.get_render("RESULT", 112, (255, 255, 0), align="center")
        _text = _text.rotate(-90, expand=True)
        _text_image = ctk.CTkImage(_text, size=_text.size)
        _label = ctk.CTkLabel(parent, text="", image=_text_image)
        return _label

    def _access_attributes(self) -> Dict[str, bool]:
        """Compare the attributes of player and average top 10 scores.

        :returns: A dictionary of attributes difference between player attrubutes and average top 10 league attributes.
        :rtype: dict[str, int]
        """
        result = {}
        player_attrs = self._data["data"]
        sample_attrs = self._sample_average
        for pk, pv in player_attrs.items():
            result[pk] = int(player_attrs[pk]) - int(sample_attrs[pk])
        return result

    def _create_attribute_widget(self, parent, name: str) -> ctk.CTkFrame:
        """Create frame containing attribute widget.

        :param parent: Place to attach the widget
        :type parent: ctk.CTkFrame
        :param name: Name of the attribute
        :type name: str
        :return: A frame containing attribute widget
        :rtype: ctk.CTkFrame
        """
        _low_color = "#eb1515"
        _high_color = "#1afa12"
        _score = self._access_attributes()[name]
        _meter_color = _low_color if _score < 0 else _high_color
        _frame = ctk.CTkFrame(parent, fg_color="transparent")
        _label = ctk.CTkLabel(
            _frame,
            text=name.capitalize(),
            justify="left",
            anchor="w",
            font=("arial", 30),
            fg_color="transparent",
        )
        _slider = SilderMeter(
            _frame,
            from_=0,
            to=100,
            thickness=20,
            width=400,
            radius=90,
            value=self._data["data"][name],
            fill_color="#FFFF00",
            under_threshold_color=_low_color,
            over_threshold_color=_high_color,
            threshold=self._sample_average[name] if _score != 0 else None,
        )
        _meter = Meter(
            _frame,
            value=abs(_score),
            suffix="%",
            prefix="-" if _score < 0 else "",
            text_color="white",
            fg_color=_meter_color,
        )

        _label.grid(row=0, column=0, columnspan=2, sticky="w")
        _slider.grid(row=1, column=0, padx=10)
        _meter.grid(row=1, column=1)

        return _frame

    def _load_threshold(self):
        """Load the threshold data"""
        sample_data = self._data_handler.get_normalized_data()
        self._sample_average = sample_data.mean().astype(int)

    def _callback(self, event: str):
        """Callback function that fires when the button is clicked or any widget trigered an event.

        :param event: A string representing the event name or id.
        :type event: str
        :raises NotImplementedError: 'proceed' event is not implemented yet.
        """
        if event == "proceed":
            attributes = self._get_attributes_to_train()
            self.parent.change_page(
                TrainingRecommendationPage,
                attributes=attributes,
                position=self._position,
            )
        elif event == "back":
            self.parent.change_page(DataInputPage, position=self._data["position"])

    def _get_attributes_to_train(self) -> List[str]:
        """Get the list of attributes that requires training.

        :return: A list of attributes name.
        :rtype: list[str]
        """
        attrs = dict(
            filter(lambda pair: pair[1] < 0, self._access_attributes().items())
        )
        attrs = dict(sorted(attrs.items(), key=lambda pair: pair[1]))
        return list(attrs.keys())


class TrainingRecommendationPage(Page):
    def __init__(self, parent, attributes: List[str], position: str = None, **kwargs):
        super().__init__(parent, **kwargs)
        self._attributes = attributes
        # NOTE: This position is used to filter the training info. Use none to use all regardless of position.
        self._position = position
        self._training_handler = trainer.Trainer("data/training/training_01.csv")
        self._add_bg()
        self._init_widget()

    def _add_bg(self):
        image = uimage.text_bg_builder("TRAININGS", self.parent.size)
        self.add_background(image)

    def _init_widget(self):
        """Initialize the widget."""
        self._init_nav_buttons()
        self._set_page_title()
        self._set_recommendation_card()

    def _init_nav_buttons(self):
        upper_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        back_button = buttons.create_back_button(
            upper_button_frame, lambda: self._callback("back")
        )
        home_button = buttons.create_button(
            upper_button_frame, "HOME", lambda: self._callback("home")
        )
        back_button.pack(side="left")
        home_button.pack(side="left")
        upper_button_frame.place(relx=0.05, rely=0.05, anchor="nw")

    def _set_page_title(self):
        """Draw the page title."""
        font = ufont.RenderFont("assets/fonts/Anton-Regular.ttf")
        text = font.get_render(
            text="RECOMMENDED TRAININGS", font_size=100, fill="yellow", align="center"
        )
        text = ctk.CTkImage(text, size=text.size)
        label = ctk.CTkLabel(self, text="", image=text, fg_color=self.fg_color1)
        label.pack(pady=25)

    def _set_recommendation_card(self):
        """Setup the recommendation cards widget"""
        training_info = self._training_handler.retrieve(
            self._attributes, self._position
        )
        textfont = ("assets/fonts/PublicSans-Bold.ttf", 32)
        subtextfont = ("assets/fonts/HankenGrotesk-Medium.ttf", 22)
        pad = (15, 25)
        card_size = (400, 500)
        n_card = len(training_info)
        parent_size = self.parent.size

        total_width = n_card * card_size[0] + (n_card + 1) * pad[0]
        if total_width < parent_size[0] - 10:
            container = ctk.CTkFrame(self, fg_color=self.fg_color1)
        else:
            container = ctk.CTkScrollableFrame(
                self,
                orientation="horizontal",
                width=parent_size[0],
                height=card_size[1] + pad[1],
                fg_color=self.fg_color1,
            )
        if n_card == 0:
            _label = ctk.CTkLabel(
                container,
                text="There is no training recomended.",
                font=("arial", 65),
            )
            _label.pack()

        # TODO: Implement correct button commands
        for i, training in enumerate(training_info):
            card = CardButton(
                container,
                text=training.name,
                subtext=training.description,
                text_font=textfont,
                subtext_font=subtextfont,
                size=card_size,
                command=lambda s=i: print(
                    s, training_info[s].name, training_info[s].attributes
                ),
            )
            card.pack(side="left", padx=pad[0])

        container.pack(expand=True)

    def _callback(self, event: str):
        if event == "back":
            self.parent.change_page(DataInputPage, position=self._position)
        elif event == "home":
            self.parent.change_page(PositionSelectPage)
