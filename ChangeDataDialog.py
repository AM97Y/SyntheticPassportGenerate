import functools
import os

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *


class ChangeDataDialog(QDialog):
    def __init__(self, passport_data, parameters_generate):
        QDialog.__init__(self)
        uic.loadUi('ChangeDataDialog.ui', self)

        # self.setWindowIcon(QtGui.QIcon('Icons/results.ico'))
        # self.buttonBox.accepted.connect(self.ok)
        # self.buttonBox.rejected.connect(self.cancel)
        # https://coderoad.ru/44193227/%D0%9A%D0%B0%D0%BA-%D1%8F-%D0%BC%D0%BE%D0%B3%D1%83-%D1%80%D0%B8%D1%81%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B8-%D1%81%D1%83%D1%89%D0%B5%D1%81%D1%82%D0%B2%D1%83%D1%8E%D1%89%D0%B5%D0%B3%D0%BE-QGraphicsVIew
        self.labelFoto.mousePressEvent = functools.partial(self._load_img, obj=self.labelFoto, name='labelFoto')
        self.label_signature_1.mousePressEvent = functools.partial(self._load_img, obj=self.label_signature_1,
                                                                   name='label_signature_1')
        self.label_signature_2.mousePressEvent = functools.partial(self._load_img, obj=self.label_signature_2,
                                                                   name='label_signature_2')

        self.imgs_dict = {'labelFoto': parameters_generate['images']['labelFoto'],
                          'label_signature_1': parameters_generate['images']['label_signature_1'],
                          'label_signature_2': parameters_generate['images']['label_signature_2'],
                          'background': ['', {}]
                          }
        self._fill_fields(passport_data, parameters_generate)

    def _fill_fields(self, passport_data, parameters_generate):
        self.sexComboBox.addItem("ЖЕН.")
        self.sexComboBox.addItem("МУЖ.")
        self.sexComboBox.setCurrentText(passport_data['sex'])
        print(passport_data['sex'])

        print(parameters_generate['fontComboBox'])
        for file in os.listdir(f'{os.path.abspath(os.curdir)}/fonts/'):
            if file != 'fonts.txt':
                self.fontComboBox.addItem(file)
        self.fontComboBox.setCurrentText(parameters_generate['fontComboBox'])

        self.blurCheckBox.setChecked(parameters_generate['blurCheckBox'])
        self.crumpledCheckBox.setChecked(parameters_generate['crumpledCheckBox'])
        self.noiseCheckBox.setChecked(parameters_generate['noiseCheckBox'])

        self.organizationLineEdit1.setText(passport_data['department'])

        self.surnameLineEdit1.setText(passport_data['secondName'])
        self.nameLineEdit.setText(passport_data['firstName'])
        self.patronymicLineEdit.setText(passport_data['patronymicName'])

        self.birthplaceLineEdit1.setText(passport_data['city'])

        self.serieSpinBox.setValue(passport_data['seriesPassport'])
        self.numberSpinBox.setValue(passport_data['numberPassport'])

        self.issueDateEdit.setDate(passport_data['dateOFissue'])

        self.codeSpinBox1.setValue(passport_data['departmentCode'][0])
        self.codeSpinBox2.setValue(passport_data['departmentCode'][1])

        self.sexComboBox.setCurrentText(passport_data['sex'])

        self.birthDateEdit.setDate(passport_data['dateOFbirth'])

        self.blotsnumSpinBox.setValue(parameters_generate['blotsnumSpinBox'])
        self.flashnumSpinBox.setValue(parameters_generate['flashnumSpinBox'])
        self.blurFlashnumBlotsnum.setValue(parameters_generate['blurFlashnumBlotsnum'])

        # self.fontComboBox.setCurrentText(parameters_generate['fontComboBox'])
        self.fontsizeSpinBox.setValue(parameters_generate['fontsizeSpinBox'])
        self.fontblurSpinBox.setValue(parameters_generate['fontblurSpinBox'])

    def _load_img(self, event, obj, name: str):
        image_path = QFileDialog.getExistingDirectory(self, 'Search image', '')

        if os.path.isfile(image_path):
            self.imgs_dict.update({name: image_path})
            img = QPixmap(image_path) \
                .scaledToWidth(obj.frameGeometry().width()) \
                .scaledToWidth(obj.frameGeometry().height())
            obj.setPixmap(img)
        self.show()
