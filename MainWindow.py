from datetime import datetime

from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from ChangeDataDialog import ChangeDataDialog
from Passport import PassportAppearance, PassportContent
from ImageCreator import ImageCreator
from utils.path_utils import Paths
from MessageBox import MessageBox


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('MainWindow.ui', self)
        self.setFixedSize(self.width(), self.height())
        # self.setWindowIcon(QtGui.QIcon('Icons/thermometer.ico'))
        self.img = None

        self.changeButton.clicked.connect(self.show_change_dialog)
        self.saveButton.clicked.connect(self.save)
        self.generateButton.clicked.connect(self.show_generate)
        self.generatePathButton.clicked.connect(self._generate_path)

        self.passport_content = PassportContent()
        self.passport_appearance = PassportAppearance()

        self.img_creator = None

        self._dialog = None

    def _update_passport(self):
        """
        Update passport data after changed.

        """
        new_parameters_appearance = {
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
        }
        new_passport_content = {
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
            'images': {'label_photo': self._dialog.imgs_dict['label_photo'],
                       'label_signature_1': self._dialog.imgs_dict['label_signature_1'],
                       'label_signature_2': self._dialog.imgs_dict['label_signature_2'],
                       'background': self.passport_content.parameters["images"]["background"],
                       },
        }

        self.passport_content.update(new_passport_content)
        self.passport_appearance.update(new_parameters_appearance)

        self._create_image_passport()

    def show_generate(self):
        """
        Generate new passport image.
        :return:
        """
        self.passport_content.random_init()
        self.passport_appearance.random_init()
        self._create_image_passport()

    def _generate_path(self):
        """
        Generate path of passport images.

        """
        # self.generate_path = QFileDialog.getExistingDirectory(self, 'Search path gen', HOME, QFileDialog.ShowDirsOnly)
        count_examples = self.genSpinBox.value()
        for i in range(0, count_examples):
            self.passport_content.random_init()
            self.passport_appearance.random_init()

            self.img_creator = ImageCreator(self.passport_content.parameters, self.passport_appearance.parameters)
            self.img = self.img_creator.create_image()

            img_filepath = Paths.outputs() / f'{datetime.now().strftime("%Y-%m-%d-%H.%M.%S.%f")}.png'
            self.img.save(str(img_filepath))
            self.progressBar.setValue((i / count_examples) * 100)
        self.progressBar.setValue(100)

    def _create_image_passport(self) -> None:
        """
        Create image passport.

        """
        self.img_creator = ImageCreator(self.passport_content.parameters, self.passport_appearance.parameters)
        self.img = self.img_creator.create_image()

        qimage = ImageQt(self.img)
        img = QPixmap.fromImage(qimage) \
            .scaledToWidth(self.passportImg.frameGeometry().width() - 400) \
            .scaledToWidth(self.passportImg.frameGeometry().height() - 400)
        self.passportImg.setPixmap(img)
        # self.passportImg ДОБАВИТЬ СКРОЛИН И ЧТОБЫ ОКНО НЕ УВЕЛИЧИТЬ.

    def save(self) -> None:
        """
        Save created images.

        """
        """
        save_path = QFileDialog.getExistingDirectory(self, caption="Open Directory")
        print('save_path: ', save_path)
        img_file_path = Paths.outputs(save_path) / f'{datetime.now().strftime("%Y-%m-%d-%H.%M.%S.%f")}.png'
        self.img.save(str(img_file_path))
        """
        save_path = QFileDialog.getExistingDirectory(self, caption="Open Directory")
        print('save_path:', save_path)
        img_file_path = Paths.outputs() / f'{datetime.now().strftime("%Y-%m-%d-%H.%M.%S.%f")}.png'
        try:
            self.img.save(str(img_file_path))
        except AttributeError:
            error_dialog = MessageBox()
            error_dialog.showMessage('Изображение не сгенерированно     ')

    def show_change_dialog(self) -> None:
        """
        Call ChangeDataDialog.

        """
        self._dialog = ChangeDataDialog(self.passport_content.parameters, self.passport_appearance.parameters)
        self._dialog.buttonBox.accepted.connect(self._update_passport)
        self._dialog.show()
