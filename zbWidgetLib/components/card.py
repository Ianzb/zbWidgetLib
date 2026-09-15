from ..base import *
from .image import *
from .widget import StatisticsWidget


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
        self.hBoxLayout.setSpacing(4)
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


class FlowGrayCard(QWidget):

    def __init__(self, title: str = None, parent=None):
        """
        流式布局灰色背景组件卡片
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

        self.flowLayout = FlowLayout(self.card)
        self.flowLayout.setSpacing(4)
        self.flowLayout.setContentsMargins(12, 12, 12, 12)

        self.setTheme()
        qconfig.themeChanged.connect(self.setTheme)

    def setTheme(self):
        if isDarkTheme():
            self.card.setStyleSheet("FlowGrayCard > QFrame {background-color: rgba(25,25,25,0.5); border:1px solid rgba(20,20,20,0.15); border-radius: 10px}")
        else:
            self.card.setStyleSheet("FlowGrayCard > QFrame {background-color: rgba(175,175,175,0.1); border:1px solid rgba(150,150,150,0.15); border-radius: 10px}")

    def addWidget(self, widget):
        """
        添加组件
        :param widget: 组件
        :param spacing: 间隔
        :param alignment: 对齐方式
        """
        self.flowLayout.addWidget(widget)

    def insertWidget(self, index: int, widget):
        """
        插入组件
        :param index: 序号
        :param widget: 组件
        :param alignment: 对齐方式
        """
        self.flowLayout.insertWidget(index, widget)


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
            self.titleLabel.setSelectable()
            self.infoLabel.setSelectable()

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
            self.titleLabel.setSelectable()
            self.contentLabel1.setSelectable()
            self.contentLabel2.setSelectable()

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

        # 滚动内容尺寸同步定时器（零毫秒单发）：把同一事件循环内的多次触发
        # （卡片增删 / 换行 / 视口变化）合并为一次同步
        self._scrollSyncTimer = QTimer(self)
        self._scrollSyncTimer.setSingleShot(True)
        self._scrollSyncTimer.setInterval(0)
        self._scrollSyncTimer.timeout.connect(self._syncScrollContentSize)

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

    def addCard(self, card, wid: str | int = None, pos: int = -1):
        """
        添加卡片
        :param card: 卡片组件
        :param wid: 卡片组件id（默认使用card）
        :param pos: 卡片放置位置索引（0 表示插在最前，-1 表示追加到末尾）
        """
        if not wid:
            wid = hex(id(card))
        if wid in self._cardMap:
            raise KeyError
        if pos >= 0 and self.show_title:
            # 有标题时索引 0/1 被标题与间距占用，调用方给的位置相对第一张卡
            pos += 2
        self.boxLayout.insertWidget(pos, card, 0, Qt.AlignmentFlag.AlignTop)
        self._cards.append(card)
        self._cardMap[wid] = card
        self.cardCountChanged.emit(self.count())
        return wid

    # ------------------------------------------------------------------
    # 滚动内容尺寸同步
    # ------------------------------------------------------------------

    def event(self, e):
        """布局失效时安排一次滚动内容尺寸同步。

        卡片因文字换行 / 增删而高度变化时，承载滚动区的 ``widgetResizable``
        只在自身 resize / setWidget 等少数时机重算内容尺寸，会错过内容 sizeHint
        的变化，导致垂直滚动范围停留在旧值（底部卡片滚不到 / 列表底部留白）。
        """
        if e.type() == QEvent.Type.LayoutRequest:
            self._scrollSyncTimer.start()
        return super().event(e)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._scrollSyncTimer.start()

    def _owningScrollArea(self):
        """向上查找承载本组件的 QScrollArea（直接放在页面里时返回 None）。"""
        parent = self.parentWidget()
        while parent is not None and not isinstance(parent, QScrollArea):
            parent = parent.parentWidget()
        return parent

    def _syncScrollContentSize(self):
        """把所在滚动区的内容 widget 尺寸同步为 max(视口, 内容实际高度)。

        - 宽度取 max(视口宽, 内容最小宽)。**不用 sizeHint 的宽度**：开启换行的
          标签其 sizeHint 宽度与视口无关（按自适应比例给出），用它会把内容撑到
          比视口宽，重新引入横向滚动；
        - 高度优先走 ``hasHeightForWidth`` 链（换行内容在当前宽度下的真实高度；
          Qt 会沿 QWidget 容器与布局透传该标记），再与视口高取大。
        """
        scroll = self._owningScrollArea()
        if scroll is None or not scroll.widgetResizable():
            return
        content = scroll.widget()
        if content is None:
            return
        viewport = scroll.viewport()
        minimum = content.minimumSizeHint()
        width = max(viewport.width(), minimum.width())
        layout = content.layout()
        if layout is not None and layout.hasHeightForWidth():
            height = layout.totalHeightForWidth(width)
        else:
            height = max(content.sizeHint().height(), minimum.height())
        height = max(height, viewport.height())
        if content.size() == QSize(width, height):
            return
        content.resize(width, height)
        try:
            scroll.updateScrollBars()
        except Exception:
            pass

    def addWidget(self, card, wid: str | int = None, pos: int = -1):
        """
        添加卡片
        :param card: 卡片组件
        :param wid: 卡片组件id（默认使用card）
        :param pos: 卡片放置位置索引（正数0开始，倒数-1开始）
        """
        self.addCard(card, wid, pos)

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
        return wid

    def removeWidget(self, wid: int | str):
        """
        移除卡片
        :param wid: 卡片组件id
        """
        self.removeCard(wid)

    def getCard(self, wid: str | int):
        """
        寻找卡片
        :param wid: 卡片组件id
        :return: 卡片组件
        """
        return self._cardMap.get(wid)

    def getWidget(self, wid: str | int):
        """
        寻找卡片
        :param wid: 卡片组件id
        :return: 卡片组件
        """
        self.getCard(wid)

    def getCards(self):
        """
        获取卡片
        :return:
        """
        return self._cards

    def getWidgets(self):
        """
        获取卡片
        :return:
        """
        return self.getCards()

    def getWids(self):
        """
        获取组件id
        :return:
        """
        return list(self._cardMap.keys())

    def getCardMap(self):
        """
        获取wid卡片映射表
        :return:
        """
        return self._cardMap

    def getWidgetMap(self):
        """
        获取wid卡片映射表
        :return:
        """
        return self.getCardMap()

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

    def clearWidget(self):
        """
        清空卡片
        """
        self.clearCard()

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


WidgetGroup = CardGroup


class FlowCardGroup(QWidget):
    cardCountChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        """
        卡片组
        :param parent:
        :param show_title: 是否显示标题
        :param is_v: 是否竖向排列
        """
        super().__init__(parent=parent)
        self._cards = []
        self._cardMap = {}

        self.flowLayout = FlowLayout(self)
        self.flowLayout.setSpacing(5)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.vBoxLayout = self.flowLayout
        self.hBoxLayout = self.flowLayout

    def addCard(self, card, wid: str | int = None, pos: int = -1):
        """
        添加卡片
        :param card: 卡片组件
        :param wid: 卡片组件id（默认使用card）
        :param pos: 卡片放置位置索引（正数0开始，倒数-1开始）
        """
        if not wid:
            wid = hex(id(card))
        if wid in self._cardMap:
            raise KeyError
        if pos == -1:
            pos = len(self._cardMap)
        elif pos < -1:
            pos += 1
        if pos > len(self._cardMap):
            pos = len(self._cardMap)
        self.flowLayout.insertWidget(pos, card)
        self._cards.append(card)
        self._cardMap[wid] = card
        self.cardCountChanged.emit(self.count())
        return wid

    def addWidget(self, card, wid: str | int = None, pos: int = -1):
        """
        添加卡片
        :param card: 卡片组件
        :param wid: 卡片组件id（默认使用card）
        :param pos: 卡片放置位置索引（正数0开始，倒数-1开始）
        """
        self.addCard(card, wid, pos)

    def removeCard(self, wid: str | int):
        """
        移除卡片
        :param wid: 卡片组件id
        """
        if wid not in self._cardMap:
            return

        card = self._cardMap.pop(wid)
        self._cards.remove(card)
        self.flowLayout.removeWidget(card)
        card.hide()
        card.deleteLater()

        self.cardCountChanged.emit(self.count())
        return wid

    def removeWidget(self, wid: str | int):
        """
        移除卡片
        :param wid: 卡片组件id
        """
        self.removeCard(wid)

    def getCard(self, wid: str | int):
        """
        寻找卡片
        :param wid: 卡片组件id
        :return: 卡片组件
        """
        return self._cardMap.get(wid)

    def getWidget(self, wid: str | int):
        """
        寻找卡片
        :param wid: 卡片组件id
        :return: 卡片组件
        """
        self.getCard(wid)

    def getCards(self):
        """
        获取卡片
        :return:
        """
        return self._cards

    def getWidgets(self):
        """
        获取卡片
        :return:
        """
        return self.getCards()

    def getWids(self):
        """
        获取组件id
        :return:
        """
        return list(self._cardMap.keys())

    def getCardMap(self):
        """
        获取wid卡片映射表
        :return:
        """
        return self._cardMap

    def getWidgetMap(self):
        """
        获取wid卡片映射表
        :return:
        """
        self.getCardMap()

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

    def clearWidget(self):
        """
        清空卡片
        """
        self.clearCard()


FlowWidgetGroup = FlowCardGroup
