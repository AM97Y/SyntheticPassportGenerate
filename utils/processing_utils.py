import json
import os

import cv2
import numpy as np
from PIL import Image, ImageFont
from pymorphy2 import MorphAnalyzer

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
    return (parsed[0].inflect({gender, 'nomn'}) or parsed[0]).word


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

def load_data():
    diff = choice(range(14, 30))
    fake = Faker()
    sex = str(choice(list(Sex)))
    self._parameters['sex'] = sex
    for key, _ in self._parameters.items():
        if key == 'series_passport':
            self._parameters[key] = randint(1000, 9999)
        elif key == 'number_passport':
            self._parameters[key] = randint(100000, 999999)
        elif key == 'department_code':
            self._parameters[key] = [randint(100, 999), randint(100, 999)]
        elif key == 'date_birth':
            start_date = date(year=1990, month=1, day=1)
            end_date = date(year=datetime.now().year - diff, month=1, day=1)
            self._parameters[key] = fake.date_between(start_date=start_date, end_date=end_date)
        elif key == 'date_issue':
            year = self._parameters['date_birth'].year + diff
            start_date = date(year=year, month=1, day=1)
            end_date = date(year=year, month=1, day=1)
            self._parameters[key] = fake.date_between(start_date=start_date, end_date=end_date)
        if key == 'first_name':
            if self._parameters['sex'] == "МУЖ.":
                df = pd.read_csv(Paths.data_passport() / 'male_names.csv', ';')
            else:
                df = pd.read_csv(Paths.data_passport() / 'female_names.csv', ';')
            tmp_choices = df[df.PeoplesCount > 1000]['Name'].tolist()
            self._parameters[key] = choice(tmp_choices)
            del tmp_choices
        elif key == 'images':
            if sex == "МУЖ.":
                path = Resources.photo_male()
            else:
                path = Resources.photo_female()
            self._parameters[key]['photoLabel'] = choice(path)

            path_signs = Resources.signs()
            self._parameters[key]['officersignLabel'] = choice(path_signs)
            self._parameters[key]['ownersignLabel'] = choice(path_signs)

            path_backgrounds = Resources.background()
            background = choice(path_backgrounds)
            self._parameters[key]['background'] = [background, load_markup(file=background)]
        elif key == 'second_name' or key == 'patronymic_name' or key == 'address' or key == 'department':
            tmp_choices = []
            file = Resources.dataset(key)
            if os.path.isfile(file):
                with open(file, "r", encoding='utf-8') as f:
                    for line in f:
                        tmp_choices.append(line.strip())
                if key == 'department':
                    self._parameters[key] = choice(tmp_choices)
                else:
                    self._parameters[key] = gender_format(text=choice(tmp_choices), sex=sex).title()

            del tmp_choices
    return {}
