import functools
import os

from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog
from PIL import Image

from utils.path_utils import Paths
from utils.qt_utils import add_pixmap_to_widget


class ChangeDataDialog(QDialog):
    def __init__(self, passport_content, parameters_appearance):
        QDialog.__init__(self)
        uic.loadUi('ChangeDataDialog.ui', self)
        self.setFixedSize(self.width(), self.height())
        # self.setWindowIcon(QtGui.QIcon('Icons/results.ico'))

        self._connect_signals_slots()

        self.imgs_dict = {'photoLabel': passport_content['images']['photoLabel'],
                          'officersignLabel': passport_content['images']['officersignLabel'],
                          'ownersignLabel': passport_content['images']['ownersignLabel'],
                          'background': ['', {}]
                          }
        self._fill_fields(passport_content, parameters_appearance)

    def _fill_fields(self, passport_content: dict, parameters_appearance: dict) -> None:
        """
        Filling in the fields.

        """
        self.sexComboBox.setCurrentText(passport_content['sex'])

        for file in os.listdir(Paths.fonts()):
            if file != 'fonts.txt':
                self.fontComboBox.addItem(file)
        self.fontComboBox.setCurrentText(parameters_appearance['fontComboBox'])

        self.upperCheckBox.setChecked(parameters_appearance['upperCheckBox'])

        self.blurCheckBox.setChecked(parameters_appearance['blurCheckBox'])
        self.crumpledCheckBox.setChecked(parameters_appearance['crumpledCheckBox'])
        self.noiseCheckBox.setChecked(parameters_appearance['noiseCheckBox'])

        self.organizationLineEdit.setText(passport_content['department'])

        self.surnameLineEdit.setText(passport_content['second_name'])
        self.nameLineEdit.setText(passport_content['first_name'])
        self.patronymicLineEdit.setText(passport_content['patronymic_name'])

        self.serieSpinBox.setValue(passport_content['series_passport'])
        self.numberSpinBox.setValue(passport_content['number_passport'])

        self.issueDateEdit.setDate(passport_content['date_issue'])

        self.codeSpinBox1.setValue(passport_content['department_code'][0])
        self.codeSpinBox2.setValue(passport_content['department_code'][1])

        self.sexComboBox.setCurrentText(passport_content['sex'])

        self.birthDateEdit.setDate(passport_content['date_birth'])

        self.blotsnumSpinBox.setValue(parameters_appearance['blotsnumSpinBox'])
        self.flashnumSpinBox.setValue(parameters_appearance['flashnumSpinBox'])
        self.blurFlashnumBlotsnum.setValue(parameters_appearance['blurFlashnumBlotsnum'])

        # self.fontComboBox.setCurrentText(parameters_appearance['fontComboBox'])
        self.fontsizeSpinBox.setValue(parameters_appearance['fontsizeSpinBox'])
        self.fontblurSpinBox.setValue(parameters_appearance['fontblurSpinBox'])

        self._fill_img(self.imgs_dict['photoLabel'], self.photoLabel)
        self._fill_img(self.imgs_dict['officersignLabel'], self.officersignLabel)
        self._fill_img(self.imgs_dict['ownersignLabel'], self.ownersignLabel)

        self.show()

    @staticmethod
    def _fill_img(image_path, obj):
        """
        Filling images.

        """
        q_image = ImageQt(Image.open(image_path))
        add_pixmap_to_widget(QPixmap.fromImage(q_image), obj)

    def _load_img(self, event, obj, name: str) -> None:
        """
        This function loads thumbnails of the selected images.
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
            self.imgs_dict.update({name: image_path})
            add_pixmap_to_widget(QPixmap(image_path), obj)
        self.show()

    def _connect_signals_slots(self):
        self.photoLabel.mousePressEvent = functools.partial(self._load_img, obj=self.photoLabel, name='photoLabel')
        self.officersignLabel.mousePressEvent = functools.partial(self._load_img, obj=self.officersignLabel,
                                                                  name='officersignLabel')
        self.ownersignLabel.mousePressEvent = functools.partial(self._load_img, obj=self.ownersignLabel,
                                                                name='ownersignLabel')
