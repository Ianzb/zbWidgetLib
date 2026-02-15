from .base import *


def QWidgetSetToolTip(self, text: str):
    self.setOldToolTip(text)
    if not hasattr(self, "newToolTipEventFilter"):
        self.newToolTipEventFilter = ToolTipFilter(self, 1000)
    self.installEventFilter(self.newToolTipEventFilter)


def QWidgetRemoveToolTip(self):
    if hasattr(self, "newToolTipEventFilter"):
        self.removeEventFilter(self.newToolTipEventFilter)
        self.newToolTipEventFilter.deleteLater()
        del self.newToolTipEventFilter
    self.setOldToolTip("")


QWidget.setOldToolTip = QWidget.setToolTip
QWidget.setToolTip = QWidgetSetToolTip
QWidget.removeToolTip = QWidgetRemoveToolTip


def setSelectable(widget):
    widget.setTextInteractionFlags(Qt.TextSelectableByMouse)
    widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)


QLabel.setSelectable = setSelectable


def MaskDialogBaseHide(self):
    """ fade out """
    self.widget.setGraphicsEffect(None)
    opacityEffect = QGraphicsOpacityEffect(self)
    self.setGraphicsEffect(opacityEffect)
    opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
    opacityAni.setStartValue(1)
    opacityAni.setEndValue(0)
    opacityAni.setDuration(100)
    opacityAni.finished.connect(self._onHide)
    opacityAni.start()


def MaskDialogBase_onHide(self):
    self.setGraphicsEffect(None)
    super(MaskDialogBase, self).hide()


MaskDialogBase.hide = MaskDialogBaseHide
MaskDialogBase._onHide = MaskDialogBase_onHide
