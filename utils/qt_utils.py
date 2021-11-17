from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


def add_pixmap_to_widget(pixmap: QPixmap, widget: QLabel) -> None:
    img = pixmap \
        .scaledToWidth(widget.frameGeometry().width()) \
        .scaledToWidth(widget.frameGeometry().width())
    widget.setPixmap(img)
