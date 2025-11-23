from ..base import *
from .page import BasicTab

class BetterScrollArea(SmoothScrollArea):
    def __init__(self, parent=None):
        """
        优化样式的滚动区域
        :param parent:
        """
        super().__init__(parent=parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("QScrollArea {background-color: rgba(0,0,0,0); border: none}")

        self.setScrollAnimation(Qt.Vertical, 500, QEasingCurve.OutQuint)
        self.setScrollAnimation(Qt.Horizontal, 500, QEasingCurve.OutQuint)

        self.view = QWidget(self)
        self.view.setStyleSheet("QWidget {background-color: rgba(0,0,0,0); border: none}")

        self.setWidget(self.view)

        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)


class ScrollMessageBoxBase(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scrollArea = BasicTab(self)
        self.scrollArea.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.scrollLayout = self.scrollArea.vBoxLayout

        self.viewLayout.addWidget(self.scrollArea, 0)


class ScrollMessageBox(ScrollMessageBoxBase):
    def __init__(self, title: str, content: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = TitleLabel(title, self)
        self.contentLabel = BodyLabel(content, self)
        self.contentLabel.setWordWrap(True)

        self.viewLayout.insertWidget(0, self.titleLabel)
        self.scrollLayout.addWidget(self.contentLabel)


class ScrollDialog(Dialog):
    def __init__(self, title: str, content: str, parent=None):
        super().__init__(title, content, parent)
        self.scrollArea = BasicTab(self)
        self.scrollArea.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.scrollLayout = self.scrollArea.vBoxLayout

        self.textLayout.removeWidget(self.contentLabel)
        self.scrollLayout.addWidget(self.contentLabel, 0)

        self.contentLabel.setWordWrap(True)
        self.contentLabel.adjustSize()

        self._adjustSize()

    def _adjustSize(self):
        content_height = self.contentLabel.sizeHint().height()
        MAX_HEIGHT = self.maximumHeight()
        # 最小高度为内容高度（不超过MAX），最大高度固定为MAX
        self.scrollArea.setMinimumHeight(min(content_height, MAX_HEIGHT))
        self.scrollArea.setMaximumHeight(MAX_HEIGHT)
        # 让scrollArea在垂直方向为固定高度（由上面控制），水平方向可扩展
        self.scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 添加滚动区域到布局
        self.textLayout.addWidget(self.scrollArea, 0)

    def setMaximumHeight(self, maxh: int, adjust: bool = True):
        super().setMaximumHeight(maxh)
        if adjust:
            self._adjustSize()
