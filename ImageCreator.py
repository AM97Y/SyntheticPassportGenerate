import albumentations as A
import PIL
from PIL import Image, ImageFilter, ImageOps, ImageFont

from MessageBox import MessageBox
from utils.draw_utils import get_box_corner_to_draw, get_box_size_to_draw, delete_white_background, get_text_image, \
    draw_watermark
from utils.path_utils import Paths, Resources
from utils.processing_utils import convert_from_image_to_cv2, convert_from_cv2_to_image


class ImageCreator:
    """
    This class create passport image
    """
    def __init__(self, passport_content_params: dict, passport_appearance_params: dict):
        self._passport_content_params = passport_content_params
        self._passport_appearance_params = passport_appearance_params

    def create_image(self) -> Image:
        """
        This function generates passport image

        :return: created passport image
        """
        with Image.open(Paths.backgrounds() / self._passport_content_params["images"]["background"][0]) as img:
            img = img.convert('RGBA')
            background_markup = self._passport_content_params["images"]["background"][1]

            fonts = {
                'text': ImageFont.truetype(font=str(Paths.fonts() / self._passport_appearance_params["fontComboBox"]),
                                           size=self._passport_appearance_params["fontsizeSpinBox"]),
                'serie_number': ImageFont.truetype(Resources.numbers_font(), 46)
            }
            font_colors = {'black': (self._passport_appearance_params['color_text'],) * 3, 'red': (130, 30, 30)}

            # Add info to the first passport page
            # Add organization issued the passport to passport background
            img_text = get_text_image(text=self._passport_content_params['department'].upper(),
                                      font=fonts['text'],
                                      size=get_box_size_to_draw(markup=background_markup["issue_place"]),
                                      color=font_colors['black'])
            img.paste(im=img_text, box=get_box_corner_to_draw(markup=background_markup["issue_place"]), mask=img_text)
            # Add issue date to passport background
            img_text = get_text_image(text=self._passport_content_params['date_issue'].strftime("%m.%d.%Y"),
                                      font=fonts['text'],
                                      size=get_box_size_to_draw(markup=background_markup["issue_date"]),
                                      color=font_colors['black'])
            img.paste(im=img_text, box=get_box_corner_to_draw(markup=background_markup["issue_date"]), mask=img_text)
            # Add department code to passport background
            img_text = get_text_image(text="-".join(map(str, self._passport_content_params['department_code'])),
                                      font=fonts['text'],
                                      size=get_box_size_to_draw(markup=background_markup["code"]),
                                      color=font_colors['black'])
            img.paste(im=img_text, box=get_box_corner_to_draw(markup=background_markup["code"]), mask=img_text)

            # Add info to the second passport page
            # Add surname to passport background
            img_text = get_text_image(text=self._passport_content_params['second_name'].upper(),
                                      font=fonts['text'],
                                      size=get_box_size_to_draw(markup=background_markup["surname"]),
                                      color=font_colors['black'])
            img.paste(im=img_text, box=get_box_corner_to_draw(markup=background_markup["surname"]), mask=img_text)
            # Add name to passport background
            img_text = get_text_image(text=self._passport_content_params['first_name'].upper(),
                                      font=fonts['text'],
                                      size=get_box_size_to_draw(markup=background_markup["name"]),
                                      color=font_colors['black'])
            img.paste(im=img_text, box=get_box_corner_to_draw(markup=background_markup["name"]), mask=img_text)
            # Add patronymic to passport background
            img_text = get_text_image(text=self._passport_content_params['patronymic_name'].upper(),
                                      font=fonts['text'],
                                      size=get_box_size_to_draw(markup=background_markup["patronymic"]),
                                      color=font_colors['black'])
            img.paste(im=img_text, box=get_box_corner_to_draw(markup=background_markup["patronymic"]), mask=img_text)
            # Add sex to passport background
            img_text = get_text_image(text=self._passport_content_params['sex'],
                                      font=fonts['text'],
                                      size=get_box_size_to_draw(markup=background_markup["sex"]),
                                      color=font_colors['black'])
            img.paste(im=img_text, box=get_box_corner_to_draw(markup=background_markup["sex"]), mask=img_text)
            # Add birth date to passport background
            img_text = get_text_image(text=self._passport_content_params['date_birth'].strftime("%m.%d.%Y"),
                                      font=fonts['text'],
                                      size=get_box_size_to_draw(markup=background_markup["birth_date"]),
                                      color=font_colors['black'])
            img.paste(im=img_text, box=get_box_corner_to_draw(markup=background_markup["birth_date"]), mask=img_text)
            # Add birth place to passport background
            img_text = get_text_image(text=self._passport_content_params['address'].upper(),
                                      font=fonts['text'],
                                      size=get_box_size_to_draw(markup=background_markup["birth_place"]),
                                      color=font_colors['black'])
            img.paste(im=img_text, box=get_box_corner_to_draw(markup=background_markup["birth_place"]), mask=img_text)

            # Add series and number to passport background
            series_number_text = " ".join([str(self._passport_content_params['series_passport']),
                                           str(self._passport_content_params['number_passport'])])
            img_text = get_text_image(text=series_number_text,
                                      font=fonts['serie_number'],
                                      size=get_box_size_to_draw(markup=background_markup["number_group1"], number=True),
                                      color=font_colors['red']).rotate(270)
            img.paste(im=img_text,
                      box=get_box_corner_to_draw(markup=background_markup["number_group1"], number=True),
                      mask=img_text)
            img_text = get_text_image(text=series_number_text,
                                      font=fonts['serie_number'],
                                      size=get_box_size_to_draw(markup=background_markup["number_group2"], number=True),
                                      color=font_colors['red']).rotate(270)
            img.paste(im=img_text,
                      box=get_box_corner_to_draw(markup=background_markup["number_group2"], number=True),
                      mask=img_text)

            # Add images to passport background
            #  Add photo of owner
            try:
                with Image.open(self._passport_content_params['images']['photoLabel']) as img_photo:
                    img_photo = img_photo.resize(get_box_size_to_draw(markup=background_markup["photo"]), Image.NEAREST)
                    img.paste(im=img_photo, box=get_box_corner_to_draw(background_markup["photo"]))
            except PIL.UnidentifiedImageError:
                error_dialog = MessageBox()
                error_dialog.show_message('Фотогорафия человека не является изображением')
            # Add signature of officer
            try:
                with Image.open(self._passport_content_params['images']['officersignLabel']) as img_signature_1:
                    img_signature_1 = delete_white_background(img_signature_1).resize(
                        get_box_size_to_draw(markup=background_markup["signature"]), Image.NEAREST)

                    paste_point = get_box_corner_to_draw(markup=background_markup["signature"])
                    img.paste(im=img_signature_1, box=paste_point, mask=img_signature_1)
            except PIL.UnidentifiedImageError:
                error_dialog = MessageBox()
                error_dialog.show_message('Выбранная подпись не является изображением.')
            # Add signature of owner
            """with Image.open(self._passport_content_params['images']['ownersignLabel']) as img_signature_2:
                img_signature_2 = img_signature_2.resize(get_box_size_to_draw(background_markup["signature"], Image.NEAREST))
                img.paste(img_signature_2, get_box_corner_to_draw(background_markup["signature"]))"""

            img = self._overlay_artifacts(img)

        return img

    def _overlay_artifacts(self, img: Image) -> Image:
        """
        This function draws watermarks

        :param img: image to overlay artifacts
        :return: changed image
        """
        # Overlay blots
        count_watermark = self._passport_appearance_params['blotsnumSpinBox']
        files = Resources.dirty()
        img = draw_watermark(img=img, count_watermark=count_watermark,
                             files=files,
                             blur=self._passport_appearance_params['blurFlashnumBlotsnum'],
                             params={"paste_point": None,
                                     "resize_size": None,
                                     })
        # Apply effect of "crumpled paper"
        if self._passport_appearance_params['crumpledCheckBox']:
            files = Resources.crumpled()
            markup = self._passport_content_params["images"]["background"][1]['passport']
            img = draw_watermark(img=img, count_watermark=1, files=files,
                                 blur=self._passport_appearance_params['blurFlashnumBlotsnum'],
                                 params={"paste_point": get_box_corner_to_draw(markup),
                                         "resize_size": get_box_size_to_draw(markup),
                                         })
            img = ImageOps.autocontrast(image=img.convert('RGB'), cutoff=2, ignore=2)
        # Apply blur
        if self._passport_appearance_params['blurCheckBox']:
            img = img.filter(ImageFilter.BLUR)
        # Apply noise
        if self._passport_appearance_params['noiseCheckBox']:
            img = img.filter(ImageFilter.MinFilter(size=3))
        # Overlay flashes
        if self._passport_appearance_params['flashnumSpinBox'] > 0:
            count_watermark = self._passport_appearance_params['flashnumSpinBox']
            image_cv = convert_from_image_to_cv2(img=img)
            for _ in range(count_watermark):
                transform = A.Compose([A.RandomSunFlare(num_flare_circles_lower=0,
                                                        num_flare_circles_upper=1,
                                                        src_radius=400,
                                                        p=1)])
                image_cv = transform(image=image_cv)["image"]
            img = convert_from_cv2_to_image(img=image_cv)

        return img
