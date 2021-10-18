import json
import os
from datetime import datetime, date
from random import choice, randint

import pandas as pd
from faker import Faker
from pymorphy2 import MorphAnalyzer

from Sex import Sex
from utils.path_utils import Paths


class Passport:
    def __init__(self):
        self.parameters = {}

    def random_init(self) -> None:
        pass

    def update(self, passport_data) -> None:
        self.parameters.update(passport_data)


class PassportContent(Passport):
    def __init__(self):

        super().__init__()
        file_background = '8QfxS6biN-w.jpg'
        # Временно, пото сделать тоже выбор или рандом
        self.parameters = {
            'first_name': 'Иван',
            'second_name': 'Иванов',
            'patronymic_name': 'Иванович',
            'address': 'Г. Ярославль, улица Строителей 77',
            'series_passport': 1102,
            'number_passport': 123685,
            'department_code': [888, 999],
            'department': 'УВД',
            'date_birth': datetime.now(),
            'date_issue': datetime.now(),
            'sex': 'МУЖ.',
            'images': {'label_photo': '',
                       'label_signature_1': '',
                       'label_signature_2': '',
                       'background': [file_background, self._load_markup(file_background)]
                       }
        }
        self.morph = MorphAnalyzer()
        self.random_init()

    def random_init(self) -> None:
        # Убрать цикл?
        diff = choice(range(14, 30))
        fake = Faker()
        sex = str(choice(list(Sex)))
        self.parameters['sex'] = sex
        for key, _ in self.parameters.items():
            if key == 'series_passport':
                self.parameters[key] = randint(1000, 9999)
            elif key == 'number_passport':
                self.parameters[key] = randint(100000, 999999)
            elif key == 'department_code':
                self.parameters[key] = [randint(100, 999), randint(100, 999)]
            elif key == 'date_birth':
                start_date = date(year=1990, month=1, day=1)
                end_date = date(year=datetime.now().year - diff, month=1, day=1)
                # print(start_date, end_date)
                self.parameters[key] = fake.date_between(start_date=start_date, end_date=end_date)
            elif key == 'date_issue':
                year = self.parameters['date_birth'].year + diff
                start_date = date(year=year, month=1, day=1)
                end_date = date(year=year, month=1, day=1)
                # print(start_date, end_date)
                self.parameters[key] = fake.date_between(start_date=start_date, end_date=end_date)

            if key == 'first_name':
                if self.parameters['sex'] == "МУЖ.":
                    df = pd.read_csv(Paths.data_passport() / 'male_names.csv', ';')
                else:
                    df = pd.read_csv(Paths.data_passport() / 'female_names.csv', ';')
                tmp_choices = df['Name'].tolist()
                self.parameters[key] = choice(tmp_choices)
                del tmp_choices
            elif key == 'images':
                if sex == "МУЖ.":
                    path = Paths.photo_male()
                else:
                    path = Paths.photo_female()
                path_blots = os.listdir(path)
                self.parameters[key]['label_photo'] = path / choice(path_blots)

                path_sign = Paths.signs()
                path_blots = os.listdir(path_sign)
                self.parameters[key]['label_signature_1'] = path_sign / choice(path_blots)
                self.parameters[key]['label_signature_2'] = path_sign / choice(path_blots)
            elif key == 'upperCheckBox':
                self.parameters[key] = choice((True, False))
            elif key == 'second_name' or key == 'patronymic_name' or key == 'address' or key == 'department':
                tmp_choices = []
                # Сделать проверку на пол, мб прикрутить pymorphy или аналог
                file = Paths.file_dataset(key)
                if os.path.isfile(file):
                    with open(file, "r") as f:
                        for line in f:
                            tmp_choices.append(line.strip())
                    if key == 'address' or key == 'department':
                        self.parameters[key] = choice(tmp_choices)
                    else:
                        self.parameters[key] = self._gender_format(choice(tmp_choices), sex).title()

                del tmp_choices

    def _gender_format(self, text, sex) -> str:
        print(text)
        parsed = self.morph.parse(text)
        if sex == "ЖЕН.":
            gender = 'femn'
        else:
            gender = 'masc'
        return (parsed[0].inflect({gender, 'nomn'}) or parsed[0]).word

    @staticmethod
    def _load_markup(file) -> dict:
        # file_background сделать в json файл
        # Правильнее наоборот искать?
        file_json = file.split(".")[-2] + '.json'
        # print(file_json)
        if os.path.isfile(Paths.backgrounds() / file_json):
            with open(Paths.backgrounds() / file_json, 'r') as f:
                data = json.load(f)
                background_markup = {}
                # background_markup = {elem['label']: list(map(lambda x: [int(x[0]), int(x[1])], elem['points']))
                #                     for elem in self.parameters["images"]["background"][1]["shapes"]}

                for elem in data["shapes"]:
                    # Берем только первое вхождение, надо обсудить issue_place.
                    if background_markup.get(elem['label'], None) is None:
                        background_markup.update(
                            {elem['label']: list(map(lambda x: [abs(int(x[0])), abs(int(x[1]))], elem['points']))})

                return background_markup
        return {}


class PassportAppearance(Passport):
    def __init__(self):
        super().__init__()

        self.parameters = {
            'blurCheckBox': True,
            'crumpledCheckBox': True,
            'noiseCheckBox': True,
            'blotsnumSpinBox': 2,
            'flashnumSpinBox': 1,
            'blurFlashnumBlotsnum': 30,
            'fontComboBox': '',
            'upperCheckBox': True,
            'color_text': (0, 0, 0),
            'fontsizeSpinBox': 28,
            'fontblurSpinBox': 80,
        }
        self.random_init()

    def random_init(self) -> None:
        # Убрать цикл?
        for key, _ in self.parameters.items():
            if key == 'blurCheckBox' or key == 'crumpledCheckBox' or key == 'noiseCheckBox':
                self.parameters[key] = choice((True, False))
            elif key == 'blotsnumSpinBox' or key == 'flashnumSpinBox':
                self.parameters[key] = randint(0, 4)
            elif key == 'blurFlashnumBlotsnum' or key == 'fontblurSpinBox':
                self.parameters[key] = randint(0, 100)
            elif key == 'fontComboBox':
                fonts_list = []
                for file in os.listdir(Paths.fonts()):
                    fonts_list.append(file)
                self.parameters[key] = choice(fonts_list)
                del fonts_list
            elif key == 'fontsizeSpinBox':
                self.parameters[key] = randint(14, 30)
            # elif key == 'color_text':
            #    pix = randint(120, 200)
            #    self.parameters[key] = (pix, pix, pix)
