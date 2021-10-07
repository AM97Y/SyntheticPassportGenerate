import ChangeDataDialog
from PyQt5 import uic
from PyQt5.QtWidgets import *

from datetime import datetime

import Passport
import passportDrawer.TextFont2Img as textGenerate


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
                       #'background': ['file_background', self._load_markup('file_background')]
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

    def showGenerate(self):
        self.passport.random_init()
        self.generate.random_init()
        #img = textGenerate("args.config_file").create_text_images(self.passport.passport_data, self.generate.parameters_generate)
        print('showGenerate')

    def save(self):
        today = datetime.now()
        self.img.save(f'{self.output_path}/{today.strftime("%Y-%m-%d-%H.%M.%S.%f")}.png')

    def showChangeDataDialog(self):
        print('ChangeDataDialog')
        self._dialog = ChangeDataDialog.ChangeDataDialog(self.passport.passport_data, self.generate.parameters_generate)
        self._dialog.buttonBox.accepted.connect(self._update_passport)
        self._dialog.show()
