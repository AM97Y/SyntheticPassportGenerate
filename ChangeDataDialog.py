import functools
import os

from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog
from PIL import Image

from utils.path_utils import Paths


class ChangeDataDialog(QDialog):
    def __init__(self, passport_content, parameters_appearance):
        QDialog.__init__(self)
        uic.loadUi('ChangeDataDialog.ui', self)
        self.setFixedSize(self.width(), self.height())
        # self.setWindowIcon(QtGui.QIcon('Icons/results.ico'))

        self.label_photo.mousePressEvent = functools.partial(self._load_img, obj=self.label_photo, name='label_photo')
        self.label_signature_1.mousePressEvent = functools.partial(self._load_img, obj=self.label_signature_1,
                                                                   name='label_signature_1')
        self.label_signature_2.mousePressEvent = functools.partial(self._load_img, obj=self.label_signature_2,
                                                                   name='label_signature_2')

        self.imgs_dict = {'label_photo': passport_content['images']['label_photo'],
                          'label_signature_1': passport_content['images']['label_signature_1'],
                          'label_signature_2': passport_content['images']['label_signature_2'],
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

        self.organizationLineEdit1.setText(passport_content['department'])

        self.surnameLineEdit1.setText(passport_content['second_name'])
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

        self._fill_img(self.imgs_dict['label_photo'], self.label_photo)
        self._fill_img(self.imgs_dict['label_signature_1'], self.label_signature_1)
        self._fill_img(self.imgs_dict['label_signature_1'], self.label_signature_1)

        self.show()

    def _fill_img(self, image_path, obj):
        """
        Filling images.

        """
        print(image_path)
        qimage = ImageQt(Image.open(image_path))
        img = QPixmap.fromImage(qimage) \
            .scaledToWidth(obj.frameGeometry().width()) \
            .scaledToWidth(obj.frameGeometry().width())
        obj.setPixmap(img)

    def _load_img(self, event, obj, name: str) -> None:
        """
        This function loads thumbnails of the selected images.
        :param event: Event.
        :param obj: Event object.
        :param name: Name image in imgs_dict.
        """

        image_path = QFileDialog.getExistingDirectory(self, 'Search image', '')
        if os.path.isfile(image_path):
            self.imgs_dict.update({name: image_path})
            self.draw_img(image_path, obj)
            img = QPixmap(image_path) \
                .scaledToWidth(obj.frameGeometry().width()) \
                .scaledToWidth(obj.frameGeometry().height())
            obj.setPixmap(img)

        self.show()
