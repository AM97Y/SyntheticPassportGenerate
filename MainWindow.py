from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QImage

import ChangeDataDialog
from PyQt5 import uic
from PyQt5.QtWidgets import *

from datetime import datetime

import Passport
import passportDrawer.TextFont2Img as imgGenerate


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('MainWindow.ui', self)
        # self.setFixedSize(self.width(), self.height())
        # self.setWindowIcon(QtGui.QIcon('Icons/thermometer.ico'))
        self.img = None

        self.changeButton.clicked.connect(self.showChangeDataDialog)
        self.saveButton.clicked.connect(self.save)
        self.generateButton.clicked.connect(self.showGenerate)

        self.passport = Passport.Passport()
        self.generate = Passport.GenerateImg()

        self._dialog = None
        self.output_path = './output'

    def _update_passport(self):
        new_parameters_generate = {
            'blurCheckBox': self._dialog.blurCheckBox.isChecked(),
            'crumpledCheckBox': self._dialog.crumpledCheckBox.isChecked(),
            'noiseCheckBox': self._dialog.noiseCheckBox.isChecked(),
            'blotsnumSpinBox': self._dialog.blotsnumSpinBox.value(),
            'flashnumSpinBox': self._dialog.flashnumSpinBox.value(),
            'blurFlashnumBlotsnum': self._dialog.blurFlashnumBlotsnum.value(),
            'fontComboBox': self._dialog.fontComboBox.currentText(),
            'fontsizeSpinBox': self._dialog.fontsizeSpinBox.value(),
            'fontblurSpinBox': self._dialog.fontblurSpinBox.value(),
            'images': {'labelFoto': self._dialog.imgs_dict['labelFoto'],
                       'label_signature_1': self._dialog.imgs_dict['label_signature_1'],
                       'label_signature_2': self._dialog.imgs_dict['label_signature_2'],
                       'background': self.generate.parameters_generate["images"]["background"],
                       }
        }
        new_passport_data = {
            'firstName': self._dialog.nameLineEdit.text(),
            'secondName': self._dialog.surnameLineEdit1.text(),
            'patronymicName': self._dialog.patronymicLineEdit.text(),
            'asdress': self._dialog,
            'seriesPassport': self._dialog.serieSpinBox.value(),
            'numberPassport': self._dialog.numberSpinBox.value(),
            'departmentCode': [self._dialog.codeSpinBox1.value(), self._dialog.codeSpinBox2.value()],
            'department': self._dialog.organizationLineEdit1.text(),
            'city': self._dialog.birthplaceLineEdit1.text(),
            'dateOFissue': self._dialog.issueDateEdit.date(),
            'dateOFbirth': self._dialog.birthDateEdit.date(),
            'sex': self._dialog.sexComboBox.currentText(),
        }

        self.passport.update(new_passport_data)
        self.generate.update(new_parameters_generate)

        self._create_image_passport()

    def showGenerate(self):
        self.passport.random_init()
        self.generate.random_init()
        self._create_image_passport()
        print('showGenerate')

    def _create_image_passport(self):
        self.img = self.generate.create_image(self.passport.passport_data)
        # img = QtGui.QPixmap(self.img)
        print(self.passportView, self.img)
        # self.passportView.setPixmap(self.img)
        # uic.loadUi('MainWindow.ui', self)
        qimage = qim = ImageQt(self.img)
        img = QPixmap.fromImage(qimage) \
            .scaledToWidth(self.passportImg.frameGeometry().width() - 400) \
            .scaledToWidth(self.passportImg.frameGeometry().height() - 400)
        self.passportImg.setPixmap(img)
        # self.passportImg ДОБАВИТЬ СКРОЛИН И ЧТОБЫ ОКНО НЕ УВЕЛИЧИТЬ.
        self.show()

    def save(self):
        today = datetime.now()
        self.img.save(f'{self.output_path}/{today.strftime("%Y-%m-%d-%H.%M.%S.%f")}.png')

    def showChangeDataDialog(self):
        print('ChangeDataDialog')
        self._dialog = ChangeDataDialog.ChangeDataDialog(self.passport.passport_data, self.generate.parameters_generate)
        self._dialog.buttonBox.accepted.connect(self._update_passport)
        self._dialog.show()
