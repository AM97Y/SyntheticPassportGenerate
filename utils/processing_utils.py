import json
import os

import cv2
import numpy as np
from PIL import Image, ImageFont
from typing import Tuple

from utils.path_utils import Paths


def get_hyphenated_str(text: str, font: ImageFont, w_box: int) -> str:
    """
    Transform the string into text with line breaks

    :param text: text to change by inserting the line breaks
    :param font: text font
    :param w_box: image width
    :return: edited text with line breaks
    """
    width, height = font.getsize(text)
    if width >= w_box:
        result = [i for i, chr in enumerate(text) if chr == ' ']
        # if not result:
        # print('Error get_hyphenated_str') print -> Exception

        for index, pos in enumerate(result):
            if text[pos - 1] == ',':
                text = "\n".join([text[:pos], text[pos + 1:]])

                if font.getsize(text[pos + 3:])[0] < w_box:
                    return text

    text = text.replace(' ', '\n')
    return text


def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_RGB2RGBA))


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2RGB)


def load_markup(file: str) -> Tuple[dict, int]:
    """
    Loading the background markup from file

    :param file: file which stores the background
    :return: background markup
    """
    file_json = file.split(".")[-2] + '.json'
    if os.path.isfile(Paths.backgrounds() / file_json):
        with open(Paths.backgrounds() / file_json, 'r') as f:
            data = json.load(f)
            background_markup = {}
            font_pick = data['font_pick']
            # background_markup = {elem['label']: list(map(lambda x: [int(x[0]), int(x[1])], elem['points']))
            #                     for elem in self.parameters["images"]["background"][1]["shapes"]}
            for elem in data["shapes"]:
                background_markup[elem['label']] = background_markup.get(elem['label'], [])+[list(map(lambda x: [abs(int(x[0])), abs(int(x[1]))], elem['points']))]
            return background_markup, font_pick
    return {}, 0
