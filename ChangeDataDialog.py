import functools
import os
from typing import Union

from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog
from PIL import Image

from utils.path_utils import Paths
from utils.qt_utils import add_pixmap_to_widget


class ChangeDataDialog(QDialog):
    def __init__(self, passport_content_params: dict, passport_appearance_params: dict):
        QDialog.__init__(self)
        uic.loadUi('ChangeDataDialog.ui', self)
        self.setFixedSize(self.width(), self.height())
        # self.setWindowIcon(QtGui.QIcon('Icons/results.ico'))

        self._connect_signals_slots()

        self.imgs_dict = {'photoLabel': passport_content_params['images']['photoLabel'],
                          'officersignLabel': passport_content_params['images']['officersignLabel'],
                          'ownersignLabel': passport_content_params['images']['ownersignLabel'],
                          'background': ['', {}]
                          }

        self._fill_first_passport_page_fields(passport_content_params)
        self._fill_second_passport_page_fields(passport_content_params)
        self._fill_artifacts_fields(passport_appearance_params)
        self._fill_fonts_fields(passport_appearance_params)

        self._fill_img(passport_content_params['images']['photoLabel'], self.photoLabel)
        self._fill_img(passport_content_params['images']['officersignLabel'], self.officersignLabel)
        self._fill_img(passport_content_params['images']['ownersignLabel'], self.ownersignLabel)

        self._image_content_paths = [passport_content_params['images']['photoLabel'],
                                     passport_content_params['images']['officersignLabel'],
                                     passport_content_params['images']['ownersignLabel']]

    def _connect_signals_slots(self):
        self.photoLabel.mousePressEvent = functools.partial(self._load_img, obj=self.photoLabel, name='photoLabel')
        self.officersignLabel.mousePressEvent = functools.partial(self._load_img, obj=self.officersignLabel,
                                                                  name='officersignLabel')
        self.ownersignLabel.mousePressEvent = functools.partial(self._load_img, obj=self.ownersignLabel,
                                                                name='ownersignLabel')

    def _fill_first_passport_page_fields(self, passport_content_params: dict) -> None:
        """
        Fill window fields which concerns data of the first passport page

        :param passport_content_params:
        """

        # First passport page
        self.serieSpinBox.setValue(passport_content_params['series_passport'])
        self.numberSpinBox.setValue(passport_content_params['number_passport'])
        self.organizationLineEdit.setText(passport_content_params['department'])
        self.issueDateEdit.setDate(passport_content_params['date_issue'])
        self.codeSpinBox1.setValue(passport_content_params['department_code'][0])
        self.codeSpinBox2.setValue(passport_content_params['department_code'][1])

    def _fill_second_passport_page_fields(self, passport_content_params: dict) -> None:
        """
        Fill window fields which concerns data of the second passport page

        :param passport_content_params:
        """
        self.surnameLineEdit.setText(passport_content_params['second_name'])
        self.nameLineEdit.setText(passport_content_params['first_name'])
        self.patronymicLineEdit.setText(passport_content_params['patronymic_name'])
        self.sexComboBox.setCurrentText(passport_content_params['sex'])
        self.birthDateEdit.setDate(passport_content_params['date_birth'])

    def _fill_artifacts_fields(self, passport_appearance_params: dict) -> None:
        """
        Fill fields of GroupBox with artifacts data

        :param passport_appearance_params:
        """

        self.blurCheckBox.setChecked(passport_appearance_params['blurCheckBox'])
        self.crumpledCheckBox.setChecked(passport_appearance_params['crumpledCheckBox'])
        self.noiseCheckBox.setChecked(passport_appearance_params['noiseCheckBox'])
        self.blotsnumSpinBox.setValue(passport_appearance_params['blotsnumSpinBox'])
        self.flashnumSpinBox.setValue(passport_appearance_params['flashnumSpinBox'])
        self.blurFlashnumBlotsnum.setValue(passport_appearance_params['blurFlashnumBlotsnum'])

    def _fill_artifacts_fields(self, passport_appearance_params: dict) -> None:
        """
        Fill fields of GroupBox with artifacts data

        :param passport_appearance_params:
        """
        self.blurCheckBox.setChecked(passport_appearance_params['blurCheckBox'])
        self.crumpledCheckBox.setChecked(passport_appearance_params['crumpledCheckBox'])
        self.noiseCheckBox.setChecked(passport_appearance_params['noiseCheckBox'])
        self.blotsnumSpinBox.setValue(passport_appearance_params['blotsnumSpinBox'])
        self.flashnumSpinBox.setValue(passport_appearance_params['flashnumSpinBox'])
        self.blurFlashnumBlotsnum.setValue(passport_appearance_params['blurFlashnumBlotsnum'])

    def _fill_fonts_fields(self, passport_appearance_params: dict) -> None:
        """
        Fill fields of GroupBox with fonts data

        :param passport_appearance_params:
        """
        for file in os.listdir(Paths.fonts()):
            if file != 'fonts.txt':
                self.fontComboBox.addItem(file)
        self.fontComboBox.setCurrentText(passport_appearance_params['fontComboBox'])
        self.fontsizeSpinBox.setValue(passport_appearance_params['fontsizeSpinBox'])
        self.fontblurSpinBox.setValue(passport_appearance_params['fontblurSpinBox'])

    def _fill_img(self, image_path: Union[str, ImageQt], obj):
        """
        Filling images.

        :param image_path:
        :param obj:
        :return:
        """
        q_image = ImageQt(Image.open(image_path))
        add_pixmap_to_widget(QPixmap.fromImage(q_image), obj)

    @property
    def images_content(self) -> dict:
        return dict(zip(['photoLabel', 'officersignLabel', 'ownersignLabel', 'background'],
                        self._image_content_paths + [['', {}]]))

    def _load_img(self, event, obj, name: str) -> None:
        """
        Load thumbnails of selected images.

        :param event: Event clicking: QMouseEvent.
        :param obj: Object by clicking on which there was a disposal.
        :param name: Name image in imgs_dict.
        """
        if name == 'photoLabel':
            dir = str(Paths.photo())
        else:
            dir = str(Paths.signs())
        filters = 'Images (*.png *.xpm *.jpg)'

        image_path = QFileDialog.getOpenFileName(self, f"{name} image", directory=dir,
                                                 filter=filters)[0]
        if os.path.isfile(image_path):
            self._images_content.update({name: image_path})
            add_pixmap_to_widget(QPixmap(image_path), obj)
        self.show()
