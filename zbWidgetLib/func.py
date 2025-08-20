from .base import *


def setToolTip(widget, text: str):
    widget.setToolTip(text)
    widget.installEventFilter(AcrylicToolTipFilter(widget, 1000))


QWidget.setNewToolTip = setToolTip


def setSelectable(widget):
    widget.setTextInteractionFlags(Qt.TextSelectableByMouse)
    widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)


QLabel.setSelectable = setSelectable
