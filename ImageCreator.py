from PIL import Image, ImageFont

from utils.draw_utils import draw_text, draw_image, draw_artifacts
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
            img = draw_text(img=img, text=self._passport_content_params['department'],
                            background_markup=background_markup["issue_place"],
                            font=fonts['text'],
                            color=font_colors['black'])
            # Add issue date to passport background
            img = draw_text(img=img,
                            text=self._passport_content_params['date_issue'].strftime("%d.%m.%Y"),
                            background_markup=background_markup["issue_date"],
                            font=fonts['text'],
                            color=font_colors['black'])
            # Add department code to passport background
            img = draw_text(img=img, text="-".join(map(str, self._passport_content_params['department_code'])),
                            background_markup=background_markup["code"],
                            font=fonts['text'],
                            color=font_colors['black'])
            # Add info to the second passport page
            # Add surname to passport background
            img = draw_text(img=img, text=self._passport_content_params['second_name'],
                            background_markup=background_markup["surname"],
                            font=fonts['text'],
                            color=font_colors['black'])
            # Add name to passport background
            img = draw_text(img=img, text=self._passport_content_params['first_name'],
                            background_markup=background_markup["name"],
                            font=fonts['text'],
                            color=font_colors['black'])
            # Add patronymic to passport background
            img = draw_text(img=img, text=self._passport_content_params['patronymic_name'],
                            background_markup=background_markup["patronymic"],
                            font=fonts['text'],
                            color=font_colors['black'])
            # Add sex to passport background
            img = draw_text(img=img, text=self._passport_content_params['sex'],
                            background_markup=background_markup["sex"],
                            font=fonts['text'],
                            color=font_colors['black'])
            # Add birth date to passport background
            img = draw_text(img=img, text=self._passport_content_params['date_birth'].strftime("%d.%m.%Y"),
                            background_markup=background_markup["birth_date"],
                            font=fonts['text'],
                            color=font_colors['black'])
            # Add birth place to passport background
            img = draw_text(img=img, text=self._passport_content_params['address'],
                            background_markup=background_markup["birth_place"],
                            font=fonts['text'],
                            color=font_colors['black'])
            # Add series and number to passport background

            # Add series and number to passport background

            series_number_text = " ".join([str(self._passport_content_params['series_passport'])[:2],
                                           str(self._passport_content_params['series_passport'])[2:]])

            number_text = "  ".join([series_number_text,
                                     str(self._passport_content_params['number_passport'])])
            img = draw_text(img=img, text=number_text,
                            background_markup=background_markup["number_group1"],
                            font=fonts['serie_number'],
                            color=font_colors['red'], number=True)

            img = draw_text(img=img, text=number_text,
                            background_markup=background_markup["number_group2"],
                            font=fonts['serie_number'],
                            color=font_colors['red'], number=True)

            # Add images to passport background
            #  Add photo of owner
            img = draw_image(img=img, file_paste_img=self._passport_content_params['images']['photoLabel'],
                             background_markup=background_markup["photo"][0])

            # Add signature of officer
            img = draw_image(img=img, file_paste_img=self._passport_content_params['images']['officersignLabel'],
                             background_markup=background_markup["officer_signature"][0], delete_background=True)

            # Add signature of owner
            img = draw_image(img=img, file_paste_img=self._passport_content_params['images']['ownersignLabel'],
                             background_markup=background_markup["signature"][0], delete_background=True)

            # Add artifacts
            img = draw_artifacts(img=img, params=self._passport_appearance_params,
                                 markup_passport=self._passport_content_params["images"]["background"][1]['passport'][
                                     0])

        return img
