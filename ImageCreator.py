from PIL import Image, ImageFont

from utils.draw_utils import get_box_corner_to_draw, get_box_size_to_draw, get_text_image, \
    draw_image, draw_artifacts
from utils.path_utils import Paths
from utils.resources_utils import Resources


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
                'serie_number': ImageFont.truetype(font=Resources.numbers_font(),
                                                   size=self._passport_appearance_params["font_pick"] + 6)
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
            img_text = get_text_image(text=self._passport_content_params['date_issue'].strftime("%d.%m.%Y"),
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
            img_text = get_text_image(text=self._passport_content_params['date_birth'].strftime("%d.%m.%Y"),
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
                                      color=font_colors['red'], center=False).rotate(270)
            img.paste(im=img_text,
                      box=get_box_corner_to_draw(markup=background_markup["number_group1"], number=True),
                      mask=img_text, )
            img_text = get_text_image(text=series_number_text,
                                      font=fonts['serie_number'],
                                      size=get_box_size_to_draw(markup=background_markup["number_group2"], number=True),
                                      color=font_colors['red'], center=False).rotate(270)
            img.paste(im=img_text,
                      box=get_box_corner_to_draw(markup=background_markup["number_group2"], number=True),
                      mask=img_text)

            # Add images to passport background
            #  Add photo of owner
            img = draw_image(img=img, file_paste_img=self._passport_content_params['images']['photoLabel'],
                             background_markup=background_markup["photo"])

            # Add signature of officer
            img = draw_image(img=img, file_paste_img=self._passport_content_params['images']['officersignLabel'],
                             background_markup=background_markup["officer_signature"], delete_background=True)

            # Add signature of owner
            img = draw_image(img=img, file_paste_img=self._passport_content_params['images']['ownersignLabel'],
                             background_markup=background_markup["signature"], delete_background=True)

            # Add artifacts
            img = draw_artifacts(img=img, params=self._passport_appearance_params,
                                 markup_passport=self._passport_content_params["images"]["background"][1]['passport'])

        return img
