from PyQt5.QtWidgets import QMessageBox, QWidget


class MessageBox(QWidget):
    def __init__(self):
        super().__init__()

    def showMessage(self, text: str):
        QMessageBox.about(self, "Error", text)
        self.show()
