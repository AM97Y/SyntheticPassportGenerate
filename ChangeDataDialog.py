import functools
import os
from typing import Union

from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog, QLabel
from PIL import Image

from utils.path_utils import Paths
from utils.qt_utils import add_pixmap_to_widget


class ChangeDataDialog(QDialog):
    def __init__(self, passport_content_params: dict, passport_appearance_params: dict):
        QDialog.__init__(self)
        uic.loadUi('ChangeDataDialog.ui', self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon('Icons/ChangeDataDialog.ico'))

        self._connect_signals_slots()

        self._fill_first_passport_page_fields(passport_content_params)
        self._fill_second_passport_page_fields(passport_content_params)
        self._fill_artifacts_fields(passport_appearance_params)
        self._fill_fonts_fields(passport_appearance_params)

        self._fill_label_by_img(image_path=passport_content_params['images']['photoLabel'],
                                label_obj=self.photoLabel)
        self._fill_label_by_img(image_path=passport_content_params['images']['officersignLabel'],
                                label_obj=self.officersignLabel)
        self._fill_label_by_img(image_path=passport_content_params['images']['ownersignLabel'],
                                label_obj=self.ownersignLabel)

        self._image_content_paths = {'photoLabel': passport_content_params['images']['photoLabel'],
                                     'officersignLabel': passport_content_params['images']['officersignLabel'],
                                     'ownersignLabel': passport_content_params['images']['ownersignLabel']}

        self.show()

    @property
    def images_content(self) -> dict:
        return self._image_content_paths

    def _connect_signals_slots(self):
        self.photoLabel.mousePressEvent = functools.partial(self._load_img, obj=self.photoLabel, name='photoLabel')
        self.officersignLabel.mousePressEvent = functools.partial(self._load_img, obj=self.officersignLabel,
                                                                  name='officersignLabel')
        self.ownersignLabel.mousePressEvent = functools.partial(self._load_img, obj=self.ownersignLabel,
                                                                name='ownersignLabel')

    def _fill_first_passport_page_fields(self, passport_content_params: dict) -> None:
        """
        Fill window fields which concerns data of the first passport page

        :param passport_content_params: passport content of the first passport page
        """
        self.serieSpinBox.setValue(passport_content_params['series_passport'])
        self.numberSpinBox.setValue(passport_content_params['number_passport'])
        self.organizationLineEdit.setText(passport_content_params['department'])
        self.issueDateEdit.setDate(passport_content_params['date_issue'])
        self.codeSpinBox1.setValue(passport_content_params['department_code'][0])
        self.codeSpinBox2.setValue(passport_content_params['department_code'][1])

    def _fill_second_passport_page_fields(self, passport_content_params: dict) -> None:
        """
        Fill window fields which concerns data of the second passport page

        :param passport_content_params: passport content of the second passport page
        """
        self.surnameLineEdit.setText(passport_content_params['second_name'])
        self.nameLineEdit.setText(passport_content_params['first_name'])
        self.patronymicLineEdit.setText(passport_content_params['patronymic_name'])
        self.sexComboBox.setCurrentText(passport_content_params['sex'])
        self.birthDateEdit.setDate(passport_content_params['date_birth'])
        self.birthPlacelineEdit.setText(passport_content_params['address'])

    def _fill_artifacts_fields(self, passport_appearance_params: dict) -> None:
        """
        Fill fields with parameters of artifacts applied to generated passport image

        :param passport_appearance_params: appearance parameters for generated passport image
        """
        self.crumpledCheckBox.setChecked(passport_appearance_params['crumpledCheckBox'])
        self.noiseCheckBox.setChecked(passport_appearance_params['noiseCheckBox'])
        self.blotsnumSpinBox.setValue(passport_appearance_params['blotsnumSpinBox'])
        self.flashnumSpinBox.setValue(passport_appearance_params['flashnumSpinBox'])
        self.blurFlashnumBlotsnum.setValue(passport_appearance_params['blurFlashnumBlotsnum'])

    def _fill_fonts_fields(self, passport_appearance_params: dict) -> None:
        """
        Fill fields with parameters of text font for generated passport image

        :param passport_appearance_params: font parameters for generated passport image
        """
        for file in os.listdir(Paths.fonts()):
            if file != 'fonts.txt':
                self.fontComboBox.addItem(file)
        self.fontComboBox.setCurrentText(passport_appearance_params['fontComboBox'].split('/')[-1])
        self.fontsizeSpinBox.setValue(passport_appearance_params['fontsizeSpinBox'])
        self.fontblurSpinBox.setValue(passport_appearance_params['fontblurSpinBox'])

    @staticmethod
    def _fill_label_by_img(image_path: Union[str, ImageQt], label_obj: QLabel) -> None:
        """
        Filling label qt object by image

        :param image_path: path to image to fill
        :param label_obj: label to fill by image.
        """
        q_image = ImageQt(Image.open(image_path))
        add_pixmap_to_widget(pixmap=QPixmap.fromImage(q_image), widget=label_obj)

    def _load_img(self, event, obj, name: str) -> None:
        """
        Load thumbnails of selected images

        :param event: mouse event clicking
        :param obj: object which was clicked in
        :param name: image name in imgs_dict
        """
        image_directory = str(Paths.photo()) if name == 'photoLabel' else str(Paths.signs())
        filters = 'Images (*.png *.xpm *.jpg *.bmp *.tiff)'

        image_path = QFileDialog.getOpenFileName(self, caption=f"{name} image",
                                                 directory=image_directory,
                                                 filter=filters)[0]
        if os.path.isfile(image_path):
            self._image_content_paths.update({name: image_path})
            add_pixmap_to_widget(pixmap=QPixmap(image_path), widget=obj)
        self.show()
