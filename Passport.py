import os
from abc import ABC, abstractmethod
from datetime import datetime, date
from faker import Faker
from random import choice, randint

import numpy as np

from Sex import Sex
from utils.name_utils import gender_format, load_names
from utils.resources_utils import Resources
from utils.processing_utils import load_markup
from utils.request import upload_online_passport_data


class Passport(ABC):
    def __init__(self):
        self._parameters = {}

    @abstractmethod
    def random_init(self) -> None:
        pass

    @property
    def content(self) -> dict:
        return self._parameters

    def update(self, passport_data: dict) -> None:
        self._parameters.update(passport_data)


class PassportContent(Passport):
    """
    This class keeps information about data content of passport
    """

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
            'images': {
                'photoLabel': '',
                'officersignLabel': '',
                'ownersignLabel': '',
                'background': ['', {}]
            }
        }
        self.random_init()

    def random_init(self) -> None:
        """
        This function randomly fills in the content of the passport
        """
        try:
            # Online mode of generating passport data
            self._parameters = upload_online_passport_data(data=self._parameters, browser='Firefox',
                                                           path_driver=Resources.driver())
            self._init_visual_content()
        except Exception:
            # Offline mode of generating passport data
            years_difference = choice(range(14, 30))
            # Fill in the sex of person
            self._parameters['sex'] = str(choice(list(Sex)))
            # Fill in the rest of passport content by keys
            for key, _ in self._parameters.items():
                if key == 'series_passport':
                    self._parameters[key] = randint(1000, 9999)
                elif key == 'number_passport':
                    self._parameters[key] = randint(100000, 999999)
                elif key == 'department_code':
                    self._parameters[key] = [randint(100, 999), randint(100, 999)]
                elif key == 'date_birth':
                    start_date = date(year=1990, month=1, day=1)
                    end_date = date(year=datetime.now().year - years_difference, month=1, day=1)
                    self._parameters[key] = Faker().date_between(start_date=start_date, end_date=end_date)
                elif key == 'date_issue':
                    year = self._parameters['date_birth'].year + years_difference
                    start_date = date(year=year, month=1, day=1)
                    end_date = date(year=year, month=1, day=1)
                    self._parameters[key] = Faker().date_between(start_date=start_date, end_date=end_date)
                if key == 'first_name':
                    self._parameters[key] = choice(load_names(sex=self._parameters['sex']))
                elif key == 'images':
                    self._init_visual_content()
                elif key == 'second_name' or key == 'patronymic_name' or key == 'address' or key == 'department':
                    if os.path.isfile(Resources.dataset(key)):
                        with open(Resources.dataset(key), "r", encoding='utf-8') as f:
                            tmp_choices = [line.strip() for line in f]
                        if key == 'department':
                            self._parameters[key] = choice(tmp_choices)
                        else:
                            self._parameters[key] = gender_format(text=choice(tmp_choices), sex=self._parameters['sex'])
                        del tmp_choices

    def _init_visual_content(self) -> None:
        """
        This function randomly fills in the visual content of the passport.

        """
        # Fill in the photo of person
        path_to_photos = Resources.photo_male() if self._parameters['sex'] == "МУЖ." else Resources.photo_female()
        self._parameters['images']['photoLabel'] = choice(path_to_photos)

        # Fills in pictures of signatures
        path_to_signs = Resources.signs()
        self._parameters['images']['officersignLabel'] = choice(path_to_signs)  # signature of the passport officer
        self._parameters['images']['ownersignLabel'] = choice(path_to_signs)  # signature of the person

        # Fill in passport background
        path_to_backgrounds = Resources.background()
        background = choice(path_to_backgrounds)
        self._parameters['images']['background'] = [background, load_markup(file=background)]


class PassportAppearance(Passport):
    """
    This class keeps information about passport appearance.
    """

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
        for key, _ in self._parameters.items():
            if key == 'blurCheckBox' or key == 'crumpledCheckBox' or key == 'noiseCheckBox':
                self._parameters[key] = choice((True, False))
            elif key == 'blotsnumSpinBox' or key == 'flashnumSpinBox':
                self._parameters[key] = np.random.poisson(0.5)
            elif key == 'blurFlashnumBlotsnum':
                self._parameters[key] = int(np.random.normal(35))
            elif key == 'fontblurSpinBox':
                self._parameters[key] = randint(75, 100)
            elif key == 'fontComboBox':
                self._parameters[key] = choice([file for file in Resources.fonts()])
            elif key == 'fontsizeSpinBox':
                self._parameters[key] = int(np.random.normal(40))
