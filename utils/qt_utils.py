from datetime import datetime

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QDateEdit


def add_pixmap_to_widget(pixmap: QPixmap, widget: QLabel) -> None:
    img = pixmap \
        .scaledToWidth(widget.frameGeometry().width()) \
        .scaledToWidth(widget.frameGeometry().width())
    widget.setPixmap(img)


def get_data(obj: QDateEdit) -> datetime:
    return datetime(obj.date().year(), obj.date().month(), obj.date().day())
