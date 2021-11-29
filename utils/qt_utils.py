from datetime import datetime

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QDateEdit


def add_pixmap_to_widget(pixmap: QPixmap, widget: QLabel) -> None:
    """
    This function add pixmap to widget

    :param pixmap: pixmap to add
    :param widget: widget to store the pixmap
    """
    img = pixmap \
        .scaledToWidth(widget.frameGeometry().width()) \
        .scaledToWidth(widget.frameGeometry().width())
    widget.setPixmap(img)


def get_data(obj: QDateEdit) -> datetime:
    """
    This function convert QDateEdit to datatime

    :param obj: DateEdit content
    :return: data stored as datatime
    """
    return datetime(obj.date().year(), obj.date().month(), obj.date().day())
