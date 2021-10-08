import json
import os
from copy import deepcopy
from datetime import datetime, date, time
from random import choice, randint
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Passport:
    def __init__(self):
        self.passport_data = {
            'firstName': 'Иван',
            'secondName': 'Иванов',
            'patronymicName': 'Иванович',
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
                if os.path.isfile(f'{os.path.abspath(os.curdir)}/dataPassport/{key}.txt'):
                    with open(f'{os.path.abspath(os.curdir)}/dataPassport/{key}.txt', "r") as f:
                        for line in f:
                            tmp_choices.append(line.strip())

                    self.passport_data[key] = choice(tmp_choices)
                del tmp_choices


class GenerateImg:
    def __init__(self, file_background='8QfxS6biN-w.jpg'):
        self.parameters_generate = {
            'blurCheckBox': True,
            'crumpledCheckBox': True,
            'noiseCheckBox': True,
            'blotsnumSpinBox': 2,
            'flashnumSpinBox': 1,
            'blurFlashnumBlotsnum': 30,
            'fontComboBox': '',
            'fontsizeSpinBox': 28,
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
                with open(f'{os.path.abspath(os.curdir)}/fonts/fonts.txt', "r") as f:
                    for line in f:
                        fonts_list.append(line.strip().split('/')[-1])
                    self.parameters_generate[key] = choice(fonts_list)
                del fonts_list
            elif key == 'fontsizeSpinBox':
                self.parameters_generate[key] = randint(14, 30)

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
        # Правильнее наоборот искать?
        file_json = f'{os.path.abspath(os.curdir)}/background/{file.split(".")[-2]}.json'
        print(file_json)
        if os.path.isfile(file_json):
            with open(file_json, 'r') as f:
                data = json.load(f)
                return data

    def update(self, parameters_generate):
        self.parameters_generate.update(parameters_generate)

    def _write_series_and_number(self, text, font, shape):
        print(shape)
        img_text = Image.new("RGBA", shape, (0, 0, 0, 0))
        drawer = ImageDraw.Draw(img_text)
        drawer.text((0, 0), text, fill=(153, 103, 105), font=font,
                    stroke_width=0,
                    stroke_fill=(0, 0, 0))
        # ImageDraw.Draw(img_text)
        return img_text

    def _get_hyphenated_str(self, text, font, width_img):
        # Декаратор поднятия регистра?

        width, height = font.getsize(text)
        if font.getsize(text)[0] >= width_img:
            result = [i for i, chr in enumerate(text) if chr == ' ']
            if result == []:
                print('Error')

            for index, pos in enumerate(result):
                if text[pos - 1] == ',':
                    text = "\n".join([text[:pos], text[pos + 1:]])

                    if font.getsize(text[pos + 3:])[0] < width_img:
                        return text

        text = text.replace(' ', '\n')
        return text

    def _draw_text(self, text, font, shape):
        # text = self._get_hyphenated_str(text, font, shape[0])
        print(shape, text)
        img_text = Image.new("RGBA", shape, (0, 0, 0, 0))
        drawer = ImageDraw.Draw(img_text)
        drawer.text((0, 0), text, fill=(50, 50, 50), font=font,
                    stroke_width=0,
                    stroke_fill=(0, 0, 0))
        # ImageDraw.Draw(img)

        return img_text

    def _get_box_size(self, markup_origin, number=False) -> tuple:

        markup = deepcopy(markup_origin)
        print(markup)
        left_upper_point = markup[0]  # min(markup)
        del markup[markup.index(left_upper_point)]
        print('min', left_upper_point)

        right_upper_point = min(markup, key=lambda x: x[0])
        del markup[markup.index(right_upper_point)]

        down_point = max(markup, key=lambda y: y[1])
        print(left_upper_point, right_upper_point, down_point)
        print(right_upper_point[1], left_upper_point[1])

        if number:
            # y, x
            return right_upper_point[1] - left_upper_point[1], down_point[0] - left_upper_point[0]
        else:
            # x, y
            return down_point[0] - left_upper_point[0], right_upper_point[1] - left_upper_point[1]

    def _get_place(self, markup) -> tuple:
        return markup[0][0], markup[0][1]
        # tuple(min(markup))

    def create_image(self, passport_data):
        print(self.parameters_generate, passport_data)
        with Image.open(f'{os.path.abspath(os.curdir)}/background/'
                        f'{self.parameters_generate["images"]["background"][0]}') as img:
            img = img.convert('RGBA')
            font = ImageFont.truetype(f'{os.path.abspath(os.curdir)}/fonts/'
                                      f'{self.parameters_generate["fontComboBox"]}',
                                      self.parameters_generate["fontsizeSpinBox"])

            background_markup = {elem['label']: list(map(lambda x: [int(x[0]), int(x[1])], elem['points']))
                                 for elem in self.parameters_generate["images"]["background"][1]["shapes"]}

            # Что-то сделать со строчками
            print(self._get_place(background_markup["issue_place"]))
            img_text = self._draw_text(passport_data['department'], font,
                                       self._get_box_size(background_markup["issue_place"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["issue_place"]), img_text)

            font_numbers = ImageFont.truetype(f'{os.path.abspath(os.curdir)}'
                                              f'/fonts/a_SeriferNr_Bold.ttf', 14)
            img_text = self._write_series_and_number(" ".join([str(passport_data['seriesPassport']),
                                                               str(passport_data['numberPassport'])]),
                                                     font_numbers,
                                                     self._get_box_size(background_markup["number_group1"],
                                                                        number=True))
            img_text = img_text.rotate(270)
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["number_group1"]), img_text)

            img_text = self._write_series_and_number(" ".join([str(passport_data['seriesPassport']),
                                                               str(passport_data['numberPassport'])]),
                                                     font_numbers,
                                                     self._get_box_size(background_markup["number_group2"],
                                                                        number=True))
            img_text = img_text.rotate(270)
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["surname"]), img_text)

            img_text = self._draw_text(passport_data['secondName'], font,
                                       self._get_box_size(background_markup["surname"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["surname"]), img_text)

            print(len(background_markup["surname"]))
            img_text = self._draw_text(passport_data['firstName'], font,
                                       self._get_box_size(background_markup["name"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["name"]), img_text)

            img_text = self._draw_text(passport_data['patronymicName'], font,
                                       self._get_box_size(background_markup["patronymic"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["patronymic"]), img_text)

            img_text = self._draw_text(passport_data['address'], font,
                                       self._get_box_size(background_markup["birth_place"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["birth_place"]), img_text)

            img_text = self._draw_text("-".join(map(str, passport_data['departmentCode'])), font,
                                       self._get_box_size(background_markup["code"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["code"]), img_text)

            img_text = self._draw_text(passport_data['dateOFbirth'].strftime("%m.%d.%Y"), font,
                                       self._get_box_size(background_markup["birth_date"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["birth_date"]), img_text)

            img_text = self._draw_text(passport_data['dateOFissue'].strftime("%m.%d.%Y"), font,
                                       self._get_box_size(background_markup["issue_date"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["issue_date"]), img_text)

            img_text = self._draw_text(passport_data['sex'], font,
                                       self._get_box_size(background_markup["sex"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["sex"]), img_text)

        return img
