from ..base import *
from .card import DisplayCard
from .progress import CustomProgressRing


class LoadingCard(DisplayCard):

    def __init__(self, parent=None, indeterminate: bool = True):
        """
        加载中卡片
        """
        super().__init__(parent)
        self.progressRing = CustomProgressRing(indeterminate=indeterminate)
        self.setDisplay(self.progressRing)
        self.setText("加载中...")

    def setVal(self, val: int):
        self.progressRing.setVal(val)

    def setValue(self, val: int):
        self.setVal(val)

    def setProgress(self, val: int):
        self.setVal(val)

    def getVal(self):
        return self.progressRing.getVal()

    def getValue(self):
        return self.getVal()

    def getProgress(self):
        return self.getVal()


class LoadingMessageBox(MaskDialogBase):
    def __init__(self, parent=None, indeterminate: bool = True):
        super().__init__(parent=parent)

        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)
        self.vBoxLayout = QVBoxLayout(self.widget)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(16, 16, 16, 16)

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))

        self.progressRing = CustomProgressRing(indeterminate=indeterminate)

        self.loadingCard = DisplayCard(self.widget)
        self.loadingCard.setText("加载中...")
        setattr(self.loadingCard, "_normalBackgroundColor", lambda: QColor(16, 16, 16, 220) if isDarkTheme() else QColor(255, 255, 255, 220))
        setattr(self.loadingCard, "_hoverBackgroundColor", lambda: QColor(16, 16, 16, 255) if isDarkTheme() else QColor(255, 255, 255, 255))
        setattr(self.loadingCard, "_pressedBackgroundColor", lambda: QColor(16, 16, 16, 110) if isDarkTheme() else QColor(255, 255, 255, 110))
        self.loadingCard.setBackgroundColor(QColor(16, 16, 16, 220) if isDarkTheme() else QColor(255, 255, 255, 220))

        self.loadingCard.setDisplay(self.progressRing)
        self.vBoxLayout.addWidget(self.loadingCard, 1)

    def setVal(self, val: int):
        self.progressRing.setVal(val)

    def setValue(self, val: int):
        self.setVal(val)

    def setProgress(self, val: int):
        self.setVal(val)

    def getVal(self):
        return self.progressRing.getVal()

    def getValue(self):
        return self.getVal()

    def getProgress(self):
        return self.getVal()

    def setText(self, text: str):
        self.loadingCard.setText(text)

    def getText(self):
        return self.loadingCard.getText()

    def finish(self):
        self.accept()

    def close(self):
        self.finish()
        super().close()

    def done(self, code):
        """ fade out """
        self.widget.setGraphicsEffect(None)
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(1)
        opacityAni.setEndValue(0)
        opacityAni.setDuration(100)
        opacityAni.finished.connect(lambda: self._onDone(code))
        opacityAni.finished.connect(self.deleteLater)
        opacityAni.start()

    def showEvent(self, e):
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_ani = QPropertyAnimation(self.opacity_effect, b'opacity', self)
        self.opacity_ani.setStartValue(0)
        self.opacity_ani.setEndValue(1)
        self.opacity_ani.setDuration(200)
        self.opacity_ani.setEasingCurve(QEasingCurve.InSine)
        self.opacity_ani.finished.connect(lambda: self.setGraphicsEffect(None))
        self.opacity_ani.start()
        super(QDialog, self).showEvent(e)

    def closeEvent(self, e):
        if hasattr(self, 'opacity_ani') and self.opacity_ani.state() == QPropertyAnimation.Running:
            self.opacity_ani.stop()
            self.setGraphicsEffect(None)
            try:
                self.opacity_ani.deleteLater()
                self.opacity_effect.deleteLater()
            except:
                pass
        super().closeEvent(e)
