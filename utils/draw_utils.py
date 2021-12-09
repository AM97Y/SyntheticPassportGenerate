from math import floor
from random import randint, choice
from typing import Tuple

import albumentations as A
import numpy as np
import PIL
from PIL import Image, ImageOps, ImageFont, ImageDraw

from MessageBox import MessageBox
from utils.processing_utils import convert_from_image_to_cv2, convert_from_cv2_to_image
from utils.resources_utils import Resources


def get_box_size_to_draw(markup: list, number: bool = False) -> tuple:
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


def get_box_corner_to_draw(markup: list, number: bool = False) -> tuple:
    """
    Get the coordinate of left upper box corner to draw inside

    :param markup: background markup
    :param number: True if it is needed to draw a number
    :return: coordinate of left upper box corner
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


def get_text_image(text: str, font: ImageFont, size: Tuple[int], color: Tuple[int, int, int],
                   center: bool = True) -> Image:
    """
    Get image with text inside

    :param center: place in the middle or not.
    :param size: image size
    :param color: text color
    :param text: text to draw inside
    :param font: text font
    :return: generated text image
        """
    # text = get_hyphenated_str(text, font, shape[0])
    text = text.upper()
    img_text = Image.new(mode="RGBA", size=size, color=(0, 0, 0, 0))
    drawer = ImageDraw.Draw(im=img_text)
    if center:
        W, H = size
        w, h = drawer.textsize(text, font=font)
        xy = ((W - w) / 2, (H - h) / 2)
    else:
        xy = (0, 0)

    drawer.text(xy=xy, text=text, fill=color, font=font)
    return img_text


def draw_watermark(img: Image, count_watermark: int, files: list, params: dict = None) -> Image:
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


def draw_image(img: Image, file_paste_img: str, background_markup, delete_background: bool = False) -> Image:
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
