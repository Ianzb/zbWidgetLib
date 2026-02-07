from .base import *


def setToolTip(widget, text: str):
    widget.setToolTip(text)
    if not hasattr(widget, "newToolTipEventFilter"):
        widget.newToolTipEventFilter = ToolTipFilter(widget, 1000)
    widget.installEventFilter(widget.newToolTipEventFilter)


def removeToolTip(widget):
    if hasattr(widget, "newToolTipEventFilter"):
        widget.removeEventFilter(widget.newToolTipEventFilter)
        widget.newToolTipEventFilter.deleteLater()
        del widget.newToolTipEventFilter
    widget.setToolTip("")


QWidget.setNewToolTip = setToolTip
QWidget.removeNewToolTip = removeToolTip


def setSelectable(widget):
    widget.setTextInteractionFlags(Qt.TextSelectableByMouse)
    widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)


QLabel.setSelectable = setSelectable
