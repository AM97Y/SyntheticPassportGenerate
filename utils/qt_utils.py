from datetime import datetime

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QDateEdit


def add_pixmap_to_widget(pixmap: QPixmap, widget: QLabel) -> None:
    """
    This function add image to widget.

    :param pixmap: Pixmap with image.
    :param widget: Widget which pixmap is added.
    """
    img = pixmap \
        .scaledToWidth(widget.frameGeometry().width()) \
        .scaledToWidth(widget.frameGeometry().width())
    widget.setPixmap(img)


def get_data(obj: QDateEdit) -> datetime:
    """
    This function covert QDateEdit to datatime.

    :param obj: DateEdit field.
    :return: Data by datatime.
    """
    return datetime(obj.date().year(), obj.date().month(), obj.date().day())
