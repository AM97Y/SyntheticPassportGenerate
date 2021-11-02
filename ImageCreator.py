import os
from copy import deepcopy
from random import choice, randint

import PIL
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from PIL import ImageDraw
from PIL import ImageFont

from utils.path_utils import Paths
from utils.draw_utils import get_box_corner_to_draw, get_box_size_to_draw
from MessageBox import MessageBox


class ImageCreator:
    def __init__(self, parameters_passport, parameters_appearance):
        self.parameters_passport = parameters_passport
        self.parameters_appearance = parameters_appearance

    def _draw_text(self, text: str, font, shape, number=False):
        """
        This function draws text in background.
        :param text: Drawing text.
        :param font: Read font.
        :param shape: Shape of text box.
        :param number: Is it a number or not.
        :return: Changed image.
        """
        # text = get_hyphenated_str(text, font, shape[0])
        if self.parameters_appearance['upperCheckBox']:
            text = text.upper()

        img_text = Image.new("RGBA", shape, (0, 0, 0, 0))
        drawer = ImageDraw.Draw(img_text)
        if number:
            color = (130, 30, 30)
        else:
            color = (self.parameters_appearance['color_text'], self.parameters_appearance['color_text'],
                     self.parameters_appearance['color_text'])
        drawer.text((0, 0), text, fill=color, font=font)

        return img_text

    def _draw_watermark(self, img, count_watermark: int, path, random_point=False, paste_point=(0, 0),
                        resize_size=None):
        """
        This function draws watermarks with the specified transparency.
        :param img: Image.
        :param count_watermark: Number of watermarks.
        :param path: The folder where watermarks.
        :param random_point: Set the coordinate of the location or choose randomly.
        :param paste_point: If you set the coordinate, then what.
        :param resize_size: New watermark sizes.
        :return: Changed image..
        """
        (w, h) = img.size
        if count_watermark > 0:
            path_blots = os.listdir(path)
            for i in range(0, count_watermark):
                with Image.open(f'{path}/{choice([x for x in path_blots])}') as img_watermark:
                    img_watermark = img_watermark.convert('RGBA')
                    if random_point:
                        paste_point = (randint(0, w), randint(0, h))

                    if resize_size is not None:
                        img_watermark = img_watermark.resize(resize_size, Image.NEAREST)

                    paste_mask = img_watermark.split()[3].point(
                        lambda i: i * self.parameters_appearance['blurFlashnumBlotsnum'] / 100.)

                    img.paste(img_watermark, paste_point, mask=paste_mask)
        return img.convert('RGBA')

    def _overlay_artifacts(self, img):
        """
        This function calls draw of watermarks.
        :param img: Image.
        :return: Changed image.
        """

        count_watermark = self.parameters_appearance['blotsnumSpinBox']
        path = Paths.dirty()
        img = self._draw_watermark(img, count_watermark, path)

        count_watermark = self.parameters_appearance['flashnumSpinBox']
        path = Paths.glares()
        img = self._draw_watermark(img, count_watermark, path)

        if self.parameters_appearance['crumpledCheckBox']:
            path = Paths.crumpled()
            markup = self.parameters_passport["images"]["background"][1]['passport']
            img = self._draw_watermark(img, 1, path, paste_point=get_box_corner_to_draw(markup),
                                       resize_size=get_box_size_to_draw(markup))
            img = ImageOps.autocontrast(img.convert('RGB'), cutoff=2, ignore=2)

        if self.parameters_appearance['blurCheckBox']:
            img = img.filter(ImageFilter.BLUR)

        if self.parameters_appearance['noiseCheckBox']:
            img = img.filter(ImageFilter.MinFilter(3))

        return img

    @staticmethod
    def _delete_white_background(img):
        """
        This function removes the white background on signs.
        :param img: Image.
        :return: Changed image.
        """
        img_signature_1 = img.convert('RGBA')
        arr = np.array(np.asarray(img_signature_1))
        r, g, b, a = np.rollaxis(arr, axis=-1)
        mask = ((r == 255) & (g == 255) & (b == 255))
        arr[mask, 3] = 0
        img = Image.fromarray(arr, mode='RGBA')
        return img

    def create_image(self):
        """
        This function generates a passport image.
        :return: Image passport.
        """
        with Image.open(Paths.backgrounds() / self.parameters_passport["images"]["background"][0]) as img:
            img = img.convert('RGBA')
            background_markup = self.parameters_passport["images"]["background"][1]
            font = ImageFont.truetype(str(Paths.fonts() / self.parameters_appearance["fontComboBox"]),
                                      self.parameters_appearance["fontsizeSpinBox"])

            img_text = self._draw_text(self.parameters_passport['department'], font,
                                       get_box_size_to_draw(background_markup["issue_place"]))
            img.paste(img_text.convert('RGBA'), get_box_corner_to_draw(background_markup["issue_place"]), img_text)

            font_numbers = ImageFont.truetype(Paths.numbers_font(), 30)
            img_text = self._draw_text(" ".join([str(self.parameters_passport['series_passport']),
                                                 str(self.parameters_passport['number_passport'])]),
                                       font_numbers,
                                       get_box_size_to_draw(background_markup["number_group1"], number=True),
                                       number=True)
            img_text = img_text.rotate(270)
            img.paste(img_text.convert('RGBA'),
                      get_box_corner_to_draw(background_markup["number_group1"], number=True),
                      img_text)

            img_text = self._draw_text(" ".join([str(self.parameters_passport['series_passport']),
                                                 str(self.parameters_passport['number_passport'])]),
                                       font_numbers,
                                       get_box_size_to_draw(background_markup["number_group2"], number=True),
                                       number=True)

            img_text = img_text.rotate(270)
            img.paste(img_text.convert('RGBA'),
                      get_box_corner_to_draw(background_markup["number_group2"], number=True),
                      img_text)

            img_text = self._draw_text(self.parameters_passport['second_name'], font,
                                       get_box_size_to_draw(background_markup["surname"]))
            img.paste(img_text.convert('RGBA'), get_box_corner_to_draw(background_markup["surname"]), img_text)

            img_text = self._draw_text(self.parameters_passport['first_name'], font,
                                       get_box_size_to_draw(background_markup["name"]))
            img.paste(img_text.convert('RGBA'), get_box_corner_to_draw(background_markup["name"]), img_text)

            img_text = self._draw_text(self.parameters_passport['patronymic_name'], font,
                                       get_box_size_to_draw(background_markup["patronymic"]))
            img.paste(img_text.convert('RGBA'), get_box_corner_to_draw(background_markup["patronymic"]), img_text)

            img_text = self._draw_text(self.parameters_passport['address'], font,
                                       get_box_size_to_draw(background_markup["birth_place"]))
            img.paste(img_text.convert('RGBA'), get_box_corner_to_draw(background_markup["birth_place"]), img_text)

            img_text = self._draw_text("-".join(map(str, self.parameters_passport['department_code'])), font,
                                       get_box_size_to_draw(background_markup["code"]))
            img.paste(img_text.convert('RGBA'), get_box_corner_to_draw(background_markup["code"]), img_text)

            img_text = self._draw_text(self.parameters_passport['date_birth'].strftime("%m.%d.%Y"), font,
                                       get_box_size_to_draw(background_markup["birth_date"]))
            img.paste(img_text.convert('RGBA'), get_box_corner_to_draw(background_markup["birth_date"]), img_text)

            img_text = self._draw_text(self.parameters_passport['date_issue'].strftime("%m.%d.%Y"), font,
                                       get_box_size_to_draw(background_markup["issue_date"]))
            img.paste(img_text.convert('RGBA'), get_box_corner_to_draw(background_markup["issue_date"]), img_text)

            img_text = self._draw_text(self.parameters_passport['sex'], font,
                                       get_box_size_to_draw(background_markup["sex"]))
            img.paste(img_text.convert('RGBA'), get_box_corner_to_draw(background_markup["sex"]), img_text)

            # photo
            try:
                with Image.open(self.parameters_passport['images']['label_photo']) as img_photo:
                    img_photo = img_photo.resize(get_box_size_to_draw(background_markup["photo"], Image.NEAREST))
                    img.paste(img_photo, get_box_corner_to_draw(background_markup["photo"]))
            except PIL.UnidentifiedImageError:
                error_dialog = MessageBox()
                error_dialog.showMessage('Фотогорафия не человека не является изображением')
            try:
                with Image.open(self.parameters_passport['images']['label_signature_1']) as img_signature_1:
                    img_signature_1 = self._delete_white_background(img_signature_1)
                    img_signature_1 = img_signature_1.resize(
                        get_box_size_to_draw(background_markup["signature"], Image.NEAREST))

                    paste_point = get_box_corner_to_draw(background_markup["signature"])
                    img.paste(img_signature_1, paste_point, mask=img_signature_1)
            except PIL.UnidentifiedImageError:
                error_dialog = MessageBox()
                error_dialog.showMessage('Выбранная подпись не является изображением')

            """with Image.open(self.parameters_passport['images']['label_signature_2']) as img_signature_2:
                img_signature_2 = img_signature_2.resize(get_box_size_to_draw(background_markup["signature"], Image.NEAREST))
                img.paste(img_signature_2.convert('RGBA'), get_box_corner_to_draw(background_markup["signature"]))"""

            img = self._overlay_artifacts(img)

        return img
