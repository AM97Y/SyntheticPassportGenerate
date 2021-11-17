import os
from datetime import datetime, date
from random import choice, randint

import numpy as np
import pandas as pd
from faker import Faker

from Sex import Sex
from utils.path_utils import Paths, Resources
from utils.processing_utils import gender_format, load_markup


class Passport:
    def __init__(self):
        self._parameters = {}

    def random_init(self) -> None:
        pass

    @property
    def content(self) -> dict:
        return self._parameters

    def update(self, passport_data: dict) -> None:
        self._parameters.update(passport_data)


class PassportContent(Passport):
    def __init__(self):

        super().__init__()
        self._parameters = {
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
            'images': {'photoLabel': '',
                       'officersignLabel': '',
                       'ownersignLabel': '',
                       'background': ['', {}]
                       }
        }
        self.random_init()

    def random_init(self) -> None:
        """
        This function randomly fills in the content of the passport.

        """

        # FIXED: Remove the cycle.
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


class PassportAppearance(Passport):
    def __init__(self):
        super().__init__()

        self._parameters = {
            'blurCheckBox': True,
            'crumpledCheckBox': True,
            'noiseCheckBox': True,
            'blotsnumSpinBox': 2,
            'flashnumSpinBox': 1,
            'blurFlashnumBlotsnum': 30,
            'fontComboBox': '',
            'color_text': 0,
            'fontsizeSpinBox': 28,
            'fontblurSpinBox': 80,
        }
        self.random_init()

    def random_init(self) -> None:
        """
        This function randomly fills in the appearance of the passport.

        """
        # FIXED: Remove the cycle.
        for key, _ in self._parameters.items():
            if key == 'blurCheckBox' or key == 'crumpledCheckBox' or key == 'noiseCheckBox':
                self._parameters[key] = choice((True, False))
            elif key == 'blotsnumSpinBox' or key == 'flashnumSpinBox':
                self._parameters[key] = np.random.poisson(0.5)
            elif key == 'blurFlashnumBlotsnum':
                self._parameters[key] = int(np.random.normal(35))
            elif key == 'fontblurSpinBox':
                self._parameters[key] = randint(65, 100)
            elif key == 'fontComboBox':
                fonts_list = []
                for file in Resources.fonts():
                    fonts_list.append(file)
                self._parameters[key] = choice(fonts_list)
                del fonts_list
            elif key == 'fontsizeSpinBox':
                self._parameters[key] = int(np.random.normal(35))
