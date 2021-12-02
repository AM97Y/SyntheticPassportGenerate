from datetime import datetime

from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication

from ChangeDataDialog import ChangeDataDialog
from ImageCreator import ImageCreator
from MessageBox import MessageBox
from Passport import PassportAppearance, PassportContent
from utils.path_utils import Paths
from utils.qt_utils import add_pixmap_to_widget, convert_dateedit_to_datetime


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('MainWindow.ui', self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon('Icons/MainWindow.ico'))

        self._connect_signals_slots()

        self._passport_content = PassportContent()
        self._passport_appearance = PassportAppearance()

        self._img = None
        self._img_creator = None
        self._dialog = None

    def _update_passport(self):
        # Init passport parameters according to the content of dialog window
        new_parameters_appearance = {
            'blurCheckBox': self._dialog.blurCheckBox.isChecked(),  # if Blur is applied to passport image
            'crumpledCheckBox': self._dialog.crumpledCheckBox.isChecked(),
            # if "Crumpled paper" effect is applied to passport image
            'noiseCheckBox': self._dialog.noiseCheckBox.isChecked(),  # if Noise is applied to passport image
            'blotsnumSpinBox': self._dialog.blotsnumSpinBox.value(),  # count of blots to draw on passport image
            'flashnumSpinBox': self._dialog.flashnumSpinBox.value(),  # count of flashes to draw on passport image
            'blurFlashnumBlotsnum': self._dialog.blurFlashnumBlotsnum.value(),
            'fontComboBox': self._dialog.fontComboBox.currentText(),  # font for passport data text fields
            'fontsizeSpinBox': self._dialog.fontsizeSpinBox.value(),  # font size
            'fontblurSpinBox': self._dialog.fontblurSpinBox.value(),  # font blur value
            'color_text': (255 - int((255.0 * (self._dialog.fontblurSpinBox.value() / 100)))),  # font color
        }
        new_passport_content = {
            'first_name': self._dialog.nameLineEdit.text(),
            'second_name': self._dialog.surnameLineEdit.text(),
            'patronymic_name': self._dialog.patronymicLineEdit.text(),
            'series_passport': self._dialog.serieSpinBox.value(),
            'address': self._dialog.birthPlacelineEdit.text(),
            'number_passport': self._dialog.numberSpinBox.value(),
            'department_code': [self._dialog.codeSpinBox1.value(), self._dialog.codeSpinBox2.value()],
            'department': self._dialog.organizationLineEdit.text(),
            'date_issue': convert_dateedit_to_datetime(self._dialog.issueDateEdit),
            'date_birth': convert_dateedit_to_datetime(self._dialog.birthDateEdit),
            'sex': self._dialog.sexComboBox.currentText(),
            'images': {
                **self._dialog.images_content,
                'background': self._passport_content.content["images"]["background"],
            }
        }
        # Update passport parameters
        self._passport_content.update(new_passport_content)
        self._passport_appearance.update(new_parameters_appearance)
        # Generate passport image with new passport parameters
        self._create_image_passport()

    def _create_image_passport(self) -> None:
        """
        Create image passport
        """
        self._img_creator = ImageCreator(self._passport_content.content, self._passport_appearance.content)
        self._img = self._img_creator.create_image()

        qimage = ImageQt(self._img)
        add_pixmap_to_widget(QPixmap.fromImage(qimage), self.passportImg)

    def _show_changedata_dialog(self) -> None:
        """
        Show dialog window with passport parameters
        """
        self._dialog = ChangeDataDialog(self._passport_content.content, self._passport_appearance.content)
        self._dialog.buttonBox.accepted.connect(self._update_passport)
        self._dialog.show()

    def _save_passport_image(self) -> None:
        new_img_file = f'{datetime.now().strftime("%Y-%m-%d-%H.%M.%S.%f")}.png'
        try:
            self._img.save(str(Paths.outputs() / new_img_file))
            self.statusBar.showMessage('Save file ' + new_img_file)
        except AttributeError:
            error_dialog = MessageBox()
            error_dialog.show_message('Изображение не сгенерировано')

    def _show_generated_passport_image(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self._passport_content.random_init()
        self._passport_appearance.random_init()
        self._create_image_passport()
        QApplication.restoreOverrideCursor()

    def _connect_signals_slots(self) -> None:
        self.changeButton.clicked.connect(self._show_changedata_dialog)
        self.saveButton.clicked.connect(self._save_passport_image)
        self.generateButton.clicked.connect(self._show_generated_passport_image)
