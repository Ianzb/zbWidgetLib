from concurrent.futures import ThreadPoolExecutor

from .base import *
from .page import *


def setToolTip(widget, text: str):
    widget.setToolTip(text)
    widget.installEventFilter(AcrylicToolTipFilter(widget, 1000))


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
        self.tagButton.setFixedHeight(32)
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
    def __init__(self, parent=None, show_title: bool = False, is_v: bool = True):
        """
        卡片组
        :param parent:
        :param show_title: 是否显示标题
        :param is_v: 是否竖向排列
        """
        super().__init__(parent=parent)
        self.show_title = show_title
        self.is_v = is_v
        self._cards = []
        self._cardMap = {}

        if show_title:
            self.titleLabel = StrongBodyLabel(self)
        if self.is_v:
            self.boxLayout = QVBoxLayout(self)
        else:
            self.boxLayout = QHBoxLayout(self)
        self.boxLayout.setSpacing(5)
        self.boxLayout.setContentsMargins(0, 0, 0, 0)
        self.boxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        if show_title:
            self.boxLayout.addWidget(self.titleLabel)
            self.boxLayout.addSpacing(12)

        self.vBoxLayout = self.boxLayout
        self.hBoxLayout = self.boxLayout

    @__init__.register
    def _(self, title: str, parent=None, is_v: bool = True):
        """
        卡片组
        :param title: 标题文本
        :param parent:
        :param is_v: 是否竖向排列
        """
        self.__init__(parent, True, is_v)
        if title and self.show_title:
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
        self.boxLayout.insertWidget(pos, card, 0, Qt.AlignmentFlag.AlignTop)
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
        self.boxLayout.removeWidget(card)
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
        self.loadingCard.setText("加载中...")
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


class SaveFilePushButton(PushButton):
    fileChoosedSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.suffixs = {}
        self.default_path = None
        self.description = None

        self.setText("导出")

        self.clicked.connect(self.clickEvent)

    def clickEvent(self):
        text = f"浏览{f"文件" if not self.description else self.description}"
        suffixs = ";;".join([f"{k} ({" ".join(["*" + i.lower() for i in v])})" for k, v in self.suffixs.items()])
        file_name, _ = QFileDialog.getSaveFileName(self, text, self.default_path if self.default_path else "C:/", suffixs)
        if file_name:
            self.fileChoosedSignal.emit(file_name)

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
        self.setText(f"导出{description}")

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

    def addSuffix(self, suffix: dict):
        """
        添加文件选择器后缀
        :param suffix: 后缀字典，格式如{"Word文档":[".doc",".docx"],"Excel表格":[".xls",".xlsx"],"PDF文档":[".pdf"]}
        """
        self.suffixs.update(suffix)

    def clearSuffix(self):
        """
        清除文件选择器后缀
        """
        self.suffixs = {}


class SaveFilePrimaryPushButton(PrimaryPushButton):
    fileChoosedSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.suffixs = {}
        self.default_path = None
        self.description = None

        self.setText("导出")

        self.clicked.connect(self.clickEvent)

    def clickEvent(self):
        text = f"浏览{f"文件" if not self.description else self.description}"
        suffixs = ";;".join([f"{k} ({" ".join(["*" + i.lower() for i in v])})" for k, v in self.suffixs.items()])
        file_name, _ = QFileDialog.getSaveFileName(self, text, self.default_path if self.default_path else "C:/", suffixs)
        if file_name:
            self.fileChoosedSignal.emit(file_name)

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
        self.setText(f"导出{description}")

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

    def addSuffix(self, suffix: dict):
        """
        添加文件选择器后缀
        :param suffix: 后缀字典，格式如{"Word文档":[".doc",".docx"],"Excel表格":[".xls",".xlsx"],"PDF文档":[".pdf"]}
        """
        self.suffixs.update(suffix)

    def clearSuffix(self):
        """
        清除文件选择器后缀
        """
        self.suffixs = {}


class PageSpliter(QWidget):
    pageChanged = pyqtSignal(int, int, int)  # 信号：当前页码, 页面长度, 起始编号(0开始)

    def __init__(self, parent=None, max_page: int = 10, max_visible: int = 10, length: int = 10,
                 preset_length: list = None, max_length: int = 100, total_count: int = 0,
                 show_max: bool = True, show_jump_input: bool = True, show_length_input: bool = True):
        """
        分页器组件，通过pageChanged绑定页面修改事件

        :param parent: 父组件
        :param max_page: 最大页码（当total_count>0时会被覆盖）
        :param max_visible: 同时显示的分页按钮数量
        :param length: 每个页面的长度（项目数量）
        :param preset_length: 预设的页面长度选项列表
        :param max_length: 允许的最大页面长度
        :param total_count: 项目总数（用于自动计算最大页码）
        :param show_max: 是否显示最大页码
        :param show_jump_input: 是否显示页面跳转输入框
        :param show_length_input: 是否显示页面长度设置控件
        """
        super().__init__(parent)

        # 初始化默认值
        self.page = 0
        self._buttons = {}
        self.numberButtons = []

        # 处理预设长度参数
        if preset_length is None:
            preset_length = []
        else:
            # 过滤无效的预设长度值
            preset_length = [i for i in preset_length if 0 < i <= max_length]

        # 处理长度参数有效性
        if length <= 0:
            length = 1
        if length > max_length:
            length = max_length

        # 确保当前长度在预设列表中
        if preset_length and length not in preset_length:
            preset_length.append(length)
        preset_length = sorted(list(set(preset_length)))

        # 根据总数计算最大页码
        if total_count > 0:
            max_page = max(1, (total_count - 1) // length + 1)
        else:
            total_count = 0

        # 存储初始参数
        self.max_visible = max_visible
        self.max_page = max_page
        self.length = length
        self.preset_length = preset_length
        self.max_length = max_length
        self.total_count = total_count
        self.show_max = show_max
        self.show_jump_input = show_jump_input
        self.show_length_input = show_length_input

        # 创建UI组件
        self._create_ui_components()

        # 设置布局
        self._setup_layout()

        # 初始化状态
        self._initialize_state()

    def _create_ui_components(self):
        """创建所有UI组件"""
        # 创建布局
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(8)

        # 创建左右翻页按钮
        self.leftButton = TransparentToolButton(FIF.CARE_LEFT_SOLID, self)
        self.leftButton.clicked.connect(lambda: self.setPage(self.page - 1))

        self.rightButton = TransparentToolButton(FIF.CARE_RIGHT_SOLID, self)
        self.rightButton.clicked.connect(lambda: self.setPage(self.page + 1))

        # 页码按钮将在_adjustButtonCount中创建

        # 跳转页面相关控件
        self.label1 = BodyLabel("页", self)
        self.lineEdit1 = LineEdit(self)
        self.lineEdit1.setMaximumWidth(50)

        self.label2 = BodyLabel("/", self)
        self.label3 = BodyLabel(str(self.max_page), self)
        self.label4 = BodyLabel("页", self)

        # 页面长度相关控件
        self.lineEdit2 = LineEdit(self)
        self.lineEdit2.setText(str(self.length))
        self.lineEdit2.setMaximumWidth(50)

        self.label5 = BodyLabel("/", self)
        self.label6 = BodyLabel("页", self)

        self.comboBox = AcrylicComboBox(self)

    def _setup_layout(self):
        """设置布局并添加组件"""
        # 添加左右翻页按钮
        self.hBoxLayout.addWidget(self.leftButton, 0, Qt.AlignLeft)

        # 页码按钮将在_adjustButtonCount中添加

        # 添加右侧翻页按钮
        self.hBoxLayout.addWidget(self.rightButton, 0, Qt.AlignLeft)

        # 添加跳转页面控件
        self.hBoxLayout.addWidget(self.label1, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.lineEdit1, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.label2, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.label3, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.label4, 0, Qt.AlignLeft)

        # 添加间距
        self.hBoxLayout.addSpacing(8)

        # 添加页面长度控件
        self.hBoxLayout.addWidget(self.lineEdit2, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.label5, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.label6, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignLeft)

        # 设置布局居中
        self.hBoxLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.hBoxLayout)

    def _initialize_state(self):
        """初始化组件状态"""
        # 设置输入框验证器
        if self.max_page <= 0:
            self.lineEdit1.setValidator(QIntValidator(1, 1000))
            self.lineEdit2.setValidator(QIntValidator(1, 1000))
        else:
            self.lineEdit1.setValidator(QIntValidator(1, self.max_page))
            self.lineEdit2.setValidator(QIntValidator(1, self.max_length))

        # 设置输入框事件
        self.lineEdit1.returnPressed.connect(lambda: self.setPage(int(self.lineEdit1.text())))
        self.lineEdit2.returnPressed.connect(lambda: self.setLength(int(self.lineEdit2.text())))

        # 设置下拉框
        self.comboBox.addItems([str(i) + " / 页" for i in self.preset_length])
        self.comboBox.currentTextChanged.connect(lambda text: self.setLength(int(text[:-4] if text else 0)))

        # 设置控件可见性
        self.setShowMax(self.show_max)
        self.setShowJumpInput(self.show_jump_input)
        self.setShowLengthInput(self.show_length_input)

        # 调整按钮数量（基于max_visible和max_page）
        self._adjustButtonCount()

        # 设置初始页码（不发送信号）
        self.setPage(1, False)

    def _adjustButtonCount(self):
        """
        动态调整页码按钮数量
        - 计算实际需要显示的按钮数量：min(max_visible, max_page) 或 max_visible（当max_page未知时）
        - 删除多余的按钮或添加不足的按钮
        """
        # 计算实际需要显示的按钮数量
        display_count = self.max_visible
        if self.max_page > 0:  # 如果有最大页码限制
            display_count = min(self.max_visible, self.max_page)

        current_count = len(self.numberButtons)

        # 删除多余的按钮
        if current_count > display_count:
            for i in range(current_count - 1, display_count - 1, -1):
                btn = self.numberButtons.pop()
                self.hBoxLayout.removeWidget(btn)
                btn.deleteLater()

        # 添加不足的按钮
        if current_count < display_count:
            for i in range(current_count, display_count):
                btn = TransparentToggleToolButton(self)
                btn.clicked.connect(self._createButtonHandler(len(self.numberButtons)))
                self.numberButtons.append(btn)
                # 在右按钮之前插入新按钮
                index = self.hBoxLayout.indexOf(self.rightButton)
                self.hBoxLayout.insertWidget(index, btn, 0, Qt.AlignLeft)

        # 确保所有按钮都有正确的状态
        self._updateButtons()

    def _updateButtons(self):
        """更新所有页码按钮的状态（文本和选中状态）"""
        if not self.numberButtons:
            return

        # 计算起始页码
        if self.max_page <= 0:  # 当最大页码未知时
            start = max(1, self.page - self.max_visible // 2)
        else:
            # 确保页码范围在有效范围内
            start = max(1, min(self.page - self.max_visible // 2,
                               self.max_page - len(self.numberButtons) + 1))

        # 更新每个按钮
        for i, btn in enumerate(self.numberButtons):
            btn_num = start + i
            # 当页码在有效范围内时显示数字，否则隐藏按钮
            if self.max_page <= 0 or btn_num <= self.max_page:
                btn.setText(str(btn_num))
                btn.setVisible(True)
                btn.setChecked(btn_num == self.page)
            else:
                # 对于无效页码，隐藏按钮
                btn.setVisible(False)

    def setMaxVisible(self, max_visible: int):
        """
        设置最大可见按钮数量

        :param max_visible: 新的最大可见按钮数（至少为1）
        """
        if max_visible < 1:
            max_visible = 1
        if self.max_visible == max_visible:
            return

        self.max_visible = max_visible
        self._adjustButtonCount()  # 调整按钮数量
        self._updateButtons()  # 更新按钮状态

    def getMaxVisible(self):
        """
        获取最大可见按钮数量

        :return: 当前最大可见按钮数
        """
        return self.max_visible

    def _createButtonHandler(self, index):
        """创建页码按钮的点击处理函数"""

        def handler():
            if index < len(self.numberButtons):
                text = self.numberButtons[index].text()
                if text.isdigit():
                    self.setPage(int(text))

        return handler

    def setPage(self, page: int, signal: bool = True):
        """
        设置当前页码

        :param page: 新的页码（从1开始）
        :param signal: 是否发送pageChanged信号
        """
        # 如果页码未改变且不需要发送信号，则直接返回
        if self.page == page and not signal:
            return

        # 检查页码有效性
        if page < 1 or (self.max_page > 0 and page > self.max_page):
            return

        # 更新页码
        self.page = page

        # 更新翻页按钮状态
        self.leftButton.setEnabled(page > 1)
        self.rightButton.setEnabled(self.max_page <= 0 or page < self.max_page)

        # 更新页码按钮
        self._updateButtons()

        # 更新跳转输入框
        self.lineEdit1.setText(str(page))

        # 如果需要，发送信号
        if signal:
            self.pageChanged.emit(self.page, self.length, self.getNumber())

    def getPage(self):
        """
        获取当前页码

        :return: 当前页码
        """
        return self.page

    def getNumber(self):
        """
        获取当前页面第一个项目的编号（从0开始）

        :return: 起始项目编号
        """
        return (self.page - 1) * self.length

    def getLength(self):
        """
        获取页面长度（每页项目数）

        :return: 页面长度
        """
        return self.length

    def setLength(self, length: int, signal: bool = True):
        """
        设置页面长度（每页项目数）

        :param length: 新的页面长度
        :param signal: 是否发送pageChanged信号
        """
        # 检查长度有效性
        if length <= 0 or length > self.max_length:
            return

        # 更新长度
        self.length = length

        # 确保新长度在预设列表中
        if self.preset_length and length not in self.preset_length:
            self.addPresetLength(length)

        # 如果有总数，重新计算最大页码
        if self.total_count > 0:
            self.setMaxPage(max(1, (self.total_count - 1) // length + 1), False)

        # 更新UI
        self.lineEdit2.setText(str(length))
        self.comboBox.setCurrentText(f"{length} / 页")

        # 如果需要，发送信号
        if signal:
            self.pageChanged.emit(self.page, self.length, self.getNumber())

    def setMaxPage(self, max_page: int, signal: bool = True):
        """
        设置最大页码

        :param max_page: 新的最大页码
        :param signal: 是否发送pageChanged信号
        """
        # 更新最大页码
        self.max_page = max_page

        # 更新输入验证器
        if self.max_page <= 0:
            self.lineEdit1.setValidator(QIntValidator(1, 1000))
        else:
            self.lineEdit1.setValidator(QIntValidator(1, self.max_page))

        # 更新UI显示
        self.label2.setVisible(self.show_max and self.show_jump_input and self.max_page > 0)
        self.label3.setText(str(self.max_page))
        self.label3.setVisible(self.show_max and self.max_page > 0)
        self.label4.setVisible(self.show_max and self.max_page > 0)

        # 调整按钮数量
        self._adjustButtonCount()

        # 如果当前页码超过最大页码，调整到最后一页
        if 0 < self.max_page < self.page:
            self.setPage(self.max_page, signal)
        else:
            # 确保按钮状态更新
            self._updateButtons()
            if signal:
                self.pageChanged.emit(self.page, self.length, self.getNumber())

    def getMaxPage(self):
        """
        获取最大页码

        :return: 最大页码
        """
        return self.max_page

    def setShowMax(self, show_max: bool):
        """
        设置是否显示最大页码

        :param show_max: 是否显示
        """
        self.show_max = show_max
        self.label2.setVisible(self.show_max and self.show_jump_input and self.max_page > 0)
        self.label3.setVisible(self.show_max and self.max_page > 0)
        self.label4.setVisible(self.show_max and self.max_page > 0)

    def getShowMax(self):
        """
        获取是否显示最大页码

        :return: 是否显示
        """
        return self.show_max

    def setShowJumpInput(self, show_jump_input: bool):
        """
        设置是否显示跳转输入框

        :param show_jump_input: 是否显示
        """
        self.show_jump_input = show_jump_input
        self.label1.setVisible(self.show_jump_input)
        self.lineEdit1.setVisible(self.show_jump_input)
        self.label2.setVisible(self.show_max and self.show_jump_input and self.max_page > 0)

    def getShowJumpInput(self):
        """
        获取是否显示跳转输入框

        :return: 是否显示
        """
        return self.show_jump_input

    def setShowLengthInput(self, show_length_input: bool):
        """
        设置是否显示页面长度设置控件

        :param show_length_input: 是否显示
        """
        self.show_length_input = show_length_input
        # 根据是否有预设长度决定显示哪种控件
        self.lineEdit2.setVisible(self.show_length_input and not bool(self.preset_length))
        self.label5.setVisible(self.show_length_input and not bool(self.preset_length))
        self.label6.setVisible(self.show_length_input and not bool(self.preset_length))
        self.comboBox.setVisible(self.show_length_input and bool(self.preset_length))

    def getShowLengthInput(self):
        """
        获取是否显示页面长度设置控件

        :return: 是否显示
        """
        return self.show_length_input

    def setPresetLength(self, preset_length: list):
        """
        设置预设长度列表

        :param preset_length: 新的预设长度列表
        """
        # 过滤无效值
        if preset_length is None:
            preset_length = []
        else:
            preset_length = [i for i in preset_length if 0 < i <= self.max_length]

        # 确保当前长度在预设列表中
        if self.length not in preset_length and preset_length:
            preset_length.append(self.length)

        # 排序并去重
        self.preset_length = sorted(list(set(preset_length)))

        # 更新下拉框
        self.comboBox.blockSignals(True)
        self.comboBox.clear()
        self.comboBox.addItems([str(i) + " / 页" for i in self.preset_length])
        self.comboBox.setCurrentText(str(self.length) + " / 页")
        self.comboBox.blockSignals(False)

        # 更新控件可见性
        self.setShowLengthInput(self.show_length_input)

    def addPresetLength(self, preset_length: int | list):
        """
        添加预设长度

        :param preset_length: 要添加的长度值或列表
        """
        if isinstance(preset_length, int):
            self.setPresetLength(self.preset_length + [preset_length])
        elif isinstance(preset_length, list):
            self.setPresetLength(self.preset_length + preset_length)

    def removePresetLength(self, preset_length: int | list):
        """
        移除预设长度

        :param preset_length: 要移除的长度值或列表
        """
        if isinstance(preset_length, int):
            preset_length = [preset_length]

        # 创建副本并移除指定值
        old = self.preset_length.copy()
        for i in preset_length:
            if i in old:
                old.remove(i)

        self.setPresetLength(old)

    def getPresetLength(self):
        """
        获取预设长度列表

        :return: 预设长度列表
        """
        return self.preset_length

    def setMaxLength(self, max_length: int):
        """
        设置最大页面长度

        :param max_length: 新的最大长度
        """
        self.max_length = max_length

        # 调整当前长度
        if self.length > self.max_length:
            self.setLength(self.max_length)

        # 调整预设长度
        if self.preset_length:
            self.setPresetLength(self.preset_length)

        # 更新输入验证器
        if self.max_page <= 0:
            self.lineEdit2.setValidator(QIntValidator(1, 1000))
        else:
            self.lineEdit2.setValidator(QIntValidator(1, self.max_length))

    def getMaxLength(self):
        """
        获取最大页面长度

        :return: 最大长度
        """
        return self.max_length

    def setTotalCount(self, total_count: int):
        """
        设置项目总数（自动计算最大页码）

        :param total_count: 项目总数
        """
        self.total_count = total_count
        if self.total_count > 0:
            self.setMaxPage(max(1, (self.total_count - 1) // self.length + 1))
        else:
            self.total_count = 0

    def getTotalCount(self):
        """
        获取项目总数

        :return: 项目总数
        """
        return self.total_count
