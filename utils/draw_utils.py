import numpy as np
from PIL import Image


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
    Returns the coordinate of corner box to draw.
    :param markup: Background markup  of entity.
    :param number: True if it is needed to draw a number.
    :return: Coordinate of corner box.
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
