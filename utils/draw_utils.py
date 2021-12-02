from random import randint, choice
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple


def get_box_size_to_draw(markup: list, number: bool = False) -> tuple:
    """
    Get box size to draw the text inside

    :param markup: background markup
    :param number: True if it is needed to draw a number
    :return: width and height of the box to draw inside
    """

    left_upper_point = markup[0]
    right_upper_point = markup[1]
    down_point = markup[3]
    if number:
        width = down_point[1] - left_upper_point[1]
        height = width
    else:
        width = right_upper_point[0] - left_upper_point[0]
        height = down_point[1] - left_upper_point[1]
    return width, height


def get_box_corner_to_draw(markup: list, number: bool = False) -> tuple:
    """
    Get the coordinate of left upper box corner to draw inside

    :param markup: background markup
    :param number: True if it is needed to draw a number
    :return: coordinate of left upper box corner
    """
    if number:
        w, h = get_box_size_to_draw(markup=markup)
        return markup[0][0] - (h - w), markup[0][1]
    else:
        return markup[0][0], markup[0][1]


def delete_white_background(img: Image) -> Image:
    """
    Remove the white background on the image

    :param img: image to remove white background
    :return: changed image
    """
    img_signature_1 = img.convert('RGBA')
    arr = np.array(np.asarray(img_signature_1))
    r, g, b, _ = np.rollaxis(arr, axis=-1)
    mask = ((r == 255) & (g == 255) & (b == 255))
    arr[mask, 3] = 0
    img = Image.fromarray(arr, mode='RGBA')
    return img


def get_text_image(text: str, font: ImageFont, size: Tuple[int], color: Tuple[int, int, int],
                   center: bool = True) -> Image:
    """
    Get image with text inside

    :param center: place in the middle or not.
    :param size: image size
    :param color: text color
    :param text: text to draw inside
    :param font: text font
    :return: generated text image
        """
    # text = get_hyphenated_str(text, font, shape[0])
    text = text.upper()
    img_text = Image.new(mode="RGBA", size=size, color=(0, 0, 0, 0))
    drawer = ImageDraw.Draw(im=img_text)
    if center:
        W, H = size
        w, h = drawer.textsize(text, font=font)
        xy = ((W - w) / 2, (H - h) / 2)
    else:
        xy = (0, 0)

    drawer.text(xy=xy, text=text, fill=color, font=font)
    return img_text


def draw_watermark(img: Image, count_watermark: int, files: list, blur: int, params: dict = None) -> Image:
    """
    Draws watermarks with the specified transparency level on the image.

    :param params: paste_point - new watermark sizes; paste_point - if you set the coordinate, then what.
    :param blur: Blur watermarck.
    :param files: List files watermarks.
    :param img: Edited Image.
    :param count_watermark: Number of watermarks.
    :return: Changed image.
    """
    (w, h) = img.size

    if count_watermark > 0:
        for i in range(0, count_watermark):
            with Image.open(choice(files)) as img_watermark:
                img_watermark = img_watermark.convert('RGBA')
                paste_point = params['paste_point'] if params['paste_point'] else (randint(0, w), randint(0, h))
                if params['resize_size'] is not None:
                    img_watermark = img_watermark.resize(size=params['resize_size'], resample=Image.NEAREST)
                paste_mask = img_watermark.split()[3].point(lambda i: i * blur / 100.)
                img.paste(im=img_watermark, box=paste_point, mask=paste_mask)

    return img.convert('RGBA')
