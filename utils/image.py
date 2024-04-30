import math
from PIL import Image, ImageFont, ImageDraw


def load_image(filename, size=None):
    """
    Load an image from filename str

    :param filename: Path to file image
    :param size: A tuple of desire size for the image. If None, then use the original image size. Default None.
    :returns: A Image object to be use in tkinter
    """
    img = Image.open(filename)
    if size is not None:
        img = img.resize(size)
    return img


def generate_text_background(
    text,
    size,
    font_family="arial",
    font_size=16,
    font_color="#000000",
    bg_color="#FFFFFF",
    padding=(0, 0),
):
    """Generate a background image with repeated text.

    :param text: Text to be repeated.
    :type text: str
    :param size: A tuple of width and height of the background image.
    :type size: tuple[int, int]
    :param font_family: String of font family. Can be a ttf file, defaults to "arial"
    :type font_family: str, optional
    :param font_size: The size of the text, defaults to 16
    :type font_size: int, optional
    :param font_color: The color of the text. Can be #rgb, #rrggbb, #rgba or #rrggbbaa format, defaults to "#000000"
    :type font_color: str, optional
    :param bg_color: The color of the background. Can be #rgb, #rrggbb, #rgba or #rrggbbaa format, defaults to "#FFFFFF"
    :type bg_color: str, optional
    :param padding: The x, and y padding beteen text, defaults to (0, 0)
    :type padding: tuple[int, int], optional
    :return: An image.
    :rtype: Image
    """
    base_image = Image.new("RGBA", size, color=bg_color)
    draw = ImageDraw.Draw(base_image, mode="RGBA")
    font = ImageFont.truetype(font_family, font_size)
    font_bbox = font.getbbox(text)
    for i, y in enumerate(range(0, size[1], font_bbox[-1] + padding[1])):
        offset = int(font.getlength(text) // -2) if i % 2 != 0 else 0
        for x in range(offset, size[0] - offset, font_bbox[-2] + padding[0]):
            draw.text((x, y), text, fill=font_color, font=font)
    return base_image


def crop_middle(image, size):
    """Crop the given image at the middle of it in given size.

    :param image: An image to crop
    :type image: Image
    :param size: A tuple of width and height of new image
    :type size: tuple[int, int]
    :return: A new image after being cropped
    :rtype: Image
    """
    new_size = image.size
    left = int(new_size[0] // 2 - size[0] // 2)
    upper = int(new_size[1] // 2 - size[1] // 2)
    right = left + size[0]
    lower = upper + size[1]
    image = image.crop((left, upper, right, lower))
    return image


def cal_square_bg_size(size):
    w, h = size
    t = int(math.sqrt(pow(w, 2) + pow(h, 2)))
    return t, t


def text_bg_builder(text, original_size):
    text = text.upper()
    size = cal_square_bg_size(original_size)
    font_family = "assets/fonts/PublicSans-Bold.ttf"
    font_size = 90
    font_color = "#c7c71922"
    bg_color = "#151515"
    padding = (25, 10)
    image = generate_text_background(
        text,
        size,
        font_family,
        font_size,
        font_color,
        bg_color,
        padding,
    )
    image = image.rotate(45, expand=True)
    image = crop_middle(image, original_size)
    return image
