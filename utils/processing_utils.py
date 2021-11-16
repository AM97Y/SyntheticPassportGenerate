import cv2
import numpy as np
from PIL import Image, ImageFont
from pymorphy2 import MorphAnalyzer


def get_hyphenated_str(text: str, font: ImageFont, width_img: int) -> str:
    """
    Transform the string into text with line breaks.
    :param text: Text to change.
    :param font: Read font.
    :param width_img: Width image.
    :return: Edited text.
    """

    width, height = font.getsize(text)
    if font.getsize(text)[0] >= width_img:
        result = [i for i, chr in enumerate(text) if chr == ' ']
        # if not result:
        # print('Error get_hyphenated_str') print -> Exception

        for index, pos in enumerate(result):
            if text[pos - 1] == ',':
                text = "\n".join([text[:pos], text[pos + 1:]])

                if font.getsize(text[pos + 3:])[0] < width_img:
                    return text

    text = text.replace(' ', '\n')
    return text


def gender_format(text: str, sex: str) -> str:
    parsed = MorphAnalyzer().parse(text)
    if sex == "ЖЕН.":
        gender = 'femn'
    else:
        gender = 'masc'
    return (parsed[0].inflect({gender, 'nomn'}) or parsed[0]).word


def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_RGB2RGBA))
    # return Image.fromarray(img)


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2RGB)
    # return np.asarray(img)
