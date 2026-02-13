from ..base import *


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
            self.titleLabel.setSelectable()
            self.valueLabel.setSelectable()

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


class ComboBoxWithLabel(QWidget):
    @functools.singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(4)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.label = BodyLabel("", self)
        self.comboBox = ComboBox(self)

        self.hBoxLayout.addWidget(self.label, 0, Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.comboBox)

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.label.setText(text)

    def __getattr__(self, name: str):
        """委托属性访问到label或comboBox"""
        try:
            return getattr(self.comboBox, name)
        except AttributeError:
            try:
                return getattr(self.label, name)
            except AttributeError:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


class PageSpliter(QWidget):
    pageChanged = pyqtSignal(int, int, int)

    def __init__(self, parent=None, max_page: int = 10, max_visible: int = 10, length: int = 10,
                 preset_length: list = None, max_length: int = 100, total_count: int = -1,
                 show_max: bool = True, show_jump_input: bool = True, show_length_input: bool = True,
                 show_first_last: bool = True, show_total_count: bool = True):
        """
        :param parent: 父组件
        :param max_page: 最大页码（当total_count>0时会被覆盖）
        :param max_visible: 同时显示的分页按钮数量
        :param length: 每个页面的长度（项目数量）
        :param preset_length: 预设的页面长度选项列表
        :param max_length: 允许的最大页面长度
        :param total_count: 项目总数（-1表示无限制，0表示只有1页）
        :param show_max: 是否显示最大页码
        :param show_jump_input: 是否显示页面跳转输入框
        :param show_length_input: 是否显示页面长度设置控件
        :param show_first_last: 是否显示首页/末页跳转按钮
        :param show_total_count: 是否显示共x项总数标签
        """
        super().__init__(parent)

        self.page = 0
        self._buttons = {}
        self.numberButtons = []

        if preset_length is None:
            preset_length = []
        else:
            preset_length = [i for i in preset_length if 0 < i <= max_length]

        if length <= 0:
            length = 1
        if length > max_length:
            length = max_length

        if preset_length and length not in preset_length:
            preset_length.append(length)
        preset_length = sorted(list(set(preset_length)))

        if total_count > 0:
            max_page = max(1, (total_count - 1) // length + 1)
        elif total_count == 0:
            max_page = 1
        else:
            total_count = -1

        self.max_visible = max_visible
        self.max_page = max_page
        self.length = length
        self.preset_length = preset_length
        self.max_length = max_length
        self.total_count = total_count
        self.show_max = show_max
        self.show_jump_input = show_jump_input
        self.show_length_input = show_length_input
        self.show_first_last = show_first_last
        self.show_total_count = show_total_count

        self._create_ui_components()
        self._setup_layout()
        self._initialize_state()

    def _create_ui_components(self):
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSpacing(8)

        self.firstButton = TransparentToolButton(ZBF.SkipStartFill, self)
        self.firstButton.clicked.connect(lambda: self.setPage(1))

        self.leftButton = TransparentToolButton(FIF.CARE_LEFT_SOLID, self)
        self.leftButton.clicked.connect(lambda: self.setPage(self.page - 1))

        self.rightButton = TransparentToolButton(FIF.CARE_RIGHT_SOLID, self)
        self.rightButton.clicked.connect(lambda: self.setPage(self.page + 1))

        self.lastButton = TransparentToolButton(ZBF.SkipEndFill, self)
        self.lastButton.clicked.connect(lambda: self.setPage(self.max_page))

        self.label1 = BodyLabel("页", self)
        self.lineEdit1 = LineEdit(self)
        self.lineEdit1.setMaximumWidth(50)

        self.label2 = BodyLabel("/", self)
        self.label3 = BodyLabel(str(self.max_page), self)
        self.label4 = BodyLabel("页", self)

        self.lineEdit2 = LineEdit(self)
        self.lineEdit2.setText(str(self.length))
        self.lineEdit2.setMaximumWidth(50)

        self.label5 = BodyLabel("/", self)
        self.label6 = BodyLabel("页", self)

        self.comboBox = ComboBox(self)
        self.totalCountLabel = BodyLabel("", self)

    def _setup_layout(self):
        self.hBoxLayout.addWidget(self.firstButton, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.leftButton, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.rightButton, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.lastButton, 0, Qt.AlignLeft)

        self.hBoxLayout.addWidget(self.label1, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.lineEdit1, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.label2, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.label3, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.label4, 0, Qt.AlignLeft)

        self.hBoxLayout.addSpacing(8)

        self.hBoxLayout.addWidget(self.lineEdit2, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.label5, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.label6, 0, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignLeft)

        self.hBoxLayout.addSpacing(8)
        self.hBoxLayout.addWidget(self.totalCountLabel, 0, Qt.AlignRight)

        self.hBoxLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.hBoxLayout)

    def _initialize_state(self):
        if self.max_page <= 0:
            self.lineEdit1.setValidator(QIntValidator(1, 1000))
            self.lineEdit2.setValidator(QIntValidator(1, 1000))
        else:
            self.lineEdit1.setValidator(QIntValidator(1, self.max_page))
            self.lineEdit2.setValidator(QIntValidator(1, self.max_length))

        self.lineEdit1.returnPressed.connect(lambda: self.setPage(int(self.lineEdit1.text())))
        self.lineEdit2.returnPressed.connect(lambda: self.setLength(int(self.lineEdit2.text())))

        self.comboBox.addItems([str(i) + " / 页" for i in self.preset_length])
        self.comboBox.currentTextChanged.connect(lambda text: self.setLength(int(text[:-4] if text else 0)))

        self.setShowMax(self.show_max)
        self.setShowJumpInput(self.show_jump_input)
        self.setShowLengthInput(self.show_length_input)
        self.setShowFirstLast(self.show_first_last)
        self.setShowTotalCount(self.show_total_count)

        self._adjustButtonCount()
        self.setPage(1, False)
        self._updateTotalCountLabel()

    def _adjustButtonCount(self):
        display_count = self.max_visible
        if self.max_page > 0:
            display_count = min(self.max_visible, self.max_page)

        current_count = len(self.numberButtons)

        if current_count > display_count:
            for i in range(current_count - 1, display_count - 1, -1):
                btn = self.numberButtons.pop()
                self.hBoxLayout.removeWidget(btn)
                btn.deleteLater()

        if current_count < display_count:
            for i in range(current_count, display_count):
                btn = TransparentToggleToolButton(self)
                btn.clicked.connect(self._createButtonHandler(len(self.numberButtons)))
                self.numberButtons.append(btn)
                index = self.hBoxLayout.indexOf(self.rightButton)
                self.hBoxLayout.insertWidget(index, btn, 0, Qt.AlignLeft)

        self._updateButtons()

    def _updateButtons(self):
        if not self.numberButtons:
            return

        if self.max_page <= 0:
            start = max(1, self.page - self.max_visible // 2)
        else:
            start = max(1, min(self.page - self.max_visible // 2,
                               self.max_page - len(self.numberButtons) + 1))

        for i, btn in enumerate(self.numberButtons):
            btn_num = start + i
            if self.max_page <= 0 or btn_num <= self.max_page:
                btn.setText(str(btn_num))
                btn.setVisible(True)
                btn.setChecked(btn_num == self.page)
            else:
                btn.setVisible(False)

        self.leftButton.setEnabled(self.page > 1)
        self.rightButton.setEnabled(self.max_page <= 0 or self.page < self.max_page)
        self.firstButton.setEnabled(self.page > 1)
        if self.max_page > 0:
            self.lastButton.setEnabled(self.page < self.max_page)
        else:
            self.lastButton.setEnabled(False)

    def _createButtonHandler(self, index):
        def handler():
            if index < len(self.numberButtons):
                text = self.numberButtons[index].text()
                if text.isdigit():
                    self.setPage(int(text))

        return handler

    def _updateLastButtonVisibility(self):
        visible = self.show_first_last and self.max_page > 0 and self.total_count >= 0
        self.lastButton.setVisible(visible)

    def _updateTotalCountLabel(self):
        if self.show_total_count and self.total_count > 0:
            self.totalCountLabel.setText(f"共 {self.total_count} 项")
            self.totalCountLabel.setVisible(True)
        else:
            self.totalCountLabel.setVisible(False)

    def setMaxVisible(self, max_visible: int):
        """
        :param max_visible: 新的最大可见按钮数
        """
        if max_visible < 1:
            max_visible = 1
        if self.max_visible == max_visible:
            return

        self.max_visible = max_visible
        self._adjustButtonCount()
        self._updateButtons()

    def getMaxVisible(self):
        """
        :return: 当前最大可见按钮数
        """
        return self.max_visible

    def setPage(self, page: int, signal: bool = True):
        """
        :param page: 新的页码（从1开始）
        :param signal: 是否发送pageChanged信号
        """
        if self.page == page and not signal:
            return
        if page < 1 or (self.max_page > 0 and page > self.max_page):
            return

        self.page = page

        self.leftButton.setEnabled(page > 1)
        self.rightButton.setEnabled(self.max_page <= 0 or page < self.max_page)
        self.firstButton.setEnabled(page > 1)
        if self.max_page > 0:
            self.lastButton.setEnabled(page < self.max_page)

        self._updateButtons()
        self.lineEdit1.setText(str(page))

        if signal:
            self.pageChanged.emit(self.page, self.length, self.getNumber())

    def getPage(self):
        """
        :return: 当前页码
        """
        return self.page

    def getNumber(self):
        """
        :return: 起始项目编号（从0开始）
        """
        return (self.page - 1) * self.length

    def getLength(self):
        """
        :return: 页面长度
        """
        return self.length

    def setLength(self, length: int, signal: bool = True):
        """
        :param length: 新的页面长度
        :param signal: 是否发送pageChanged信号
        """
        if length <= 0 or length > self.max_length:
            return

        self.length = length

        if self.preset_length and length not in self.preset_length:
            self.addPresetLength(length)

        if self.total_count > 0:
            max_page = max(1, (self.total_count - 1) // length + 1)
        elif self.total_count == 0:
            max_page = 1
        else:
            max_page = 0

        self.setMaxPage(max_page, False)

        self.lineEdit2.setText(str(length))
        self.comboBox.setCurrentText(f"{length} / 页")

        if signal:
            self.pageChanged.emit(self.page, self.length, self.getNumber())

    def setMaxPage(self, max_page: int, signal: bool = True):
        """
        :param max_page: 新的最大页码
        :param signal: 是否发送pageChanged信号
        """
        self.max_page = max_page

        if self.max_page <= 0:
            self.lineEdit1.setValidator(QIntValidator(1, 1000))
        else:
            self.lineEdit1.setValidator(QIntValidator(1, self.max_page))

        self.label2.setVisible(self.show_max and self.show_jump_input and self.max_page > 0)
        self.label3.setText(str(self.max_page))
        self.label3.setVisible(self.show_max and self.max_page > 0)
        self.label4.setVisible(self.show_max and self.max_page > 0)

        self._updateLastButtonVisibility()
        self._adjustButtonCount()

        if 0 < self.max_page < self.page:
            self.setPage(self.max_page, signal)
        else:
            self._updateButtons()
            if signal:
                self.pageChanged.emit(self.page, self.length, self.getNumber())

    def getMaxPage(self):
        """
        :return: 最大页码
        """
        return self.max_page

    def setShowMax(self, show_max: bool):
        """
        :param show_max: 是否显示最大页码
        """
        self.show_max = show_max
        self.label2.setVisible(self.show_max and self.show_jump_input and self.max_page > 0)
        self.label3.setVisible(self.show_max and self.max_page > 0)
        self.label4.setVisible(self.show_max and self.max_page > 0)

    def getShowMax(self):
        """
        :return: 是否显示最大页码
        """
        return self.show_max

    def setShowJumpInput(self, show_jump_input: bool):
        """
        :param show_jump_input: 是否显示跳转输入框
        """
        self.show_jump_input = show_jump_input
        self.label1.setVisible(self.show_jump_input)
        self.lineEdit1.setVisible(self.show_jump_input)
        self.label2.setVisible(self.show_max and self.show_jump_input and self.max_page > 0)

    def getShowJumpInput(self):
        """
        :return: 是否显示跳转输入框
        """
        return self.show_jump_input

    def setShowLengthInput(self, show_length_input: bool):
        """
        :param show_length_input: 是否显示页面长度设置控件
        """
        self.show_length_input = show_length_input
        self.lineEdit2.setVisible(self.show_length_input and not bool(self.preset_length))
        self.label5.setVisible(self.show_length_input and not bool(self.preset_length))
        self.label6.setVisible(self.show_length_input and not bool(self.preset_length))
        self.comboBox.setVisible(self.show_length_input and bool(self.preset_length))

    def getShowLengthInput(self):
        """
        :return: 是否显示页面长度设置控件
        """
        return self.show_length_input

    def setShowFirstLast(self, show: bool):
        """
        :param show: 是否显示首页/末页跳转按钮
        """
        self.show_first_last = show
        self.firstButton.setVisible(show)
        self._updateLastButtonVisibility()

    def getShowFirstLast(self):
        """
        :return: 是否显示首页/末页跳转按钮
        """
        return self.show_first_last

    def setShowTotalCount(self, show: bool):
        """
        :param show: 是否显示总数标签
        """
        self.show_total_count = show
        self._updateTotalCountLabel()

    def getShowTotalCount(self):
        """
        :return: 是否显示总数标签
        """
        return self.show_total_count

    def setPresetLength(self, preset_length: list):
        """
        :param preset_length: 新的预设长度列表
        """
        if preset_length is None:
            preset_length = []
        else:
            preset_length = [i for i in preset_length if 0 < i <= self.max_length]

        if self.length not in preset_length and preset_length:
            preset_length.append(self.length)

        self.preset_length = sorted(list(set(preset_length)))

        self.comboBox.blockSignals(True)
        self.comboBox.clear()
        self.comboBox.addItems([str(i) + " / 页" for i in self.preset_length])
        self.comboBox.setCurrentText(str(self.length) + " / 页")
        self.comboBox.blockSignals(False)

        self.setShowLengthInput(self.show_length_input)

    def addPresetLength(self, preset_length: int | list):
        """
        :param preset_length: 要添加的长度值或列表
        """
        if isinstance(preset_length, int):
            self.setPresetLength(self.preset_length + [preset_length])
        elif isinstance(preset_length, list):
            self.setPresetLength(self.preset_length + preset_length)

    def removePresetLength(self, preset_length: int | list):
        """
        :param preset_length: 要移除的长度值或列表
        """
        if isinstance(preset_length, int):
            preset_length = [preset_length]

        old = self.preset_length.copy()
        for i in preset_length:
            if i in old:
                old.remove(i)

        self.setPresetLength(old)

    def getPresetLength(self):
        """
        :return: 预设长度列表
        """
        return self.preset_length

    def setMaxLength(self, max_length: int):
        """
        :param max_length: 新的最大长度
        """
        self.max_length = max_length

        if self.length > self.max_length:
            self.setLength(self.max_length)

        if self.preset_length:
            self.setPresetLength(self.preset_length)

        if self.max_page <= 0:
            self.lineEdit2.setValidator(QIntValidator(1, 1000))
        else:
            self.lineEdit2.setValidator(QIntValidator(1, self.max_length))

    def getMaxLength(self):
        """
        :return: 最大长度
        """
        return self.max_length

    def setTotalCount(self, total_count: int, signal: bool = True):
        """
        :param total_count: 项目总数（-1表示无限制，0表示只有1页）
        :param signal: 是否发送信号
        """
        self.total_count = total_count

        if total_count > 0:
            max_page = max(1, (total_count - 1) // self.length + 1)
        elif total_count == 0:
            max_page = 1
        else:
            max_page = 0

        self.setMaxPage(max_page, signal)
        self._updateTotalCountLabel()
        self._updateLastButtonVisibility()

    def getTotalCount(self):
        """
        :return: 项目总数（-1表示无限制）
        """
        return self.total_count


class LineEditWithLabel(QWidget):
    @functools.singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(4)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.label = BodyLabel("", self)
        self.lineEdit = LineEdit(self)

        self.hBoxLayout.addWidget(self.label, 0, Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.lineEdit)

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.label.setText(text)

    def __getattr__(self, name: str):
        try:
            return getattr(self.lineEdit, name)
        except AttributeError:
            try:
                return getattr(self.label, name)
            except AttributeError:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
