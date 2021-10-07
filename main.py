
import sys
import MainWindow

from PyQt5.QtWidgets import *

app = QApplication(sys.argv)

mw = MainWindow.MainWindow()
mw.show()

sys.exit(app.exec_())
