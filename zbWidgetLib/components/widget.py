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
        self.comboBox = AcrylicComboBox(self)

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
    pageChanged = pyqtSignal(int, int, int)  # 信号：当前页码, 页面长度, 起始编号(0开始)

    def __init__(self, parent=None, max_page: int = 10, max_visible: int = 10, length: int = 10,
                 preset_length: list = None, max_length: int = 100, total_count: int = -1,
                 show_max: bool = True, show_jump_input: bool = True, show_length_input: bool = True):
        """
        分页器组件，通过pageChanged绑定页面修改事件

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
        elif total_count == 0:
            max_page = 1  # 总数为0时强制为1页
        else:  # total_count < 0 表示无限制
            total_count = -1  # 确保为负值

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
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
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
        self.leftButton.setEnabled(self.page > 1)
        self.rightButton.setEnabled(self.max_page <= 0 or self.page < self.max_page)

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
            max_page = max(1, (self.total_count - 1) // length + 1)
        elif self.total_count == 0:
            max_page = 1  # 总数为0时强制为1页
        else:  # total_count < 0 表示无限制
            max_page = 0  # 无限制

        self.setMaxPage(max_page, False)

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

    def setTotalCount(self, total_count: int, signal: bool = True):
        """
        设置项目总数（自动计算最大页码）

        :param total_count: 项目总数（-1表示无限制，0表示只有1页）
        :param signal: 是否发送信号
        """
        self.total_count = total_count

        # 根据新的总数计算最大页码
        if total_count > 0:
            max_page = max(1, (total_count - 1) // self.length + 1)
        elif total_count == 0:
            max_page = 1  # 总数为0时强制为1页
        else:  # total_count < 0 表示无限制
            max_page = 0  # 无限制

        self.setMaxPage(max_page, signal)

    def getTotalCount(self):
        """
        获取项目总数

        :return: 项目总数（-1表示无限制）
        """
        return self.total_count
