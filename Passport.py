import json
import os
from datetime import datetime, date, time
from random import choice, randint


class Passport:
    def __init__(self):
        self.passport_data = {
            'firstName': 'Иван',
            'secondName': 'Иванович',
            'patronymicName': 'Иванов',
            'address': 'Г. Ярославль, улица Строителей 77',
            'seriesPassport': 1102,
            'numberPassport': 123685,
            'departmentCode': [888, 999],
            'department': 'УВД',
            'city': 'Ярославль',
            'dateOFbirth': datetime.now(),
            'dateOFissue': datetime.now(),
            'sex': 'МУЖ.',
        }

    def update(self, passport_data):
        self.passport_data.update(passport_data)

    def random_init(self):
        diff = choice((14, 60))
        sex = choice(('МУЖ.', 'ЖЕН.'))
        self.passport_data['sex'] = sex
        for key, _ in self.passport_data.items():
            if key == 'seriesPassport':
                self.passport_data[key] = randint(1000, 9999)
            elif key == 'numberPassport':
                self.passport_data[key] = randint(100000, 999999)
            elif key == 'departmentCode':
                self.passport_data[key] = [randint(100, 999), randint(100, 999)]
            elif key == 'dateOFbirth':
                year = randint(1900, datetime.now().year - diff)
                # Проверить вхождение последнего числа
                month = randint(1, 12)
                # Сделать зависимость от месяца
                day = randint(1, 28)
                self.passport_data[key] = date(year, month, day)
            elif key == 'dateOFissue':
                year = self.passport_data['dateOFbirth'].year + diff
                month = randint(1, 12)
                # Сделать зависимость от месяца
                day = randint(1, 28)
                self.passport_data[key] = date(year, month, day)
            elif key != 'sex':
                tmp_choices = []
                # Сделать проверку на пол, мб прикрутить pymorphy
                if os.path.isfile(f'{os.path.abspath(os.curdir)}/passportDrawer/dataPassport/{key}.txt'):
                    with open(f'{os.path.abspath(os.curdir)}/passportDrawer/dataPassport/{key}.txt', "r") as f:
                        for line in f:
                            tmp_choices.append(line.strip())

                    self.passport_data[key] = choice(tmp_choices)
                del tmp_choices


class GenerateImg:
    def __init__(self, file_background=''):
        self.parameters_generate = {
            'blurCheckBox': True,
            'crumpledCheckBox': True,
            'noiseCheckBox': True,
            'blotsnumSpinBox': 2,
            'flashnumSpinBox': 1,
            'blurFlashnumBlotsnum': 30,
            'fontComboBox': '',
            'fontsizeSpinBox': 18,
            'fontblurSpinBox': 80,
            'images': {'labelFoto': '',
                       'label_signature_1': '',
                       'label_signature_2': '',
                       'background': [file_background, self._load_markup(file_background)]
                       }
        }

    def random_init(self):
        sex = choice(('МУЖ.', 'ЖЕН.'))
        for key, _ in self.parameters_generate.items():
            if key == 'blurCheckBox' or key == 'crumpledCheckBox' or key == 'noiseCheckBox':
                self.parameters_generate[key] = choice((True, False))
            elif key == 'blotsnumSpinBox' or key == 'flashnumSpinBox':
                self.parameters_generate[key] = randint(0, 4)
            elif key == 'blurFlashnumBlotsnum' or key == 'fontblurSpinBox':
                self.parameters_generate[key] = randint(0, 100)
            elif key == 'fontComboBox':
                fonts_list = []
                with open(f'{os.path.abspath(os.curdir)}/passportDrawer/fonts/fonts.txt', "r") as f:
                    for line in f:
                        fonts_list.append(line.strip().split('/')[-1])
                    self.parameters_generate[key] = choice(fonts_list)
                del fonts_list
            elif key == 'fontsizeSpinBox':
                self.parameters_generate[key] = randint(14, 26)

            """
            'images': {'labelFoto': '',
                       'label_signature_1': '',
                       'label_signature_2': '',
                       'background': ["file_background", self._load_markup("file_background")]
                       }
            """


    @staticmethod
    def _load_markup(file):
        # file_background сделать в json файл
        if os.path.isfile(file):
            with open(file, 'w') as f:
                data = json.load(f)
                return data

    def update(self, parameters_generate):
        self.parameters_generate.update(parameters_generate)
