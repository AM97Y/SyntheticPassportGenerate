from math import floor
from random import randint, choice
from typing import Tuple, List

import albumentations as A
import numpy as np
import PIL
from PIL import Image, ImageOps, ImageFont, ImageDraw

from MessageBox import MessageBox
from utils.processing_utils import convert_from_image_to_cv2, convert_from_cv2_to_image, get_hyphenated_str
from utils.resources_utils import Resources


def get_box_size_to_draw(markup: List[list], number: bool = False) -> tuple:
    """
    Get box size to draw the text inside

    :param markup: background markup
    :param number: True if it is needed to draw a number
    :return: width and height of the box to draw inside
    """

    left_upper_point = markup[0]
    right_upper_point = markup[1]
    down_point = markup[3]
    if number:
        width = down_point[1] - left_upper_point[1]
        height = width
    else:
        width = right_upper_point[0] - left_upper_point[0]
        height = down_point[1] - left_upper_point[1]
    return width, height


def get_box_corner_to_draw(markup: List[list], number: bool = False) -> tuple:
    """
    Get the coordinate of left upper box corner to draw inside.

    :param markup: Background markup.
    :param number: True if it is needed to draw a number.
    :return: coordinate of left upper box corner.
    """
    if number:
        w, h = get_box_size_to_draw(markup=markup)
        return markup[0][0] - (h - w), markup[0][1]
    else:
        return markup[0][0], markup[0][1]


def delete_white_background(img: Image) -> Image:
    """
    Remove the white background on the image

    :param img: image to remove white background
    :return: changed image
    """
    img_signature_1 = img.convert('RGBA')
    arr = np.array(np.asarray(img_signature_1))
    r, g, b, _ = np.rollaxis(arr, axis=-1)
    mask = ((r > 150) & (g > 150) & (b > 150))
    arr[mask, 3] = 0
    img = Image.fromarray(arr, mode='RGBA')
    return img


def draw_text(img: Image, background_markup: List[List[list]], text: str, font: ImageFont, color: Tuple[int, int, int],
              number: bool = False) -> Image:
    """
    Draw image with text inside.

    :param number:
    :param img: Edited image.
    :param background_markup: Object markup.
    :param color: text color.
    :param text: text to draw inside
    :param font: text font.
    :return: generated text image.
    """

    prepositions = ("по", "в")
    text_lines = text.split("\n")

    for i, markup in enumerate(background_markup):
        if i >= len(text_lines):
            break

        size = get_box_size_to_draw(markup=markup, number=number)
        img_text = Image.new(mode="RGBA", size=size, color=(0, 0, 0, 0))
        drawer = ImageDraw.Draw(im=img_text)

        w_box, h_box = size
        w_text, h_text = drawer.textsize(text_lines[i], font=font)
        text = text.upper()

        if w_text > w_box:
            revers_words = text_lines[i].split(" ")[::-1]
            for j, word in enumerate(revers_words):
                if word in prepositions:
                    revers_words.insert(j + 1, '\n')
                    new_text_line_j = " ".join(revers_words[::-1]).split('\n')
                    text_lines[i] = new_text_line_j[0]
                    w_text, h_text = drawer.textsize(text_lines[i], font=font)
                    text_lines.insert(i+1, new_text_line_j[1])
                    break
            else:
                tmp_words = text_lines[i].split(' ')
                tmp_words.insert(-2, '\n')
                new_text_line_j = " ".join(tmp_words).split('\n')
                text_lines[i] = new_text_line_j[0]
                w_text, h_text = drawer.textsize(text_lines[i], font=font)
                text_lines.insert(i + 1, new_text_line_j[1])

        xy = ((w_box - w_text) / 2, 0)
        drawer.text(xy=xy, text=text_lines[i], fill=color, font=font)
        box = get_box_corner_to_draw(markup=markup, number=number)
        if number:
            img_text = img_text.rotate(270)
        img.paste(im=img_text, box=box, mask=img_text)

    return img


def draw_watermark(img: Image, count_watermark: int, files: List[str], params: dict = None) -> Image:
    """
    Draws watermarks with the specified transparency level on the image.

    :param params: paste_point - new watermark sizes; paste_point - if you set the coordinate, then what.
    :param files: List files watermarks.
    :param img: Edited Image.
    :param count_watermark: Number of watermarks.
    :return: Changed image.
    """
    (w, h) = img.size

    if count_watermark > 0:
        for i in range(0, count_watermark):
            with Image.open(choice(files)) as img_watermark:
                img_watermark = img_watermark.convert('RGBA')
                paste_point = params['paste_point'] if params['paste_point'] else (randint(0, w), randint(0, h))
                if params['resize_size'] is not None:
                    img_watermark = img_watermark.resize(size=params['resize_size'], resample=Image.NEAREST)
                paste_mask = img_watermark.split()[3].point(lambda i: i * 20 / 100.)
                img.paste(im=img_watermark, box=paste_point, mask=paste_mask)

    return img.convert('RGBA')


def draw_image(img: Image, file_paste_img: str, background_markup: List[List[list]], delete_background: bool = False) -> Image:
    """
    This function draws the image on the background.

    :param img: Edited Image.
    :param file_paste_img: Path to inserted image.
    :param background_markup: Edited Image markup.
    :param delete_background: True for deleted/
    :return: Changed image.
    """
    try:
        with Image.open(file_paste_img) as paste_img:

            paste_img = paste_img.resize(
                get_box_size_to_draw(markup=background_markup), Image.NEAREST)
            paste_point = get_box_corner_to_draw(markup=background_markup)
            if delete_background:
                paste_img = delete_white_background(paste_img)
                img.paste(im=paste_img, box=paste_point, mask=paste_img)
            else:
                img.paste(im=paste_img, box=paste_point)
            return img

    except PIL.UnidentifiedImageError:
        error_dialog = MessageBox()
        error_dialog.show_message('Выбранный объект не является изображением. Выберите другое изображение.')
        return img


def draw_artifacts(img: Image, params: dict, markup_passport: list) -> Image:
    """
    This function draws watermarks.

    :param params: Information about artifacts.
    :param markup_passport: Markup passport.
    :param img: image to overlay artifacts.
    :return: Changed image.
    """

    # Overlay blots
    count_watermark = params['blotsnumSpinBox']
    files = Resources.dirty()
    img = draw_watermark(img=img, count_watermark=count_watermark,
                         files=files,
                         params={"paste_point": None,
                                 "resize_size": None,
                                 })
    # Apply effect of "crumpled paper"
    if params['crumpledCheckBox']:
        files = Resources.crumpled()
        img = draw_watermark(img=img, count_watermark=1, files=files,
                             params={"paste_point": get_box_corner_to_draw(markup_passport),
                                     "resize_size": get_box_size_to_draw(markup_passport),
                                     })
        img = ImageOps.autocontrast(image=img.convert('RGB'), cutoff=2, ignore=2)

    effects = [A.RGBShift(r_shift_limit=10, g_shift_limit=10, b_shift_limit=10, p=0.5),
               A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.15),
               ]
    # Apply blur
    if params['blurCheckBox']:
        effects.append(A.OneOf([A.GaussianBlur(p=1), A.MedianBlur(p=1), A.Blur(p=1)], p=1))

    # Apply noise
    if params['noiseCheckBox']:
        # img = img.filter(ImageFilter.MinFilter(size=3))
        effects.append(A.GaussNoise(p=1))

    # Overlay flashes
    if params['flashnumSpinBox'] > 0:
        effects += [A.RandomSunFlare(num_flare_circles_lower=0, num_flare_circles_upper=1,
                                     src_radius=floor(6.25 * params['font_pick']), p=1)] \
                   * params['flashnumSpinBox']

    image_cv = convert_from_image_to_cv2(img=img)
    transform = A.Compose(effects)
    image_cv = transform(image=image_cv)["image"]
    img = convert_from_cv2_to_image(img=image_cv)

    return img
