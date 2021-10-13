import json
import os
from copy import deepcopy
from datetime import datetime, date
from random import choice, randint

import numpy as np
from PIL import Image, ImageFilter, ImageOps
from PIL import ImageDraw
from PIL import ImageFont


class Passport:
    def __init__(self):

        self.passport_data = {
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
        }

    def update(self, passport_data):
        self.passport_data.update(passport_data)

    def random_init(self):
        diff = choice((14, 60))
        sex = choice(('МУЖ.', 'ЖЕН.'))
        self.passport_data['sex'] = sex
        for key, _ in self.passport_data.items():
            if key == 'series_passport':
                self.passport_data[key] = randint(1000, 9999)
            elif key == 'number_passport':
                self.passport_data[key] = randint(100000, 999999)
            elif key == 'department_code':
                self.passport_data[key] = [randint(100, 999), randint(100, 999)]
            elif key == 'date_birth':
                year = randint(1900, datetime.now().year - diff)
                # Проверить вхождение последнего числа
                month = randint(1, 12)
                # Сделать зависимость от месяца
                day = randint(1, 28)
                self.passport_data[key] = date(year, month, day)
            elif key == 'date_issue':
                year = self.passport_data['date_birth'].year + diff
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
            'upperCheckBox': True,
            'color_text': (0, 0, 0),
            'fontsizeSpinBox': 28,
            'fontblurSpinBox': 80,
            'images': {'labelFoto': '',
                       'label_signature_1': '',
                       'label_signature_2': '',
                       'background': [file_background, self._load_markup(file_background)]
                       }
        }
        self.random_init()

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
            elif key == 'images':
                path = f'{os.path.abspath(os.curdir)}/Foto/'
                path_blots = os.listdir(f'{path}')
                self.parameters_generate[key]['labelFoto'] = path + choice(path_blots)

                path = f'{os.path.abspath(os.curdir)}/signs/'
                path_blots = os.listdir(f'{path}')
                self.parameters_generate[key]['label_signature_1'] = path + choice(path_blots)
                self.parameters_generate[key]['label_signature_2'] = path + choice(path_blots)
            elif key == 'upperCheckBox':
                self.parameters_generate[key] = choice((True, False))
            elif key == 'color_text':
                pix = randint(120, 200)
                self.parameters_generate[key] = (pix, pix, pix)

            """
            'images': {'labelFoto': '',
                       'label_signature_1': '',
                       'label_signature_2': '',
                       'background': ["file_background", self._load_markup("file_background")]
                       }
            """

    @staticmethod
    def _load_markup(file) -> dict:
        # file_background сделать в json файл
        # Правильнее наоборот искать?
        file_json = f'{os.path.abspath(os.curdir)}/background/{file.split(".")[-2]}.json'
        print(file_json)
        if os.path.isfile(file_json):
            with open(file_json, 'r') as f:
                data = json.load(f)
                background_markup = {}
                # background_markup = {elem['label']: list(map(lambda x: [int(x[0]), int(x[1])], elem['points']))
                #                     for elem in self.parameters_generate["images"]["background"][1]["shapes"]}

                for elem in data["shapes"]:
                    # Берем только первое вхождение, надо обсудить issue_place.
                    if background_markup.get(elem['label'], None) is None:
                        background_markup.update(
                            {elem['label']: list(map(lambda x: [abs(int(x[0])), abs(int(x[1]))], elem['points']))})

                return background_markup
        return {}

    def update(self, parameters_generate) -> None:
        self.parameters_generate.update(parameters_generate)

    def _get_hyphenated_str(self, text, font, width_img) -> str:
        # Декаратор поднятия регистра?

        width, height = font.getsize(text)
        if font.getsize(text)[0] >= width_img:
            result = [i for i, chr in enumerate(text) if chr == ' ']
            if not result:
                print('Error _get_hyphenated_str')

            for index, pos in enumerate(result):
                if text[pos - 1] == ',':
                    text = "\n".join([text[:pos], text[pos + 1:]])

                    if font.getsize(text[pos + 3:])[0] < width_img:
                        return text

        text = text.replace(' ', '\n')
        return text

    def _draw_text(self, text, font, shape, number=False):
        # text = self._get_hyphenated_str(text, font, shape[0])
        if self.parameters_generate['upperCheckBox']:
            text = text.upper()

        img_text = Image.new("RGBA", shape, (0, 0, 0, 0))
        drawer = ImageDraw.Draw(img_text)
        if number:
            color = (130, 30, 30)
        else:
            color = self.parameters_generate['color_text']
        print(text, font, shape)
        drawer.text((0, 0), text, fill=color, font=font,
                    stroke_width=0,
                    stroke_fill=(0, 0, 0))

        return img_text

    def _get_box_size(self, markup_origin, number=False) -> tuple:

        markup = deepcopy(markup_origin)
        print(markup)
        left_upper_point = markup[0]  # min(markup)
        # del markup[markup.index(left_upper_point)]

        right_upper_point = markup[1]  # min(markup, key=lambda x: x[0])
        # del markup[markup.index(right_upper_point)]

        down_point = markup[3]  # max(markup, key=lambda y: y[1])
        print(left_upper_point, right_upper_point, down_point)

        if number:
            x = down_point[1] - left_upper_point[1]
            y = x

        else:
            x = right_upper_point[0] - left_upper_point[0]
            y = down_point[1] - left_upper_point[1]
            print(x, y)

        return x, y

    def _get_place(self, markup, number=False) -> tuple:
        if number:
            # Чтобы от этого избавиться, надо найти как вставлять по вернему левому углу.
            extra_space = self._get_box_size(markup)
            return markup[0][0] - (extra_space[1] - extra_space[0]), markup[0][1]
        else:
            return markup[0][0], markup[0][1]

    def _draw_watermark(self, img, count_watermark, path, random_point=False, paste_point=(0, 0),
                        resize_size=None):
        (w, h) = img.size
        if count_watermark > 0:
            path_blots = os.listdir(f'{path}')
            for i in range(0, count_watermark):
                with Image.open(f'{path}/{choice([x for x in path_blots])}') as img_watermark:
                    img_watermark = img_watermark.convert('RGBA')
                    if random_point:
                        paste_point = (randint(0, w), randint(0, h))

                    if resize_size is not None:
                        img_watermark = img_watermark.resize(resize_size, Image.NEAREST)

                    paste_mask = img_watermark.split()[3].point(
                        lambda i: i * self.parameters_generate['blurFlashnumBlotsnum'] / 100.)

                    img.paste(img_watermark, paste_point, mask=paste_mask)
        return img.convert('RGBA')

    def _overlay_artifacts(self, img):

        count_watermark = self.parameters_generate['blotsnumSpinBox']
        path = f'{os.path.abspath(os.curdir)}/dirty/'
        img = self._draw_watermark(img, count_watermark, path)

        count_watermark = self.parameters_generate['flashnumSpinBox']
        path = f'{os.path.abspath(os.curdir)}/glares/'
        img = self._draw_watermark(img, count_watermark, path)

        if self.parameters_generate['crumpledCheckBox']:
            path = f'{os.path.abspath(os.curdir)}/crumpled paper/'
            markup = self.parameters_generate["images"]["background"][1]['passport']
            img = self._draw_watermark(img, 1, path, paste_point=self._get_place(markup),
                                       resize_size=self._get_box_size(markup))
            img = ImageOps.autocontrast(img.convert('RGB'), cutoff=2, ignore=2)

        if self.parameters_generate['blurCheckBox']:
            img = img.filter(ImageFilter.BLUR)

        if self.parameters_generate['noiseCheckBox']:
            img = img.filter(ImageFilter.MinFilter(3))

        return img

    def _delete_signature_background(self, img):
        img_signature_1 = img.convert('RGBA')
        arr = np.array(np.asarray(img_signature_1))
        r, g, b, a = np.rollaxis(arr, axis=-1)
        mask = ((r == 255) & (g == 255) & (b == 255))
        arr[mask, 3] = 0
        img = Image.fromarray(arr, mode='RGBA')
        return img

    def create_image(self, passport_data):
        with Image.open(f'{os.path.abspath(os.curdir)}/background/'
                        f'{self.parameters_generate["images"]["background"][0]}') as img:
            img = img.convert('RGBA')
            background_markup = self.parameters_generate["images"]["background"][1]
            font = ImageFont.truetype(f'{os.path.abspath(os.curdir)}/fonts/'
                                      f'{self.parameters_generate["fontComboBox"]}',
                                      self.parameters_generate["fontsizeSpinBox"])

            img_text = self._draw_text(passport_data['department'], font,
                                       self._get_box_size(background_markup["issue_place"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["issue_place"]), img_text)

            font_numbers = ImageFont.truetype(f'{os.path.abspath(os.curdir)}'
                                              f'/fonts/a_SeriferNr_Bold.ttf',
                                              self.parameters_generate["fontsizeSpinBox"])
            img_text = self._draw_text(" ".join([str(passport_data['series_passport']),
                                                 str(passport_data['number_passport'])]),
                                       font_numbers,
                                       self._get_box_size(background_markup["number_group1"], number=True),
                                       number=True)
            img_text = img_text.rotate(270)
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["number_group1"], number=True),
                      img_text)

            print(" ".join([str(passport_data['series_passport']), str(passport_data['number_passport'])]),
                  background_markup["number_group2"],
                  self._get_box_size(background_markup["number_group2"]))
            img_text = self._draw_text(" ".join([str(passport_data['series_passport']),
                                                 str(passport_data['number_passport'])]),
                                       font_numbers,
                                       self._get_box_size(background_markup["number_group2"], number=True),
                                       number=True)

            img_text = img_text.rotate(270)
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["number_group2"], number=True),
                      img_text)

            img_text = self._draw_text(passport_data['second_name'], font,
                                       self._get_box_size(background_markup["surname"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["surname"]), img_text)

            img_text = self._draw_text(passport_data['first_name'], font,
                                       self._get_box_size(background_markup["name"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["name"]), img_text)

            img_text = self._draw_text(passport_data['patronymic_name'], font,
                                       self._get_box_size(background_markup["patronymic"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["patronymic"]), img_text)

            img_text = self._draw_text(passport_data['address'], font,
                                       self._get_box_size(background_markup["birth_place"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["birth_place"]), img_text)

            img_text = self._draw_text("-".join(map(str, passport_data['department_code'])), font,
                                       self._get_box_size(background_markup["code"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["code"]), img_text)

            img_text = self._draw_text(passport_data['date_birth'].strftime("%m.%d.%Y"), font,
                                       self._get_box_size(background_markup["birth_date"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["birth_date"]), img_text)

            img_text = self._draw_text(passport_data['date_issue'].strftime("%m.%d.%Y"), font,
                                       self._get_box_size(background_markup["issue_date"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["issue_date"]), img_text)

            img_text = self._draw_text(passport_data['sex'], font,
                                       self._get_box_size(background_markup["sex"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["sex"]), img_text)

            # Foto
            with Image.open(self.parameters_generate['images']['labelFoto']) as img_photo:
                img_photo = img_photo.resize(self._get_box_size(background_markup["photo"], Image.NEAREST))
                img.paste(img_photo, self._get_place(background_markup["photo"]))

            with Image.open(self.parameters_generate['images']['label_signature_1']) as img_signature_1:
                img_signature_1 = self._delete_signature_background(img_signature_1)
                img_signature_1 = img_signature_1.resize(
                    self._get_box_size(background_markup["signature"], Image.NEAREST))

                paste_point = self._get_place(background_markup["signature"])
                img.paste(img_signature_1, paste_point, mask=img_signature_1)

            """with Image.open(self.parameters_generate['images']['label_signature_2']) as img_signature_2:
                img_signature_2 = img_signature_2.resize(self._get_box_size(background_markup["signature"], Image.NEAREST))
                img.paste(img_signature_2.convert('RGBA'), self._get_place(background_markup["signature"]))"""

            img = self._overlay_artifacts(img)

        return img


