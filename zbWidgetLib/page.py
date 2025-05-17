from .base import *


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


class BasicPage(BetterScrollArea):

    def __init__(self, parent=None, title: str = None, subtitle: str = None, icon=None):
        """
        基本页面，包含标题和子标题，适用于基本页面，通过类变量修改title和subtitle设置标题和子标题。
        :param parent:
        """
        super().__init__(parent=parent)

        self.toolBar = ToolBar(self)
        if title:
            self.setTitle(title)
        if subtitle:
            self.setSubtitle(subtitle)

        self.setViewportMargins(0, self.toolBar.height(), 0, 0)

        self._icon = None

    def getTitle(self):
        """
        获取主标题
        :return: 主标题
        """
        return self.toolBar.title()

    def title(self):
        """
        获取主标题
        :return: 主标题
        """
        return self.getTitle()

    def getSubtitle(self):
        """
        获取副标题
        :return: 副标题
        """
        return self.toolBar.subtitle()

    def subtitle(self):
        """
        获取副标题
        :return: 副标题
        """
        return self.getSubtitle()

    def setTitle(self, text: str):
        """
        设置主标题
        :param text:
        """
        self.toolBar.setTitle(text)

    def setSubtitle(self, text: str):
        """
        设置副标题
        :param text:
        """
        self.toolBar.setSubtitle(text)

    def setIcon(self, icon):
        """
        设置页面图标
        :param icon: 图标
        """
        self._icon = icon

    def getIcon(self):
        """
        获取页面图标
        :return: 图标
        """
        return self._icon

    def icon(self):
        """
        获取页面图标
        :return: 图标
        """
        return self.getIcon()


class BasicTabPage(BasicPage):
    _pages = {}

    def __init__(self, parent=None):
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

    def addPage(self, widget, name: str = None, icon=None):
        """
        添加标签页
        :param widget: 标签页对象
        :param name: 名称
        :param icon: 图标
        """
        if not name:
            name = widget.objectName()
        if name in self._pages.keys():
            raise NameError(f"页面名称{name}已存在，请替换为其他名称!")
        widget.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(name, name, lambda: self.stackedWidget.setCurrentWidget(widget), icon)
        self._pages[name] = widget
        if self.stackedWidget.count() == 1:
            self.pivot.setCurrentItem(name)

    def setPage(self, name: str = None):
        self.pivot.setCurrentItem(name)

    def showPage(self, name: str = None):
        self.setPage(name=name)

    def getPage(self, name: str):
        """
        获取指定页面
        :param name: 页面id
        :return: 页面对象
        """
        return self._pages.get(name)

    def page(self, name: str):
        """
        获取指定页面
        :param name: 页面id
        :return: 页面对象
        """
        return self.getPage(name)

    def getPages(self):
        """
        获取所有页面
        :return: 页面名称和对象的字典
        """
        return self._pages

    def pages(self):
        """
        获取所有页面
        :return: 页面名称和对象的字典
        """
        return self.getPages()

    def removePage(self, name: str):
        """
        移除页面
        :param name: 页面名称
        :return:
        """
        if name not in self._pages.keys():
            return False
        widget = self._pages.pop(name)
        widget.hide()
        self.stackedWidget.removeWidget(widget)
        self.pivot.removeWidget(name)
        widget.deleteLater()

    def deletePage(self, name: str):
        """
        删除页面
        :param name: 页面名称
        :return:
        """
        self.removePage(name)

    def onCurrentIndexChanged(self, index: int):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


class BasicTab(BasicPage):

    def __init__(self, parent=None):
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

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._pages = {}
        self.on_show_page = None
        self.on_show_wid = None

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)

    def addPage(self, widget, wid: str | int = None, alignment: Qt.AlignmentFlag = None):
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
        self.on_show_page = self.getPage(wid)
        self.on_show_wid = wid

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
        if self.on_show_page:
            self.on_show_page.hide()

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

    def page(self, wid: str | int):
        """
        获取指定页面
        :param wid: 页面id
        :return:
        """
        return self.getPage(wid)

    def pageAt(self, wid: str | int):
        """
        获取指定页面
        :param wid: 页面id
        :return:
        """
        return self.getPage(wid)


class ToolBar(QWidget):
    """
    页面顶端工具栏
    """

    def __init__(self, parent=None, title: str = None, subtitle: str = None):
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

    def getTitle(self):
        """
        获取主标题
        :return: 主标题
        """
        return self.titleLabel.text()

    def title(self):
        """
        获取主标题
        :return: 主标题
        """
        return self.getTitle()

    def setTitle(self, text: str):
        """
        设置主标题
        :param text: 主标题
        """
        self.titleLabel.setText(text)

    def getSubtitle(self):
        """
        获取副标题
        :return: 副标题
        """
        return self.subtitleLabel.text()

    def subtitle(self):
        """
        获取副标题
        :return: 副标题
        """
        return self.getSubtitle()

    def setSubtitle(self, text: str):
        """
        设置副标题
        :param text:
        """
        self.subtitleLabel.setText(text)


class Window(FluentWindow):
    """
    主窗口
    """

    def __init__(self):
        super().__init__()

    def addPage(self, page, pos: str):
        """
        添加导航栏页面简易版
        @param page: 页面对象
        @param pos: 位置top/scroll/bottom
        """
        return self.addSubInterface(page, page.getIcon(), page.objectName(), eval(f"NavigationItemPosition.{pos.upper()}"))

    def addSeparator(self, pos: str):
        """
        添加导航栏分割线简易版
        @param pos: 位置top/scroll/bottom
        """
        self.navigationInterface.addSeparator(eval(f"NavigationItemPosition.{pos.upper()}"))
