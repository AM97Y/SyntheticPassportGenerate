import json
import os

import cv2
import numpy as np
from PIL import Image, ImageFont
from pymorphy2 import MorphAnalyzer
import pandas as pd

from utils.path_utils import Paths


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
    return (parsed[0].inflect({gender, 'nomn'}) or parsed[0]).word.title()


def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_RGB2RGBA))
    # return Image.fromarray(img)


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2RGB)
    # return np.asarray(img)


def load_markup(file: str) -> dict:
    """
    Loading the background markup.

    :param file: File of background.
    :return: Background markup.
    """
    file_json = file.split(".")[-2] + '.json'
    if os.path.isfile(Paths.backgrounds() / file_json):
        with open(Paths.backgrounds() / file_json, 'r') as f:
            data = json.load(f)
            background_markup = {}
            # background_markup = {elem['label']: list(map(lambda x: [int(x[0]), int(x[1])], elem['points']))
            #                     for elem in self.parameters["images"]["background"][1]["shapes"]}

            for elem in data["shapes"]:
                # FIXED: We take only the first occurrence, we need to discuss the issue_place.
                if background_markup.get(elem['label'], None) is None:
                    background_markup.update(
                        {elem['label']: list(map(lambda x: [abs(int(x[0])), abs(int(x[1]))], elem['points']))})

            return background_markup
    return {}


def load_names(sex: str) -> list:
    """
    This function returns names by sex.

    :param sex: Sex of person.
    :return: List of names.
    """
    if sex:
        df = pd.read_csv(Paths.data_passport() / 'male_names.csv', ';')
    else:
        df = pd.read_csv(Paths.data_passport() / 'female_names.csv', ';')
    return df[df.PeoplesCount > 1000]['Name'].tolist()


def get_sex(name: str) -> str:
    """
    This function returns gender by name.

    :param name:
    :return: Sex of person.
    """
    df = pd.read_csv(Paths.data_passport() / 'male_names.csv', ';')
    if df.loc[df.Name == name].count()['Name'] > 0:
        sex = "МУЖ."
    else:
        sex = "ЖЕН."
    return sex
