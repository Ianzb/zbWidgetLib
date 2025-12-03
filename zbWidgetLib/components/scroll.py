from ..base import *
from .page import BasicTab


class ScrollMessageBoxBase(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scrollArea = BasicTab(self)
        self.scrollArea.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.scrollLayout = self.scrollArea.vBoxLayout

        self.viewLayout.addWidget(self.scrollArea, 0)

        QScroller.grabGesture(self.viewport(), QScroller.ScrollerGestureType.TouchGesture)


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
