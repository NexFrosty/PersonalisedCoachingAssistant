import math
import textwrap
from PIL import Image, ImageDraw, ImageFont


def wrap_text(
    text: str,
    pixel: int,
    font: ImageFont.FreeTypeFont = None,
    font_factor: float = 0.95,
) -> str:
    """Wrape the text so it won't exceed the pixel specified.

    :param text: The text to wrap
    :type text: str
    :param pixel: The maximum pixel.
    :type pixel: int
    :param font: For custom font, defaults to None
    :type font: ImageFont.FreeTypeFont, optional
    :return: Wrapped text.
    :rtype: str
    """
    if font is None:
        font = ImageFont.truetype("arial", 18)
    letters = set(text)
    avg_size = sum(font.getlength(c) for c in letters) / len(letters) * font_factor
    max_c = math.floor(pixel / avg_size)

    new_string = textwrap.fill(text, max_c)
    return new_string


class RenderFont:
    def __init__(self, filename):
        """
        Create a RenderFont

        :param filename: The filename of the ttf font file
        :type filename: str
        """
        self._file = filename
        self._image = None

    def get_render(
        self, text, font_size=18, fill=(0, 0, 0), type_="normal", align="left"
    ) -> Image.Image:
        """
        Create transparent PIL image that contains the text

        :param text: Text to be render as PIL Image
        :type text: str
        :param font_size: An int represent the size of the text. Default 18
        :type font_size: int
        :param fill: A tuple of RGB value for the text color
        :type fill: tuple[R, G, B]
        :param type_: Type of the text, "normal", "bold"
        :type type_: str
        :return: A PIL.Image consist of rendered text on transparent background
        :rtype: PIL.Image
        """
        font = ImageFont.truetype(font=self._file, size=font_size)
        mx_txt_len = max(text.split("\n"), key=len)
        width = int(font.getlength(mx_txt_len)) + 15
        _, _, _, height = font.getbbox(text)
        height = height * len(text.split("\n"))
        self._image = Image.new(mode="RGBA", size=(width, height))
        text_render = ImageDraw.Draw(self._image, "RGBA")

        stroke_width = 0
        stroke_fill = None
        if type_ == "bold":
            stroke_width = 1
            stroke_fill = fill

        text_render.text(
            (width / 2, height / 2),
            text,
            fill=fill,
            anchor="mm",
            align=align,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
            font=font,
        )
        return self._image

    def _count_line(self, text: str) -> int:
        """Count the number of lines.

        :param text: The text to count
        :type text: str
        :return: The number of lines
        :rtype: int
        """
        return text.count("\n") + 1

    def _longest_line_length(self, text: str) -> int:
        """Get the longest line length.

        :param text: The text to get the longest line length
        :type text: str
        :return: The longest line length
        :rtype: int
        """
        return len(max(text.split("\n"), key=len))
