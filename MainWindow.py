from datetime import datetime

from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow

from ChangeDataDialog import ChangeDataDialog
from Passport import Passport, GenerateImg


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('MainWindow.ui', self)
        # self.setFixedSize(self.width(), self.height())
        # self.setWindowIcon(QtGui.QIcon('Icons/thermometer.ico'))
        self.img = None

        self.changeButton.clicked.connect(self.show_change_dialog)
        self.saveButton.clicked.connect(self.save)
        self.generateButton.clicked.connect(self.show_generate)

        self.passport = Passport()
        self.generate = GenerateImg()

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
            'upperCheckBox': self._dialog.upperCheckBox.isChecked(),
            'color_text': (self._dialog.codeSpinBox1_R.value(), self._dialog.codeSpinBox1_G.value(),
                           self._dialog.codeSpinBox1_B.value()),
            'images': {'label_photo': self._dialog.imgs_dict['label_photo'],
                       'label_signature_1': self._dialog.imgs_dict['label_signature_1'],
                       'label_signature_2': self._dialog.imgs_dict['label_signature_2'],
                       'background': self.generate.parameters_generate["images"]["background"],
                       }
        }
        print(self._dialog.upperCheckBox.isChecked())
        new_passport_data = {
            'first_name': self._dialog.nameLineEdit.text(),
            'second_name': self._dialog.surnameLineEdit1.text(),
            'patronymic_name': self._dialog.patronymicLineEdit.text(),
            'address': self._dialog.birthplaceLineEdit1.text(),
            'series_passport': self._dialog.serieSpinBox.value(),
            'number_passport': self._dialog.numberSpinBox.value(),
            'department_code': [self._dialog.codeSpinBox1.value(), self._dialog.codeSpinBox2.value()],
            'department': self._dialog.organizationLineEdit1.text(),
            'date_issue': self._dialog.issueDateEdit.date().currentDate().toPyDate(),
            'date_birth': self._dialog.birthDateEdit.date().currentDate().toPyDate(),
            'sex': self._dialog.sexComboBox.currentText(),
        }

        self.passport.update(new_passport_data)
        self.generate.update(new_parameters_generate)

        self._create_image_passport()

    def show_generate(self):
        self.passport.random_init()
        self.generate.random_init()
        self._create_image_passport()

    def _create_image_passport(self):
        self.img = self.generate.create_image(self.passport.passport_data)
        qimage = ImageQt(self.img)
        img = QPixmap.fromImage(qimage) \
            .scaledToWidth(self.passportImg.frameGeometry().width() - 400) \
            .scaledToWidth(self.passportImg.frameGeometry().height() - 400)
        self.passportImg.setPixmap(img)
        # self.passportImg ДОБАВИТЬ СКРОЛИН И ЧТОБЫ ОКНО НЕ УВЕЛИЧИТЬ.
        self.show()

    def save(self):
        today = datetime.now()
        self.img.save(f'{self.output_path}/{today.strftime("%Y-%m-%d-%H.%M.%S.%f")}.png')

    def show_change_dialog(self):
        self._dialog = ChangeDataDialog(self.passport.passport_data, self.generate.parameters_generate)
        self._dialog.buttonBox.accepted.connect(self._update_passport)
        self._dialog.show()
