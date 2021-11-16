from PyQt5.QtWidgets import QMessageBox, QWidget


class MessageBox(QWidget):
    def __init__(self):
        super().__init__()

    def show_message(self, text: str):
        QMessageBox.about(self, "Error", text)
        self.show()
