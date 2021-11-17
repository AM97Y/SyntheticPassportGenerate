from datetime import datetime

from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDateEdit

from ChangeDataDialog import ChangeDataDialog
from Passport import PassportAppearance, PassportContent
from ImageCreator import ImageCreator
from utils.path_utils import Paths
from utils.qt_utils import add_pixmap_to_widget
from MessageBox import MessageBox


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('MainWindow.ui', self)
        self.setFixedSize(self.width(), self.height())
        # self.setWindowIcon(QtGui.QIcon('Icons/thermometer.ico'))

        self._connect_signals_slots()

        self._passport_content = PassportContent()
        self._passport_appearance = PassportAppearance()

        self._img = None
        self._img_creator = None

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
            'color_text': (255 - int((255.0 * (self._dialog.fontblurSpinBox.value() / 100)))),
        }
        new_passport_content = {
            'first_name': self._dialog.nameLineEdit.text(),
            'second_name': self._dialog.surnameLineEdit.text(),
            'patronymic_name': self._dialog.patronymicLineEdit.text(),
            'series_passport': self._dialog.serieSpinBox.value(),
            'number_passport': self._dialog.numberSpinBox.value(),
            'department_code': [self._dialog.codeSpinBox1.value(), self._dialog.codeSpinBox2.value()],
            'department': self._dialog.organizationLineEdit.text(),
            'date_issue': self._get_data(self._dialog.issueDateEdit),
            'date_birth': self._get_data(self._dialog.birthDateEdit),
            'sex': self._dialog.sexComboBox.currentText(),
            'images': {
                **self._dialog.images_content,
                'background': self._passport_content.content["images"]["background"],
            }
        }

        self._passport_content.update(new_passport_content)
        self._passport_appearance.update(new_parameters_appearance)
        self._create_image_passport()

    @staticmethod
    def _get_data(obj: QDateEdit):
        return datetime(obj.date().year(), obj.date().month(), obj.date().day())

    def show_generate(self):
        """
        Generate new passport image.
        :return:
        """
        self._passport_content.random_init()
        self._passport_appearance.random_init()
        self._create_image_passport()

    def _create_image_passport(self) -> None:
        """
        Create image passport.

        """
        self._img_creator = ImageCreator(self._passport_content.content, self._passport_appearance.content)
        self._img = self._img_creator.create_image()

        qimage = ImageQt(self._img)
        add_pixmap_to_widget(QPixmap.fromImage(qimage), self.passportImg)

    def save(self) -> None:
        """
        Save created images.

        """
        file = f'{datetime.now().strftime("%Y-%m-%d-%H.%M.%S.%f")}.png'
        img_file_path = Paths.outputs() / file
        try:
            self._img.save(str(img_file_path))
            self.statusBar.showMessage('Save file ' + file)
            # timer = QTimer()
            # timer.start(2147483647)
            # self.label.setText('')
        except AttributeError:
            error_dialog = MessageBox()
            error_dialog.show_message('Изображение не сгенерированно')

    def show_change_dialog(self) -> None:
        """
        Call ChangeDataDialog.

        """
        self._dialog = ChangeDataDialog(self._passport_content.content, self._passport_appearance.content)
        self._dialog.buttonBox.accepted.connect(self._update_passport)
        self._dialog.show()

    def _connect_signals_slots(self):
        self.changeButton.clicked.connect(self.show_change_dialog)
        self.saveButton.clicked.connect(self.save)
        self.generateButton.clicked.connect(self.show_generate)
