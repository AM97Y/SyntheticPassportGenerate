import json
import os
from copy import deepcopy
from datetime import datetime, date
from random import choice, randint

from PIL import Image, ImageFilter
from PIL import ImageDraw
from PIL import ImageFont


class Passport:
    def __init__(self):
        self.color_text = (0, 0, 0)
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
        self.random_init()

    def random_init(self):
        self._set_random_color()
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
                return data
        return {} # Посмотреть формат

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
        print(shape, text)
        img_text = Image.new("RGBA", shape, (0, 0, 0, 0))
        drawer = ImageDraw.Draw(img_text)
        if number:
            color = (130, 30, 30)
        else:
            color = self.color_text
        drawer.text((0, 0), text, fill=color, font=font,
                    stroke_width=0,
                    stroke_fill=(0, 0, 0))

        return img_text

    def _get_box_size(self, markup_origin, number=False) -> tuple:

        markup = deepcopy(markup_origin)

        left_upper_point = markup[0]  # min(markup)
        del markup[markup.index(left_upper_point)]

        right_upper_point = min(markup, key=lambda x: x[0])
        del markup[markup.index(right_upper_point)]

        down_point = max(markup, key=lambda y: y[1])
        print(left_upper_point, right_upper_point, down_point)

        if number:
            return right_upper_point[1] - left_upper_point[1], right_upper_point[1] - left_upper_point[1]
        else:
            # x, y
            return down_point[0] - left_upper_point[0], right_upper_point[1] - left_upper_point[1]

    def _get_place(self, markup, number=False) -> tuple:
        if number:
            # Чтобы от этого избавиться, надо найти как вставлять по вернему левому углу.
            extra_space = self._get_box_size(markup)
            return markup[0][0] - (extra_space[1] - extra_space[0]), markup[0][1]
        else:
            return markup[0][0], markup[0][1]

    def _set_random_color(self) -> None:
        pix = randint(120, 200)
        self.color_text = (pix, pix, pix)

    def _draw_watermark(self, img, count_watermark, path, resize=False):
        (w, h) = img.size
        if count_watermark > 0:
            path_blots = os.listdir(f'{path}')
            for i in range(0, count_watermark):
                with Image.open(f'{path}/{choice([x for x in path_blots])}') as img_watermark:
                    img_watermark = img_watermark.convert('RGBA')
                    if resize:
                        point = (0, 0)
                        img_watermark = img_watermark.resize((w, h), Image.NEAREST)
                    else:
                        point = (randint(0, w), randint(0, h))

                    paste_mask = img_watermark.split()[3].point(
                        lambda i: i * self.parameters_generate['blurFlashnumBlotsnum'] / 100.)
                    img.paste(img_watermark, point, mask=paste_mask)
        return img

    def _overlay_artifacts(self, img):

        count_watermark = self.parameters_generate['blotsnumSpinBox']
        path = f'{os.path.abspath(os.curdir)}/dirty/'
        img = self._draw_watermark(img, count_watermark, path)

        count_watermark = self.parameters_generate['flashnumSpinBox']
        path = f'{os.path.abspath(os.curdir)}/glares/'
        img = self._draw_watermark(img, count_watermark, path)

        if self.parameters_generate['crumpledCheckBox']:
            path = f'{os.path.abspath(os.curdir)}/crumpled paper/'
            img = self._draw_watermark(img, 1, path, resize=True)

        if self.parameters_generate['blurCheckBox']:
            img = img.filter(ImageFilter.BLUR)

        if self.parameters_generate['noiseCheckBox']:
            img = img.filter(ImageFilter.MinFilter(3))

        return img

    def create_image(self, passport_data):
        with Image.open(f'{os.path.abspath(os.curdir)}/background/'
                        f'{self.parameters_generate["images"]["background"][0]}') as img:
            img = img.convert('RGBA')
            background_markup = {}
            font = ImageFont.truetype(f'{os.path.abspath(os.curdir)}/fonts/'
                                      f'{self.parameters_generate["fontComboBox"]}',
                                      self.parameters_generate["fontsizeSpinBox"])

            # background_markup = {elem['label']: list(map(lambda x: [int(x[0]), int(x[1])], elem['points']))
            #                     for elem in self.parameters_generate["images"]["background"][1]["shapes"]}

            for elem in self.parameters_generate["images"]["background"][1]["shapes"]:
                # Берем только первое вхождение, надо обсудить issue_place.
                if background_markup.get(elem['label'], None) is None:
                    background_markup.update(
                        {elem['label']: list(map(lambda x: [int(x[0]), int(x[1])], elem['points']))})

            # Что-то сделать со строчками

            img_text = self._draw_text(passport_data['department'], font,
                                       self._get_box_size(background_markup["issue_place"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["issue_place"]), img_text)

            font_numbers = ImageFont.truetype(f'{os.path.abspath(os.curdir)}'
                                              f'/fonts/a_SeriferNr_Bold.ttf',
                                              self.parameters_generate["fontsizeSpinBox"])
            img_text = self._draw_text(" ".join([str(passport_data['seriesPassport']),
                                                 str(passport_data['numberPassport'])]),
                                       font_numbers,
                                       self._get_box_size(background_markup["number_group1"], number=True),
                                       number=True)
            img_text = img_text.rotate(270)
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["number_group1"], number=True),
                      img_text)

            print(" ".join([str(passport_data['seriesPassport']), str(passport_data['numberPassport'])]),
                  background_markup["number_group2"],
                  self._get_box_size(background_markup["number_group2"]))
            img_text = self._draw_text(" ".join([str(passport_data['seriesPassport']),
                                                 str(passport_data['numberPassport'])]),
                                       font_numbers,
                                       self._get_box_size(background_markup["number_group2"], number=True),
                                       number=True)

            img_text = img_text.rotate(270)
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["number_group2"], number=True),
                      img_text)

            img_text = self._draw_text(passport_data['secondName'], font,
                                       self._get_box_size(background_markup["surname"]))
            img.paste(img_text.convert('RGBA'), self._get_place(background_markup["surname"]), img_text)

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

            # Foto
            with Image.open(self.parameters_generate['images']['labelFoto']) as img_photo:
                img_photo = img_photo.resize(self._get_box_size(background_markup["photo"], Image.NEAREST))
                img.paste(img_photo, self._get_place(background_markup["photo"]))


            with Image.open(self.parameters_generate['images']['label_signature_1']) as img_photo:
                img_photo = img_photo.resize(self._get_box_size(background_markup["signature"], Image.NEAREST))
                img.paste(img_photo.convert('RGBA'), self._get_place(background_markup["signature"]))

            """with Image.open(self.parameters_generate['images']['label_signature_2']) as img_photo:
                img_photo = img_photo.resize(self._get_box_size(background_markup["signature"], Image.NEAREST))
                img.paste(img_photo.convert('RGBA'), self._get_place(background_markup["signature"]))"""

            img = self._overlay_artifacts(img)

        return img
