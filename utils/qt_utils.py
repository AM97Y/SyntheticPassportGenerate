from PyQt5.QtGui import QPixmap


def add_pixmap_to_widget(pixmap, widget):
    img = pixmap \
        .scaledToWidth(widget.frameGeometry().width()) \
        .scaledToWidth(widget.frameGeometry().width())
    widget.setPixmap(img)
