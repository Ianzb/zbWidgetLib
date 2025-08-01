from concurrent.futures import ThreadPoolExecutor

from .base import *
from .page import *


def setToolTip(widget, text: str):
    widget.setToolTip(text)
    widget.installEventFilter(ToolTipFilter(widget, 1000))


class StatisticsWidget(QWidget):

    def __init__(self, title: str, value: str, parent=None, select_text: bool = False):
        """
        两行信息组件
        :param title: 标题
        :param value: 值
        """
        super().__init__(parent=parent)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = BodyLabel(value, self)

        if select_text:
            self.titleLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.valueLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(16, 0, 16, 0)
        self.vBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignBottom)

        setFont(self.valueLabel, 18, QFont.Weight.DemiBold)
        self.titleLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))

    def getTitle(self):
        """
        获取标题
        :return: 标题
        """
        return self.titleLabel.text()

    def title(self):
        """
        获取标题
        :return: 标题
        """
        return self.getTitle()

    def setTitle(self, title: str):
        """
        设置标题
        :param title: 标题
        """
        self.titleLabel.setText(title)

    def getValue(self):
        """
        获取值
        :return: 值
        """
        return self.valueLabel.text()

    def value(self):
        """
        获取值
        :return: 值
        """
        return self.getValue()

    def setValue(self, value: str):
        """
        设置值
        :param value: 值
        """
        self.valueLabel.setText(value)


class Image(QLabel):
    def __init__(self, parent=None):
        """
        图片组件
        """
        super().__init__(parent=parent)
        self.setFixedSize(48, 48)
        self.setScaledContents(True)

    def setImg(self, path: str):
        """
        设置图片
        :param path: 路径
        :param url: 链接
        :param thread_pool: 下载线程池
        """
        self.loading = False
        self.setPixmap(QPixmap(path))


class WebImage(QLabel):
    downloadFinishedSignal = pyqtSignal(bool)

    @functools.singledispatchmethod
    def __init__(self, parent=None):
        """
        图片组件（可实时下载）
        """
        super().__init__(parent=parent)
        self.setFixedSize(48, 48)
        self.setScaledContents(True)
        self.loading = False
        self.downloadFinishedSignal.connect(self.downloadFinished)

    @__init__.register
    def _(self, path: str, url: str = None, parent=None, thread_pool: ThreadPoolExecutor = None):
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
    def _(self, path: str, parent=None):
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

    def __init__(self, text: str, data_type: str = "", parent=None):
        """
        复制文本按钮
        :param text: 复制的文本
        :param data_type: 复制文本的提示信息，可以提示复制文本的内容类型
        :param parent: 父组件
        """
        super().__init__(FIF.COPY, parent)
        self._text = text
        self._data_type = data_type
        self.clicked.connect(self.copyButtonClicked)
        if self._data_type is None:
            self._data_type = ""
        self.setData(self._text, self._data_type)

    def setData(self, text: str, data_type: str = ""):
        """
        设置信息
        :param text: 复制的文本
        :param data_type: 复制文本的提示信息，可以提示复制文本的内容类型
        :return:
        """
        if not text:
            self.setEnabled(False)
            return
        self._text = text
        self._data_type = data_type

        setToolTip(self, f"点击复制{self._data_type}信息！")

    def getText(self):
        """
        复制的文本
        :return: 复制的文本
        """
        return self._text

    def text(self):
        """
        复制的文本
        :return: 复制的文本
        """
        return self.getText()

    def setText(self, text: str):
        """
        设置复制的文本
        :param text: 复制的文本
        """
        self.setData(text)

    def dataType(self):
        return self._data_type

    def getDataType(self):
        return self.dataType()

    def setDataType(self, data_type: str):
        """
        设置复制文本的提示信息
        :param data_type: 复制文本的提示信息
        """
        self.setData(self.text(), data_type)

    def copyButtonClicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self._text)


class DisplayCard(ElevatedCardWidget):

    def __init__(self, parent=None):
        """
        大图片卡片
        """
        super().__init__(parent)
        self.setFixedSize(168, 176)

        self.widget = WebImage(self)

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

    def getText(self):
        """
        设置文本
        :return: 文本
        """
        return self.bodyLabel.text()

    def text(self):
        """
        设置文本
        :return: 文本
        """
        return self.getText()

    def setDisplay(self, widget):
        """
        设置展示组件
        :param widget: 组件
        """
        self.widget = widget
        self.vBoxLayout.replaceWidget(self.vBoxLayout.itemAt(1).widget(), self.widget)


class IntroductionCard(ElevatedCardWidget):

    def __init__(self, parent=None):
        """
        简介卡片
        """
        super().__init__(parent)
        self.setFixedSize(190, 200)

        self.image = WebImage(self)
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

    def getTitle(self):
        """
        设置标题
        :return: 文本
        """
        return self.titleLabel.text()

    def title(self):
        """
        设置标题
        :return: 文本
        """
        return self.getTitle()

    def setTitle(self, text: str):
        """
        设置标题
        :param text: 文本
        """
        self.titleLabel.setText(text)

    def getText(self):
        """
        设置标题
        :return: 文本
        """
        return self.bodyLabel.text()

    def text(self):
        """
        设置标题
        :return: 文本
        """
        return self.getText()

    def setText(self, text: str):
        """
        设置标题
        :param text: 文本
        """
        self.bodyLabel.setText(text)


class LoadingCard(DisplayCard):

    def __init__(self, parent=None, is_random: bool = True):
        """
        加载中卡片
        """
        super().__init__(parent)
        if is_random:
            self.progressRing = IndeterminateProgressRing()
        else:
            self.progressRing = ProgressRing()
        self.setDisplay(self.progressRing)
        self.setText("加载中...")

    def setVal(self, val: int):
        self.progressRing.setVal(val)

    def setProgress(self, val: int):
        self.setVal(val)

    def getVal(self):
        return self.progressRing.getVal()

    def getProgress(self):
        return self.getVal()


class GrayCard(QWidget):

    def __init__(self, title: str = None, parent=None, alignment: Qt.AlignmentFlag = Qt.AlignLeft):
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
            self.card.setStyleSheet("GrayCard > QFrame {background-color: rgba(25,25,25,0.5); border:1px solid rgba(20,20,20,0.15); border-radius: 10px}")
        else:
            self.card.setStyleSheet("GrayCard > QFrame {background-color: rgba(175,175,175,0.1); border:1px solid rgba(150,150,150,0.15); border-radius: 10px}")

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

    def __init__(self, parent=None, url: bool = True, tag: bool = True, data: bool = True, select_text: bool = False):
        """
        详细信息卡片
        :param url: 是否展示链接
        :param tag: 是否展示标签
        :param data: 是否展示数据
        """
        super().__init__(parent)
        self.setMinimumWidth(100)

        self.select_text = select_text

        self.backButton = TransparentToolButton(FIF.RETURN, self)
        self.backButton.move(8, 8)
        self.backButton.setMaximumSize(32, 32)

        self.image = WebImage(self)

        self.titleLabel = TitleLabel(self)

        self.mainButton = PrimaryPushButton("", self)
        self.mainButton.setFixedWidth(160)

        self.infoLabel = BodyLabel(self)
        self.infoLabel.setWordWrap(True)

        if select_text:
            self.titleLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.infoLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)

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

    def getTitle(self):
        """
        获取标题
        :return: 文本
        """
        return self.titleLabel.text()

    def title(self):
        """
        获取标题
        :return: 文本
        """
        return self.getTitle()

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

    def getInfo(self):
        """
        获取信息
        :return: 文本
        """
        return self.infoLabel.text()

    def info(self):
        """
        获取信息
        :return: 文本
        """
        return self.getInfo()

    def setInfo(self, data: str):
        """
        设置信息
        :param data: 文本
        """
        self.infoLabel.setText(data)

    def getText(self):
        """
        获取信息
        :return: 文本
        """
        return self.getInfo()

    def text(self):
        """
        获取信息
        :return: 文本
        """
        return self.getText()

    def setText(self, data: str):
        """
        设置信息
        :param data: 文本
        """
        self.setInfo(data)

    def getUrlFromIndex(self, index: int):
        """
        获取链接
        :param index: 索引
        :return: 链接
        """
        if index < 0 or index >= self.hBoxLayout2.count():
            return None
        button = self.hBoxLayout2.itemAt(index).widget()
        if isinstance(button, HyperlinkButton):
            return button.url
        return None

    def getUrl(self, index: int):
        """
        获取链接
        :param index: 索引
        :return: 链接
        """
        return self.getUrlFromIndex(index)

    def getUrlIndexFromUrl(self, url: str):
        """
        获取链接索引
        :param url: 链接
        :return: 索引
        """
        for i in range(self.hBoxLayout2.count()):
            button = self.hBoxLayout2.itemAt(i).widget()
            if isinstance(button, HyperlinkButton) and button.getUrl() == url:
                return i
        return None

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

    def getDataFromTitle(self, title: str):
        """
        获取数据
        :param title: 标题
        :return: 数据
        """
        for i in range(self.hBoxLayout3.count()):
            widget = self.hBoxLayout3.itemAt(i).widget()
            if isinstance(widget, StatisticsWidget) and widget.titleLabel.text() == title:
                return widget.valueLabel.text()
        return None

    def getDataFromIndex(self, index: int):
        """
        获取数据
        :param index: 索引
        :return: 数据
        """
        if index < 0 or index >= self.hBoxLayout3.count():
            return None
        index = index * 2 - 2
        widget = self.hBoxLayout3.itemAt(index).widget()
        if isinstance(widget, StatisticsWidget):
            return widget.valueLabel.text()
        return None

    def getData(self, info: int | str):
        """
        获取数据
        :param info: 索引或标题
        :return: 数据
        """
        if isinstance(info, int):
            return self.getDataFromIndex(info)
        elif isinstance(info, str):
            return self.getDataFromTitle(info)

    def data(self, info: int | str):
        """
        获取数据
        :param info: 索引或标题
        :return: 数据
        """
        return self.getData(info)

    def addData(self, title: str, data: str | int):
        """
        添加数据
        :param title: 标题
        :param data: 数据
        """
        widget = StatisticsWidget(title, str(data), self, self.select_text)
        if self.hBoxLayout3.count() >= 1:
            seperator = VerticalSeparator(widget)
            seperator.setMinimumHeight(50)
            self.hBoxLayout3.addWidget(seperator)
        self.hBoxLayout3.addWidget(widget)

    def removeDataFromTitle(self, title: str):
        """
        移除数据
        :param title: 标题
        """
        for i in range(self.hBoxLayout3.count()):
            widget = self.hBoxLayout3.itemAt(i).widget()
            if isinstance(widget, StatisticsWidget) and widget.titleLabel.text() == title:
                self.hBoxLayout3.removeWidget(widget)
                widget.deleteLater()
                if i > 0:
                    seperator = self.hBoxLayout3.itemAt(i - 1).widget()
                    if isinstance(seperator, VerticalSeparator):
                        self.hBoxLayout3.removeWidget(seperator)
                        seperator.deleteLater()
                break

    def removeDataFromIndex(self, index: int):
        """
        移除数据
        :param index: 索引
        """
        if index < 0 or index >= self.hBoxLayout3.count():
            return
        index = index * 2 - 2
        widget = self.hBoxLayout3.itemAt(index).widget()
        if isinstance(widget, StatisticsWidget):
            self.hBoxLayout3.removeWidget(widget)
            widget.deleteLater()
            if index > 0:
                seperator = self.hBoxLayout3.itemAt(index - 1).widget()
                if isinstance(seperator, VerticalSeparator):
                    self.hBoxLayout3.removeWidget(seperator)
                    seperator.deleteLater()

    def removeData(self, info: int | str):
        if isinstance(info, int):
            self.removeDataFromIndex(info)
        elif isinstance(info, str):
            self.removeDataFromTitle(info)

    def getTagFromIndex(self, index: int):
        """
        获取标签
        :param index: 索引
        :return: 标签
        """
        if index < 0 or index >= self.hBoxLayout4.count():
            return None
        button = self.hBoxLayout4.itemAt(index).widget()
        if isinstance(button, PillPushButton):
            return button.text()
        return None

    def getTag(self, index: int):
        """
        获取标签
        :param index: 索引
        :return: 标签
        """
        return self.getTagFromIndex(index)

    def tag(self, index: int):
        """
        获取标签
        :param index: 索引
        :return: 标签
        """
        return self.getTagFromIndex(index)

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

    def __init__(self, parent=None, select_text: bool = False):
        """
        普通信息卡片（搜索列表展示）
        """
        super().__init__(parent)
        self.setMinimumWidth(100)
        self.setFixedHeight(73)

        self.image = WebImage(self)

        self.titleLabel = BodyLabel(self)

        self._text = ["", "", "", ""]
        self.contentLabel1 = CaptionLabel(f"{self._text[0]}\n{self._text[1]}", self)
        self.contentLabel1.setTextColor("#606060", "#d2d2d2")
        self.contentLabel1.setAlignment(Qt.AlignLeft)

        self.contentLabel2 = CaptionLabel(f"{self._text[2]}\n{self._text[3]}", self)
        self.contentLabel2.setTextColor("#606060", "#d2d2d2")
        self.contentLabel2.setAlignment(Qt.AlignRight)

        if select_text:
            self.titleLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.contentLabel1.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.contentLabel2.setTextInteractionFlags(Qt.TextSelectableByMouse)

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

    def getText(self, pos: int):
        """
        获取文本
        :param pos: 位置：0 左上 1 左下 2 右上 3 右下
        :return: 文本
        """
        return self._text[pos]

    def text(self, pos: int):
        """
        获取文本
        :param pos: 位置：0 左上 1 左下 2 右上 3 右下
        :return: 文本
        """
        return self.getText(pos)

    def setText(self, data: str, pos: int):
        """
        设置文本
        :param data: 文本
        :param pos: 位置：0 左上 1 左下 2 右上 3 右下
        """
        self._text[pos] = zb.clearEscapeCharaters(data)
        self.contentLabel1.setText(f"{self._text[0]}\n{self._text[1]}".strip())
        self.contentLabel2.setText(f"{self._text[2]}\n{self._text[3]}".strip())

        self.contentLabel1.adjustSize()


class CardGroup(QWidget):
    cardCountChanged = pyqtSignal(int)

    @functools.singledispatchmethod
    def __init__(self, parent=None):
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
    def _(self, title: str = None, parent=None):
        self.__init__(parent)
        if title:
            self.titleLabel.setText(title)

    def addCard(self, card, wid: str | int, pos: int = -1):
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

    def card(self, wid: str | int):
        """
        寻找卡片
        :param wid: 卡片组件id
        :return: 卡片组件
        """
        return self.getCard(wid)

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

    def getTitle(self):
        """
        获取标题
        :return: 文本
        """
        return self.titleLabel.text()

    def title(self):
        """
        获取标题
        :return: 文本
        """
        return self.getTitle()

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


class FileChooser(QFrame):
    fileChoosedSignal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mode = "file"
        self.only_one = True
        self.suffixs = {}
        self.show_suffixs = False
        self.default_path = None
        self.description = None
        self._drag = False

        self.setFixedSize(150, 115)

        self.vBoxLayout = QVBoxLayout(self)

        self.label1 = BodyLabel("拖拽文件到框内", self)
        self.label1.setWordWrap(True)
        self.label1.setAlignment(Qt.AlignCenter)

        self.label2 = BodyLabel("或者", self)
        self.label2.setAlignment(Qt.AlignCenter)

        self.chooseFileButton = HyperlinkButton(self)
        self.chooseFileButton.setText("浏览文件")
        self.chooseFileButton.clicked.connect(self.chooseFileButtonClicked)

        self.vBoxLayout.addWidget(self.label1, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.label2, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.chooseFileButton, Qt.AlignCenter)

        self.setLayout(self.vBoxLayout)

        self.setTheme()
        qconfig.themeChanged.connect(self.setTheme)

        self.setAcceptDrops(True)

    def setTheme(self):
        if isDarkTheme():
            if self._drag:
                self.setStyleSheet(".FileChooser {border: 2px rgb(121, 121, 121); border-style: dashed; border-radius: 6px; background-color: rgba(100, 100, 100, 0.5)}")
            else:
                self.setStyleSheet(".FileChooser {border: 2px rgb(121, 121, 121); border-style: dashed; border-radius: 6px; background-color: rgba(121, 121, 121, 0)}")
        else:
            if self._drag:
                self.setStyleSheet(".FileChooser {border: 2px rgb(145, 145, 145); border-style: dashed; border-radius: 6px; background-color: rgba(220, 220, 220, 0.5)}")
            else:
                self.setStyleSheet(".FileChooser {border: 2px rgb(145, 145, 145); border-style: dashed; border-radius: 6px; background-color: rgba(145, 145, 145, 0)}")

    def chooseFileButtonClicked(self):
        text = f"浏览{f"文件{"夹" if self.mode == "folder" else ""}" if not self.description else self.description}"
        if self.mode == "file":
            suffixs = ";;".join([f"{k} ({" ".join(["*" + i.lower() for i in v])})" for k, v in self.suffixs.items()])
            if self.only_one:
                file_name, _ = QFileDialog.getOpenFileName(self, text, self.default_path if self.default_path else "C:/", suffixs)
                file_name = [file_name]
            else:
                file_name, _ = QFileDialog.getOpenFileNames(self, text, self.default_path if self.default_path else "C:/", suffixs)
        elif self.mode == "folder":
            file_name = QFileDialog.getExistingDirectory(self, text, self.default_path if self.default_path else "C:/")
            file_name = [file_name]
        else:
            return
        if len(file_name) == 0:
            return
        self.fileChoosedSignal.emit(file_name)

    def _checkDragFile(self, urls):
        if len(urls) == 0:
            return False
        if self.mode == "file":
            if self.only_one:
                if len(urls) > 1:
                    return False
            if all(zb.isFile(i) for i in urls):
                suffixs = []
                for i in [[i.lower() for i in v] for v in self.suffixs.values()]:
                    suffixs.extend(i)
                if all(zb.getFileSuffix(i).lower() in suffixs for i in urls):
                    return True
                else:
                    return False
            else:
                return False
        elif self.mode == "folder":
            if self.only_one:
                if len(urls) > 1:
                    return False
            if all(zb.isDir(i) for i in urls):
                return True
            else:
                return False
        else:
            return False

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = [i.toLocalFile() for i in event.mimeData().urls()]
            if self._checkDragFile(urls):
                event.acceptProposedAction()
                self._drag = True
                self.label1.setText(f"松开即可选择")
                self.label2.hide()
                self.setTheme()

    def dragLeaveEvent(self, event):
        self._setText()
        self._drag = False
        self.setTheme()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = [i.toLocalFile() for i in event.mimeData().urls()]
            if self._checkDragFile(urls):
                self.fileChoosedSignal.emit(urls)
                self._setText()
                self._drag = False
                self.setTheme()

    def _setText(self):
        self.label1.setText(f"拖拽{", ".join([", ".join(v).replace(".", "").upper() for k, v in self.suffixs.items()]) if self.show_suffixs and self.mode == "file" else ""}{f"文件{"夹" if self.mode == "folder" else ""}" if not self.description else self.description}到框内")
        self.label2.show()
        self.chooseFileButton.setText(f"浏览{f"文件{"夹" if self.mode == "folder" else ""}" if not self.description else self.description}")

    def getMode(self):
        """
        获取文件选择器模式
        :return: "file" or "folder"
        """
        return self.mode

    def setMode(self, mode: str = "file"):
        """
        设置文件选择器模式
        :param mode: "file" or "folder"
        """
        self.mode = mode
        self._setText()

    def getDescription(self):
        """
        获取文件选择器描述
        :return: str
        """
        return self.description

    def setDescription(self, description: str):
        """
        设置文件选择器描述
        :param description: 描述
        """
        self.description = description
        self._setText()

    def isOnlyOne(self):
        """
        获取是否只选择一个文件
        """
        return self.only_one

    def setOnlyOne(self, only_one: bool):
        """
        设置是否只选择一个文件
        """
        self.only_one = only_one

    def getDefaultPath(self):
        """
        获取默认路径
        :return: str
        """
        return self.default_path

    def setDefaultPath(self, path: str):
        """
        设置默认路径
        :param path: 默认路径
        """
        self.default_path = path

    def getShowSuffixs(self):
        """
        获取是否在文本中显示后缀
        :return: bool
        """
        return self.show_suffixs

    def setShowSuffixs(self, show_suffixs: bool):
        """
        设置是否在文本中显示后缀
        """
        self.show_suffixs = show_suffixs
        self._setText()

    def getSuffix(self):
        """
        获取文件选择器后缀
        """
        return self.suffixs

    def setSuffix(self, suffixs: dict):
        """
        设置文件选择器后缀
        :param suffixs: 后缀字典，格式如{"Word文档":[".doc",".docx"],"Excel表格":[".xls",".xlsx"],"PDF文档":[".pdf"]}
        """
        self.suffixs = suffixs
        self._setText()

    def addSuffix(self, suffix: dict):
        """
        添加文件选择器后缀
        :param suffix: 后缀字典，格式如{"Word文档":[".doc",".docx"],"Excel表格":[".xls",".xlsx"],"PDF文档":[".pdf"]}
        """
        self.suffixs.update(suffix)
        self._setText()

    def clearSuffix(self):
        """
        清除文件选择器后缀
        """
        self.suffixs = {}
        self._setText()


class LoadingMessageBox(MaskDialogBase):
    def __init__(self, parent=None, is_random: bool = True):
        super().__init__(parent=parent)

        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)
        self.vBoxLayout = QVBoxLayout(self.widget)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(16, 16, 16, 16)

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))

        if is_random:
            self.progressRing = IndeterminateProgressRing()
        else:
            self.progressRing = ProgressRing()
        self.loadingCard = DisplayCard(self.widget)
        setattr(self.loadingCard, "_normalBackgroundColor", lambda: QColor(16, 16, 16, 220) if isDarkTheme() else QColor(255, 255, 255, 220))
        setattr(self.loadingCard, "_hoverBackgroundColor", lambda: QColor(16, 16, 16, 255) if isDarkTheme() else QColor(255, 255, 255, 255))
        setattr(self.loadingCard, "_pressedBackgroundColor", lambda: QColor(16, 16, 16, 110) if isDarkTheme() else QColor(255, 255, 255, 110))
        self.loadingCard.setBackgroundColor(QColor(16, 16, 16, 220) if isDarkTheme() else QColor(255, 255, 255, 220))

        self.loadingCard.setDisplay(self.progressRing)
        self.vBoxLayout.addWidget(self.loadingCard, 1)

    def setVal(self, val: int):
        self.progressRing.setVal(val)

    def setProgress(self, val: int):
        self.setVal(val)

    def getVal(self):
        return self.progressRing.getVal()

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
