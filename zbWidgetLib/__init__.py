from concurrent.futures import ThreadPoolExecutor

from .base import *
from .page import *


def setToolTip(widget: QWidget, text: str):
    widget.setToolTip(text)
    widget.installEventFilter(ToolTipFilter(widget, 1000))


class StatisticsWidget(QWidget):

    def __init__(self, title: str, value: str, parent: QWidget = None):
        """
        两行信息组件
        :param title: 标题
        :param value: 值
        """
        super().__init__(parent=parent)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = BodyLabel(value, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(16, 0, 16, 0)
        self.vBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignBottom)

        setFont(self.valueLabel, 18, QFont.Weight.DemiBold)
        self.titleLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))


class Image(QLabel):
    downloadFinishedSignal = Signal(bool)

    @functools.singledispatchmethod
    def __init__(self, parent: QWidget = None):
        """
        图片组件（可实时下载）
        """
        super().__init__(parent=parent)
        self.setFixedSize(48, 48)
        self.setScaledContents(True)
        self.loading = False
        self.downloadFinishedSignal.connect(self.downloadFinished)

    @__init__.register
    def _(self, path: str, url: str = None, parent: QWidget = None, thread_pool: ThreadPoolExecutor = None):
        """
        图片组件（可实时下载）
        :param path: 路径
        :param url: 链接
        :param parent:
        :param thread_pool: 线程池
        """
        self.__init__(parent)
        if path:
            self.setImg(path, url, thread_pool)

    @__init__.register
    def _(self, path: str, parent: QWidget = None):
        """
        :param path: 路径
        """
        self.__init__(parent)
        if path:
            self.setImg(path)

    def setImg(self, path: str, url: str = None, thread_pool: ThreadPoolExecutor = None):
        """
        设置图片
        :param path: 路径
        :param url: 链接
        :param thread_pool: 下载线程池
        """
        if url:
            self.loading = True
            self.path = path
            self.url = url

            thread_pool.submit(self.download)
        else:
            self.loading = False
            self.setPixmap(QPixmap(path))

    def downloadFinished(self, msg):
        if not self.loading:
            return
        if msg or zb.existPath(self.path):
            self.setImg(self.path)

    def download(self):
        if zb.existPath(self.path):
            self.downloadFinishedSignal.emit(True)
            return
        msg = zb.singleDownload(self.url, self.path, False, True, zb.REQUEST_HEADER)
        self.downloadFinishedSignal.emit(bool(msg))


class CopyTextButton(ToolButton):

    def __init__(self, text: str, data: str = "", parent: QWidget = None):
        """
        复制文本按钮
        :param text: 复制的文本
        :param data: 复制文本的提示信息，可以提示复制文本的内容类型
        :param parent: 父组件
        """
        super().__init__(FIF.COPY, parent)
        self._text = text
        self._data = data
        self.clicked.connect(self.copyButtonClicked)
        if self._data is None:
            self._data = ""
        self.set(self._text, self._data)

    def set(self, text: str, data: str = ""):
        """
        设置信息
        :param text: 复制的文本
        :param data: 复制文本的提示信息，可以提示复制文本的内容类型
        :return:
        """
        if not text:
            self.setEnabled(False)
            return
        self._text = text
        self._data = data

        setToolTip(self, f"点击复制{self._data}信息！")

    def text(self):
        """
        复制的文本
        :return: 复制的文本
        """
        return self._text

    def setText(self, text: str):
        """
        设置复制的文本
        :param text: 复制的文本
        """
        self.set(text)

    def setData(self, data: str):
        """
        设置复制文本的提示信息
        :param data: 复制文本的提示信息
        """
        self.set(self.text(), data)

    def copyButtonClicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self._text)


class DisplayCard(ElevatedCardWidget):

    def __init__(self, parent: QWidget = None):
        """
        大图片卡片
        """
        super().__init__(parent)
        self.setFixedSize(168, 176)

        self.widget = Image(self)

        self.bodyLabel = CaptionLabel(self)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.widget, 0, Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.bodyLabel, 0, Qt.AlignHCenter | Qt.AlignBottom)

    def setText(self, text: str):
        """
        设置文本
        :param text: 文本
        """
        self.bodyLabel.setText(text)

    def text(self):
        """
        设置文本
        :return: 文本
        """
        return self.bodyLabel.text()

    def setDisplay(self, widget):
        """
        设置展示组件
        :param widget: 组件
        """
        self.widget = widget
        self.vBoxLayout.replaceWidget(self.vBoxLayout.itemAt(1).widget(), self.widget)


class IntroductionCard(ElevatedCardWidget):

    def __init__(self, parent: QWidget = None):
        """
        简介卡片
        """
        super().__init__(parent)
        self.setFixedSize(190, 200)

        self.image = Image(self)
        self.titleLabel = SubtitleLabel(self)
        self.titleLabel.setWordWrap(True)
        self.bodyLabel = BodyLabel(self)
        self.bodyLabel.setWordWrap(True)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(16, 16, 16, 16)
        self.vBoxLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.vBoxLayout.addWidget(self.image, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.bodyLabel, 0, Qt.AlignLeft)

    def setImg(self, path: str, url: str = None, thread_pool: ThreadPoolExecutor = None):
        """
        设置图片
        :param path: 路径
        :param url: 连接
        :param thread_pool: 下载线程池
        """
        self.image.setImg(path, url, thread_pool)

    def setTitle(self, text: str):
        """
        设置标题
        :param text: 文本
        """
        self.titleLabel.setText(text)

    def setText(self, text: str):
        """
        设置标题
        :param text: 文本
        """
        self.bodyLabel.setText(text)


class LoadingCard(DisplayCard):

    def __init__(self, parent: QWidget = None):
        """
        加载中卡片
        """
        super().__init__(parent)
        self.progressRingLoading = IndeterminateProgressRing(self)
        self.setDisplay(self.progressRingLoading)
        self.setText("加载中...")


class GrayCard(QWidget):

    def __init__(self, title: str = None, parent: QWidget = None, alignment: Qt.AlignmentFlag = Qt.AlignLeft):
        """
        灰色背景组件卡片
        :param title: 标题
        """
        super().__init__(parent=parent)

        self.titleLabel = StrongBodyLabel(self)
        if title:
            self.titleLabel.setText(title)
        else:
            self.titleLabel.hide()

        self.card = QFrame(self)
        self.card.setObjectName("GrayCard")

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.card, 0, Qt.AlignTop)

        self.hBoxLayout = QHBoxLayout(self.card)
        self.hBoxLayout.setAlignment(alignment)
        self.hBoxLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(12, 12, 12, 12)

        self.setTheme()
        qconfig.themeChanged.connect(self.setTheme)

    def setTheme(self):
        if isDarkTheme():
            self.card.setStyleSheet("#GrayCard {background-color: rgba(25,25,25,0.5); border:1px solid rgba(20,20,20,0.15); border-radius: 10px}")
        else:
            self.card.setStyleSheet("#GrayCard {background-color: rgba(175,175,175,0.1); border:1px solid rgba(150,150,150,0.15); border-radius: 10px}")

    def addWidget(self, widget, spacing=0, alignment: Qt.AlignmentFlag = Qt.AlignTop):
        """
        添加组件
        :param widget: 组件
        :param spacing: 间隔
        :param alignment: 对齐方式
        """
        self.hBoxLayout.addWidget(widget, alignment=alignment)
        self.hBoxLayout.addSpacing(spacing)

    def insertWidget(self, index: int, widget, alignment: Qt.AlignmentFlag = Qt.AlignTop):
        """
        插入组件
        :param index: 序号
        :param widget: 组件
        :param alignment: 对齐方式
        """
        self.hBoxLayout.insertWidget(index, widget, 0, alignment)


class BigInfoCard(CardWidget):

    def __init__(self, parent: QWidget = None, url: bool = True, tag: bool = True, data: bool = True):
        """
        详细信息卡片
        :param url: 是否展示链接
        :param tag: 是否展示标签
        :param data: 是否展示数据
        """
        super().__init__(parent)
        self.setMinimumWidth(100)

        self.backButton = TransparentToolButton(FIF.RETURN, self)
        self.backButton.move(8, 8)
        self.backButton.setMaximumSize(32, 32)

        self.image = Image(self)

        self.titleLabel = TitleLabel(self)

        self.mainButton = PrimaryPushButton("", self)
        self.mainButton.setFixedWidth(160)

        self.infoLabel = BodyLabel(self)
        self.infoLabel.setWordWrap(True)

        self.hBoxLayout1 = QHBoxLayout()
        self.hBoxLayout1.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout1.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.hBoxLayout1.addWidget(self.mainButton, 0, Qt.AlignRight)

        self.hBoxLayout2 = FlowLayout()
        self.hBoxLayout2.setAnimation(200)
        self.hBoxLayout2.setSpacing(0)
        self.hBoxLayout2.setAlignment(Qt.AlignLeft)

        self.hBoxLayout3 = FlowLayout()
        self.hBoxLayout3.setAnimation(200)
        self.hBoxLayout3.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout3.setSpacing(10)
        self.hBoxLayout3.setAlignment(Qt.AlignLeft)

        self.hBoxLayout4 = FlowLayout()
        self.hBoxLayout4.setAnimation(200)
        self.hBoxLayout4.setSpacing(8)
        self.hBoxLayout4.setAlignment(Qt.AlignLeft)

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addLayout(self.hBoxLayout1)

        if url:
            self.vBoxLayout.addSpacing(3)
            self.vBoxLayout.addLayout(self.hBoxLayout2)
        else:
            self.hBoxLayout2.deleteLater()
        if data:
            self.vBoxLayout.addSpacing(20)
            self.vBoxLayout.addLayout(self.hBoxLayout3)
            self.vBoxLayout.addSpacing(20)
        else:
            self.hBoxLayout3.deleteLater()
        self.vBoxLayout.addWidget(self.infoLabel)
        if tag:
            self.vBoxLayout.addSpacing(12)
            self.vBoxLayout.addLayout(self.hBoxLayout4)
        else:
            self.hBoxLayout4.deleteLater()

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(30)
        self.hBoxLayout.setContentsMargins(34, 24, 24, 24)
        self.hBoxLayout.addWidget(self.image, 0, Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

    def setTitle(self, text: str):
        """
        设置标题
        :param text: 文本
        """
        self.titleLabel.setText(text)

    def setImg(self, path: str, url: str = None, thread_pool: ThreadPoolExecutor = None):
        """
        设置图片
        :param path: 路径
        :param url: 链接
        :param thread_pool: 线程池
        """
        self.image.setImg(path, url, thread_pool)

    def setInfo(self, data: str):
        """
        设置信息
        :param data: 文本
        """
        self.infoLabel.setText(data)

    def addUrl(self, text: str, url: str, icon=None):
        """
        添加链接
        :param text: 文本
        :param url: 链接
        :param icon: 图标
        """
        button = HyperlinkButton(url, text, self)
        if icon:
            button.setIcon(icon)
        self.hBoxLayout2.addWidget(button)

    def addData(self, title: str, data: str | int):
        """
        添加数据
        :param title: 标题
        :param data: 数据
        """
        widget = StatisticsWidget(title, str(data), self)
        if self.hBoxLayout3.count() >= 1:
            seperator = VerticalSeparator(widget)
            seperator.setMinimumHeight(50)
            self.hBoxLayout3.addWidget(seperator)
        self.hBoxLayout3.addWidget(widget)

    def addTag(self, name: str):
        """
        添加标签
        :param name: 名称
        """
        self.tagButton = PillPushButton(name, self)
        self.tagButton.setCheckable(False)
        setFont(self.tagButton, 12)
        self.tagButton.setFixedSize(80, 32)
        self.hBoxLayout4.addWidget(self.tagButton)


class SmallInfoCard(CardWidget):

    def __init__(self, parent: QWidget = None):
        """
        普通信息卡片（搜索列表展示）
        """
        super().__init__(parent)
        self.setMinimumWidth(100)
        self.setFixedHeight(73)

        self.image = Image(self)

        self.titleLabel = BodyLabel(self)

        self._text = ["", "", "", ""]
        self.contentLabel1 = CaptionLabel(f"{self._text[0]}\n{self._text[1]}", self)
        self.contentLabel1.setTextColor("#606060", "#d2d2d2")
        self.contentLabel1.setAlignment(Qt.AlignLeft)

        self.contentLabel2 = CaptionLabel(f"{self._text[2]}\n{self._text[3]}", self)
        self.contentLabel2.setTextColor("#606060", "#d2d2d2")
        self.contentLabel2.setAlignment(Qt.AlignRight)

        self.mainButton = PushButton("", self)

        self.vBoxLayout1 = QVBoxLayout()

        self.vBoxLayout1.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout1.setSpacing(0)
        self.vBoxLayout1.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout1.addWidget(self.contentLabel1, 0, Qt.AlignVCenter)
        self.vBoxLayout1.setAlignment(Qt.AlignVCenter)

        self.vBoxLayout2 = QVBoxLayout()
        self.vBoxLayout2.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout2.setSpacing(0)
        self.vBoxLayout2.addWidget(self.contentLabel2, 0, Qt.AlignVCenter)
        self.vBoxLayout2.setAlignment(Qt.AlignRight)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(16)
        self.hBoxLayout.addWidget(self.image)
        self.hBoxLayout.addLayout(self.vBoxLayout1)
        self.hBoxLayout.addStretch(5)
        self.hBoxLayout.addLayout(self.vBoxLayout2)
        self.hBoxLayout.addStretch(0)
        self.hBoxLayout.addWidget(self.mainButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

    def setTitle(self, text: str):
        """
        设置标题
        :param text: 文本
        """
        self.titleLabel.setText(text)

    def setImg(self, path: str, url: str = None, thread_pool: ThreadPoolExecutor = None):
        """
        设置图片
        :param path: 路径
        :param url: 链接
        :param thread_pool: 线程池
        """
        self.image.setImg(path, url, thread_pool)

    def setText(self, data: str, pos: int):
        """
        设置文本
        :param data: 文本
        :param pos: 位置：0 左上 1 左下 2 右上 3 右下
        """
        self._text[pos] = zb.clearCharacters(data)
        self.contentLabel1.setText(f"{self._text[0]}\n{self._text[1]}".strip())
        self.contentLabel2.setText(f"{self._text[2]}\n{self._text[3]}".strip())

        self.contentLabel1.adjustSize()


class CardGroup(QWidget):
    cardCountChanged = Signal(int)

    @functools.singledispatchmethod
    def __init__(self, parent: QWidget = None):
        """
        卡片组
        :param parent:
        """
        super().__init__(parent=parent)
        self._cards = []

        self._cardMap = {}

        self.titleLabel = StrongBodyLabel(self)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(5)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(12)

    @__init__.register
    def _(self, title: str = None, parent: QWidget = None):
        self.__init__(parent)
        if title:
            self.titleLabel.setText(title)

    def addCard(self, card: QWidget, wid: str | int, pos: int = -1):
        """
        添加卡片
        :param card: 卡片组件
        :param wid: 卡片组件id（不要重复！）
        :param pos: 卡片放置位置索引（正数0开始，倒数-1开始）
        """
        if pos >= 0:
            pos += 1
        self.vBoxLayout.insertWidget(pos, card, 0, Qt.AlignmentFlag.AlignTop)
        self._cards.append(card)
        self._cardMap[wid] = card

    def removeCard(self, wid: str | int):
        """
        移除卡片
        :param wid: 卡片组件id
        """
        if wid not in self._cardMap:
            return

        card = self._cardMap.pop(wid)
        self._cards.remove(card)
        self.vBoxLayout.removeWidget(card)
        card.hide()
        card.deleteLater()

        self.cardCountChanged.emit(self.count())

    def getCard(self, wid: str | int):
        """
        寻找卡片
        :param wid: 卡片组件id
        :return: 卡片组件
        """
        return self._cardMap.get(wid)

    def count(self):
        """
        卡片数量
        :return: 卡片数量
        """
        return len(self._cards)

    def clearCard(self):
        """
        清空卡片
        """
        while self._cardMap:
            self.removeCard(next(iter(self._cardMap)))

    def setTitle(self, text: str):
        """
        设置标题
        :param text: 文本
        """
        self.titleLabel.setText(text)

    def setShowTitle(self, enabled: bool):
        """
        是否展示标题
        :param enabled: 是否
        """
        self.titleLabel.setHidden(not enabled)
