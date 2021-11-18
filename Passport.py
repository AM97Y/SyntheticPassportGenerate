import os
from datetime import datetime, date
from random import choice, randint

import numpy as np
from faker import Faker

from Sex import Sex
from utils.name_utils import gender_format, load_names
from utils.path_utils import Resources
from utils.processing_utils import load_markup
from utils.request import get_data


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
            'first_name': '',
            'second_name': '',
            'patronymic_name': '',
            'address': '',
            'series_passport': 1,
            'number_passport': 1,
            'department_code': [0, 0],
            'department': '',
            'date_birth': '',
            'date_issue': '',
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
        try:
            # Online data
            print('online')
            self._parameters = get_data(data=self._parameters, browser='Firefox', path_driver=Resources.driver())
            self._init_img()
        except Exception:
            print(Exception)
            # Offline data
            print('offline')
            # Age of obtaining a passport.
            diff = choice(range(14, 30))
            fake = Faker()
            # Sex of person.
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
                    tmp_choices = load_names(sex=self._parameters['sex'])
                    self._parameters[key] = choice(tmp_choices)
                    del tmp_choices
                elif key == 'images':
                    self._init_img()
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
                            self._parameters[key] = gender_format(text=choice(tmp_choices), sex=sex)
                    del tmp_choices

    def _init_img(self) -> None:
        """
        Random init images.

        """
        # Person photo
        if self._parameters['sex'] == "МУЖ.":
            path = Resources.photo_male()
        else:
            path = Resources.photo_female()
        self._parameters['images']['photoLabel'] = choice(path)

        # Signs images.
        path_signs = Resources.signs()
        self._parameters['images']['officersignLabel'] = choice(path_signs)
        self._parameters['images']['ownersignLabel'] = choice(path_signs)

        # Background with markup.
        path_backgrounds = Resources.background()
        background = choice(path_backgrounds)
        self._parameters['images']['background'] = [background, load_markup(file=background)]


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

    def init_img(self):
        pass
