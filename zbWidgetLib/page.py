from .base import *


class BetterScrollArea(SmoothScrollArea):
    def __init__(self, parent: QWidget = None):
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


class BasicPage(BetterScrollArea):
    title = ""
    subtitle = ""

    def __init__(self, parent: QWidget = None):
        """
        基本页面，包含标题和子标题，适用于基本页面，通过类变量修改title和subtitle设置标题和子标题。
        :param parent:
        """
        super().__init__(parent=parent)
        self.setObjectName(self.title)

        self.toolBar = ToolBar(self.title, self.subtitle, self)

        self.setViewportMargins(0, self.toolBar.height(), 0, 0)

        self._icon = None

    def setIcon(self, icon):
        """
        设置页面图标
        :param icon: 图标
        """
        self._icon = icon

    def icon(self):
        """
        获取页面图标
        :return: 图标
        """
        return self._icon

    def getIcon(self):
        """
        获取页面图标
        :return: 图标
        """
        return self._icon


class BasicTabPage(BasicPage):

    def __init__(self, parent: QWidget = None):
        """
        内置多标签页的页面，没有标题
        :param parent:
        """
        super().__init__(parent=parent)

        self.toolBar.deleteLater()

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.pivot = Pivot(self)

        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)

    def addPage(self, widget: QWidget, name: str = None):
        """
        添加标签页
        :param widget: 标签页对象，需设置icon属性为页面图标
        :param name: 名称
        """
        if not name:
            name = widget.objectName()
        widget.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(name, name, lambda: self.stackedWidget.setCurrentWidget(widget), widget.icon)
        if self.stackedWidget.count() == 1:
            self.stackedWidget.setCurrentWidget(widget)
            self.pivot.setCurrentItem(widget.objectName())

    def onCurrentIndexChanged(self, index: int):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


class BasicTab(BasicPage):

    def __init__(self, parent: QWidget = None):
        """
        基本的页面，没有边距和标题
        :param parent:
        """
        super().__init__(parent=parent)
        self.toolBar.deleteLater()
        self.setViewportMargins(0, 0, 0, 0)


class ChangeableTab(BasicTab):
    """
    可切换页面的页面
    """

    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self._pages = {}
        self.onShowPage = None
        self.onShowName = None

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)

    def addPage(self, widget: QWidget, wid: str | int = None, alignment: Qt.AlignmentFlag = None):
        """
        添加页面
        :param alignment: 对其方式
        :param widget: 组件
        :param wid: 页面id
        """
        widget.setParent(self)
        widget.hide()
        if not wid:
            wid = widget.objectName()
        self._pages[wid] = widget
        if alignment:
            self.vBoxLayout.addWidget(widget, 0, alignment)
        else:
            self.vBoxLayout.addWidget(widget)

    def showPage(self, wid: str | int):
        """
        展示页面
        :param wid: 页面id
        """
        self.hidePage()
        self.getPage(wid).show()
        self.onShowPage = self.getPage(wid)
        self.onShowName = wid

    def setPage(self, wid: str | int):
        """
        展示页面
        :param wid: 页面id
        """
        self.showPage(wid)

    def hidePage(self):
        """
        隐藏页面
        """
        if self.onShowPage:
            self.onShowPage.hide()

    def removePage(self, wid: str | int):
        """
        移除页面
        :param wid: 页面id
        :return:
        """
        if wid not in self._pages.keys():
            return False
        widget = self._pages.pop(wid)
        widget.hide()
        self.vBoxLayout.removeWidget(widget)
        widget.deleteLater()

    def getPage(self, wid: str | int):
        """
        获取指定页面
        :param wid: 页面id
        :return:
        """
        return self._pages.get(wid)


class ToolBar(QWidget):
    """
    页面顶端工具栏
    """

    def __init__(self, title: str, subtitle: str, parent=None):
        """
        :param title: 主标题
        :param subtitle: 副标题
        """
        super().__init__(parent=parent)
        self.setFixedHeight(90)

        self.titleLabel = TitleLabel(title, self)
        self.subtitleLabel = CaptionLabel(subtitle, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 22, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addWidget(self.subtitleLabel)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
