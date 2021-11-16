from random import randint, choice

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple


def get_box_size_to_draw(markup: dict, number=False) -> tuple:
    """
    Get box size to draw the text insides.

    :param markup: Background markup of entity.
    :param number: True if it is needed to draw a number.
    :return: Width and height of the box.
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


def get_box_corner_to_draw(markup, number=False) -> tuple:
    """
    Returns the coordinate of corner box to draw

    :param markup: Background markup  of entity
    :param number: True if it is needed to draw a number
    :return: Coordinate of corner box
    """

    if number:
        # Чтобы от этого избавиться, надо найти как вставлять по вернему левому углу.
        extra_space = get_box_size_to_draw(markup)
        return markup[0][0] - (extra_space[1] - extra_space[0]), markup[0][1]
    else:
        return markup[0][0], markup[0][1]


def delete_white_background(img):
    """
    Remove the white background on the image.
    :param img: Image.
    :return: Changed image.
    """
    img_signature_1 = img.convert('RGBA')
    arr = np.array(np.asarray(img_signature_1))
    r, g, b, a = np.rollaxis(arr, axis=-1)
    mask = ((r == 255) & (g == 255) & (b == 255))
    arr[mask, 3] = 0
    img = Image.fromarray(arr, mode='RGBA')
    return img


def get_text_image(text: str, font: ImageFont, size: Tuple[int], color: Tuple[int, int, int]) -> Image:
    """
        This function draws text in background.
        :param size:
        :param color:
        :param text: Drawing text.
        :param font: Read font.
        :return: Changed image.
        """
    # text = get_hyphenated_str(text, font, shape[0])
    text = text.upper()

    img_text = Image.new("RGBA", size, (0, 0, 0, 0))
    drawer = ImageDraw.Draw(img_text)
    drawer.text((0, 0), text, fill=color, font=font)

    return img_text


def draw_watermark(img, count_watermark: int, files, blur, params = None):
    """
    TDraws watermarks with the specified transparency level on the image.

    :param img: Image.
    :param count_watermark: Number of watermarks.
    :param path: The folder where watermarks.
    :param random_point: Set the coordinate of the location or choose randomly.
    :param paste_point: If you set the coordinate, then what.
    :param resize_size: New watermark sizes.
    :return: Changed image..
    """
    (w, h) = img.size

    if count_watermark > 0:
        for i in range(0, count_watermark):
            with Image.open(choice(files)) as img_watermark:
                img_watermark = img_watermark.convert('RGBA')
                if params:
                    if params['paste_point']:
                        paste_point = params['paste_point']
                    else:
                        paste_point = (randint(0, w), randint(0, h))
                    if params['resize_size'] is not None:
                        img_watermark = img_watermark.resize(params['resize_size'], Image.NEAREST)

                paste_mask = img_watermark.split()[3].point(lambda i: i * blur / 100.)
                img.paste(img_watermark, paste_point, mask=paste_mask)

    return img.convert('RGBA')
