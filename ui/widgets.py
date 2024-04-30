import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk, ImageFont, ImageColor

from utils import font as ufont


class Meter(ctk.CTkFrame):
    """A circular meter

    :param parent: Where the widget attached to
    :type parent: tk.Widget
    :param variable: A variable that store the meter value, defaults to None
    :type variable: tk.IntVar, optional
    :param meter_size: The size of the meter. Since the meter is within square boundary, only 1 int needed, defaults to 100
    :type meter_size: int, optional
    :param meter_thickness: The thickness of meter progress indicator, defaults to 10
    :type meter_thickness: int, optional
    :param troughcolor: The color of empty progress, defaults to "#494747"
    :type troughcolor: str, optional
    :param wedge_size: The size of meter's wedge, defaults to 0
    :type wedge_size: int, optional
    :param fg_color: The color of meter filled progress, defaults to "#ff1e00"
    :type fg_color: str, optional
    :param value: Set new meter's value of variable not given, defaults to 0
    :type value: int, optional
    :param max_value: The upper limit of the meter's value, defaults to 100
    :type max_value: int, optional
    :param prefix: Additional str to be display on the left of meter's value label, defaults to ""
    :type prefix: str, optional
    :param suffix: Additional str to be display on the right of meter's value label, defaults to ""
    :type suffix: str, optional
    :param showtext: If True, show text label, else hide it, defaults to True
    :type showtext: bool, optional
    :param textfont: A tuple of (font_family, font_size), defaults to ("arial", 25)
    :type textfont: tuple, optional
    :param text_color: The color of text label, defaults to "black"
    :type text_color: str, optional
    :raises TypeError: If variable is not a tk.IntVar or None object, raise TypeError
    """

    M = 3

    def __init__(
        self,
        parent,
        variable=None,
        meter_size=100,
        meter_thickness=10,
        troughcolor="#494747",
        wedge_size=0,
        fg_color="#ff1e00",
        value=0,
        max_value=100,
        prefix="",
        suffix="",
        showtext=True,
        textfont=("arial", 25),
        text_color="black",
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        self.configure(fg_color="transparent")

        if variable is None:
            variable = tk.IntVar(value=value)

        if type(variable) is not tk.IntVar:
            raise TypeError("variable must be None or a tk.IntVar")

        self.current_value = variable
        self.current_value.trace_add("write", self._draw_meter)
        self.max_value = max_value

        self._base_image = None
        self._metersize = meter_size
        self._meterthickness = meter_thickness
        self._metertrough = troughcolor
        self._meterforeground = fg_color
        self._wedgesize = wedge_size
        self._arcoffset = -90
        self._arcrange = 360
        self._meterimage = None

        self._prefixtext = prefix
        self._suffixtext = suffix
        self._showtext = showtext
        self._textfont = textfont
        self._fontcolor = text_color

        self._setup_widget()

    def _draw_meter(self, *_):
        """Draw a complete meter"""
        img = self._base_image.copy()
        draw = ImageDraw.Draw(img, mode="RGBA")
        self._draw_solid_meter(draw)
        if self._showtext:
            self._draw_meter_label(draw)
        self._meterimage = ctk.CTkImage(img, size=(self._metersize, self._metersize))
        self.indicator.configure(image=self._meterimage)

    def _draw_meter_base(self):
        """Draw meter base image"""
        self._base_image = Image.new(
            mode="RGBA",
            size=(self._metersize * self.M, self._metersize * self.M),
            color=(0, 0, 0, 0),
        )
        draw = ImageDraw.Draw(self._base_image, mode="RGBA")

        x1 = y1 = self._metersize * self.M - 20
        width = self._meterthickness * self.M

        draw.arc(
            xy=(0, 0, x1, y1),
            start=self._arcoffset,
            end=self._arcrange + self._arcoffset,
            fill=self._metertrough,
            width=width,
        )

    def _draw_solid_meter(self, draw: ImageDraw.Draw):
        """Draw the meter progress bar

        :param draw: Meter draw object
        :type draw: ImageDraw.Draw
        """
        x1 = y1 = self._metersize * self.M - 20
        width = self._meterthickness * self.M

        if self._wedgesize > 0:
            value = self._get_meter_value()
            draw.arc(
                xy=(0, 0, x1, y1),
                start=value - self._wedgesize,
                end=value + self._wedgesize,
                fill=self._meterforeground,
                width=width,
            )
        else:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=self._arcoffset,
                end=self._get_meter_value(),
                fill=self._meterforeground,
                width=width,
            )

    def _draw_meter_label(self, draw: ImageDraw.Draw):
        """Draw the label on meter image. This label is the text in the middle of the meter image

        :param draw: Meter drawer object
        :type draw: ImageDraw.Draw
        """
        x1 = y1 = self._metersize * self.M - 20
        font_size = self._textfont[1] * self.M - 3
        text = str(self.current_value.get())

        if self._prefixtext:
            text = str(self._prefixtext) + text
        if self._suffixtext:
            text = text + str(self._suffixtext)

        font = ImageFont.truetype(self._textfont[0], font_size)
        draw.text(
            (x1 // 2, y1 // 2), text, self._fontcolor, font, anchor="mm", stroke_width=2
        )

    def _get_meter_value(self) -> int:
        """Return the meter value to be used to draw the arc of the meter progress."

        :return: The arc of the meter progress
        :rtype: int
        """
        value = (
            int(self.current_value.get() / self.max_value * self._arcrange)
            + self._arcoffset
        )
        return value

    def _setup_widget(self):
        """Setup the widget"""
        self.meterframe = ctk.CTkFrame(
            self, width=self._metersize, height=self._metersize, fg_color="transparent"
        )
        self.indicator = ctk.CTkLabel(self.meterframe, text="", fg_color="transparent")

        self._draw_meter_base()
        self._draw_meter()

        self.indicator.place(x=0, y=0)
        self.meterframe.pack()


class SilderMeter(ctk.CTkFrame):
    """A SliderMeter object. The same as Slider widget from ttk but has threshold value.

    :param parent: Parent where this widget will be attached to, defaults to None
    :type parent: ctk.CTkWidget, optional
    :param value: The value of the slider, defaults to 0
    :type value: int, optional
    :param from_: The minimum value expected, defaults to 0
    :type from_: int, optional
    :param to: The maximum value, defaults to 100
    :type to: int, optional
    :param threshold: The threshold value, defaults to None
    :type threshold: float, optional
    :param thickness: The thickness of the slider, defaults to 30
    :type thickness: int, optional
    :param fill_color: The color of the filled slider, defaults to "#1212ff"
    :type fill_color: str, optional
    :param trough_color: The color of empty slider, defaults to "#a9a9a9"
    :type trough_color: str, optional
    :param under_threshold_color: The color that appear if valeu under the threshold, defaults to "#e81313"
    :type under_threshold_color: str, optional
    :param over_threshold_color: The color that indicate the value above threshold, defaults to "#4cec1b"
    :type over_threshold_color: str, optional
    :param radius: The radius of the slider corner, defaults to 0
    :type radius: int, optional
    """

    M = 3

    def __init__(
        self,
        parent=None,
        value=0,
        from_=0,
        to=100,
        threshold=None,
        thickness=30,
        fill_color="#1212ff",
        trough_color="#a9a9a9",
        under_threshold_color="#e81313",
        over_threshold_color="#4cec1b",
        radius=0,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        self.value = value
        self._from = from_
        self._to = to
        self._threshold = threshold
        self._thickness = thickness
        self._fill_color = fill_color
        self._trough_color = trough_color
        self._radius = radius
        self._under_threshold_color = under_threshold_color
        self._over_threshold_color = over_threshold_color

        _h = self._thickness + 30
        self.configure(height=_h)
        self.configure(fg_color="transparent")

        self._base_image = None
        self._slider_image = None

        self._setup_widget()

    def _draw_slider(self, *_):
        img = self._base_image.copy()
        draw = ImageDraw.Draw(img, mode="RGBA")

        if self._threshold is not None and self.value < self._threshold:
            self._draw_slider_threshold(draw)
        self._draw_slider_progress(draw)
        self._draw_circle(draw)
        if self._threshold is not None:
            self._draw_threshold_divider(draw)
            if self.value >= self._threshold:
                self._draw_slider_threshold(draw)

        w = self.cget("width")
        h = self.cget("height")
        self._slider_image = ctk.CTkImage(img, size=(w, h))
        self.slider.configure(image=self._slider_image)

    def _draw_slider_base(self):
        w = self.cget("width") * self.M
        h = self.cget("height") * self.M
        thickness = self._thickness * self.M

        self._base_image = Image.new(mode="RGBA", size=(w, h))
        draw = ImageDraw.Draw(self._base_image, mode="RGBA")

        start = (h - thickness) // 2
        draw.rounded_rectangle(
            (0, start, w, start + thickness),
            fill=self._trough_color,
            radius=self._radius,
        )

    def _draw_slider_progress(self, draw: ImageDraw.Draw):
        h = self.cget("height") * self.M
        x1 = self._cal_fill(self.value) * self.M
        thickness = self._thickness * self.M
        y0 = (h - thickness) // 2
        draw.rounded_rectangle(
            xy=(0, y0, x1, y0 + thickness),
            radius=self._radius,
            fill=self._fill_color,
        )

    def _draw_slider_threshold(self, draw: ImageDraw.Draw):
        """Draw the threshold indicator.

        :param draw: Drawer object that will draw the threshold indicator.
        :type draw: ImageDraw.Draw
        """
        color = self._under_threshold_color
        if self.value >= self._threshold:
            color = self._over_threshold_color
        h = self.cget("height") * self.M
        thickness = self._thickness * self.M
        x1 = self._cal_fill(self._threshold) * self.M
        y0 = (h - thickness) // 2
        draw.rounded_rectangle((0, y0, x1, y0 + thickness), self._radius, fill=color)

    def _draw_threshold_divider(self, draw: ImageDraw.Draw):
        """Draw threshold divider. The square thinging shows where the threshold is.

        :param draw: Drawer object that will draw the threshold divider.
        :type draw: ImageDraw.Draw
        """
        indicator_thickness = 10 * self.M
        x = self._cal_fill(self._threshold) * self.M

        if self._threshold < indicator_thickness // 2:
            x0 = 0
        else:
            x0 = x - indicator_thickness // 2

        x1 = x + indicator_thickness // 2

        if self.value < self._threshold:
            color = self._under_threshold_color
        else:
            color = self._over_threshold_color

        y_offset = 7
        draw.rectangle(
            (x0, y_offset, x1, self.cget("height") * self.M - y_offset), fill=color
        )

    def _draw_circle(self, draw: ImageDraw.Draw):
        """Draw the slider cirlce.

        :param draw: Draw object
        :type draw: ImageDraw.Draw
        """
        x = self._cal_fill(self.value) * self.M
        y_offset = 25
        y1 = self.cget("height") * self.M - y_offset
        radius = (y1 - y_offset) // 2
        x0 = x - radius
        x1 = x + radius
        draw.ellipse((x0, y_offset, x1, y1), fill=self._fill_color)

    def _setup_widget(self):
        """Setup the widget"""
        self.slider = ctk.CTkLabel(self, text="", fg_color="transparent")
        self._draw_slider_base()
        self._draw_slider()
        self.slider.pack()

    def _cal_fill(self, value):
        """Calculate the fill area of the slider

        :param value: The slider value / current value
        :type value: float
        :return: The normalized value of the fill area
        :rtype: float
        """
        _range = abs(self._from - value)
        _total = abs(self._from - self._to)
        return (_range / _total) * self.cget("width")


class CardButton(ctk.CTkFrame):
    M = 3

    def __init__(
        self,
        parent,
        text,
        size=(250, 350),
        subtext="",
        image_name=None,
        text_color="black",
        text_font=("arial", 18),
        subtext_font=("arial", 16),
        subtext_color="#181818",
        textbox_color="yellow",
        textbox_size_pct=0.6,
        command=None,
        disabled=False,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        self.configure(fg_color="transparent")

        self.text = text
        self.subtext = subtext
        self.disabled = disabled

        self._size = size
        self._image_name = image_name
        self._text_color = text_color
        self._textfont = text_font
        self._subtext_color = subtext_color
        self._subtextfont = subtext_font
        self._textbox_color = textbox_color
        if command is not None and not hasattr(command, "__call__"):
            raise TypeError("command must be a function.")
        self._command = command
        if self._image_name is None:
            textbox_size_pct = 1.0
        self._textbox_size_pct = textbox_size_pct
        self.base_image = None

        self._init_widget()

    def _draw_base(self):
        """Draw base image"""
        w = self._size[0] * self.M
        h = self._size[1] * self.M
        self.base_image = Image.new("RGBA", (w, h))

    def _set_image(self):
        """Set image to CardButton"""
        w, h = self.base_image.size
        h = int(h * (1 - self._textbox_size_pct))
        image = Image.open(self._image_name)
        image = image.resize(w, h)
        self.base_image.paste(image, (0, 0))

    def _draw_textbox(self):
        """Draw the textbox."""
        w, h = self.base_image.size
        th = int(h * self._textbox_size_pct)
        textbox_image = Image.new("RGBA", size=(w, th), color=self._textbox_color)
        draw = ImageDraw.Draw(textbox_image, "RGBA")
        self._draw_text(draw)
        self._draw_subtext(draw)
        self.base_image.paste(textbox_image, (0, h - th))

    def _draw_text(self, draw: ImageDraw.Draw):
        """Draw the text in the textbox"""
        x = (self._size[0] * self.M) // 2
        y = 15 * self.M
        anchor = "ma"
        font = ImageFont.truetype(self._textfont[0], self._textfont[1] * self.M - 3)
        text = self._get_wrapepd_text(self.text, font, offset=25)
        draw.text(
            xy=(x, y),
            text=text,
            fill=self._text_color,
            font=font,
            anchor=anchor,
            align="center",
            stroke_width=1,
        )
        self.__bbox = draw.textbbox(
            xy=(x, y),
            text=text,
            font=font,
            anchor=anchor,
            align="center",
            stroke_width=1,
        )

    def _draw_subtext(self, draw: ImageDraw.Draw):
        """Draw the subtext in the textbox"""
        font = ImageFont.truetype(self._textfont[0], self._textfont[1] * self.M - 3)

        _, _, _, offset_y = self.__bbox
        actual_y = offset_y + 45
        subtextfont = ImageFont.truetype(
            self._subtextfont[0],
            self._subtextfont[1] * self.M - 3,
        )
        subtext = self._get_wrapepd_text(self.subtext, subtextfont, offset=25)
        draw.multiline_text(
            xy=(20, actual_y),
            text=subtext,
            fill=self._subtext_color,
            font=subtextfont,
            align="left",
        )

    def _get_wrapepd_text(
        self,
        text: str,
        font: ImageFont.FreeTypeFont,
        offset: int = 0,
    ) -> str:
        """Wrap the given text base on the font given. This will make sure the text never go past the width of the base image.

        :param text: Text to wrap.
        :type text: str
        :param font: The font object for custom font.
        :type font: ImageFont.FreeTypeFont
        :param offset: The x offset, defaults to 0
        :type offset: int, optional
        :return: A new fromatted string.
        :rtype: str
        """
        pixel = self.base_image.size[0] - offset
        lines = text.split("\n")
        new_text = [
            ufont.wrap_text(t, pixel, font=font, font_factor=0.97) for t in lines
        ]
        return "\n".join(new_text)

    def _init_widget(self):
        """Initialize the widget by drawing the items in correct order."""
        self._draw_base()
        if self._image_name is not None:
            self._set_image()
        self._draw_textbox()
        image = ctk.CTkImage(self.base_image, size=self._size)
        label = ctk.CTkLabel(self, text="", image=image)
        label.pack()
        label.bind("<Button-1>", self._callback)

    def _callback(self, event):
        """Callback function when the widget is clicked."""
        if self._command is None:
            return
        self._command()
