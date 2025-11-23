from ..base import *


class CopyTextButton(ToolButton):

    def __init__(self, text: str, data_type: str = "", parent=None):
        """
        复制文本按钮
        :param text: 复制的文本
        :param data_type: 复制文本的提示信息，可以提示复制文本的内容类型
        :param parent: 父组件
        """
        super().__init__(parent=parent)
        self.setIcon(FIF.COPY)
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

        self.setNewToolTip(f"点击复制{self._data_type}信息！")

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


class SaveFileBase:
    fileChoosedSignal = pyqtSignal(str)

    def __init__(self):
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
        if not zb.existPath(self.default_path):
            zb.createDir(zb.getFileDir(self.default_path))

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


class SaveFilePushButton(PushButton, SaveFileBase):

    def __init__(self, parent=None):
        super().__init__(parent)


class SaveFilePrimaryPushButton(PrimaryPushButton, SaveFileBase):

    def __init__(self, parent=None):
        super().__init__(parent)


class OpenFileBase:
    fileChoosedSignal = pyqtSignal(str)

    def __init__(self):
        self.suffixs = {}
        self.default_path = None
        self.description = None
        self.only_one = True
        self.mode = "file"

        self.setText("导入")

        self.clicked.connect(self.clickEvent)

    def clickEvent(self):
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

        self.fileChoosedSignal.emit([i for i in file_name if i])

    def setFileMode(self):
        """
        设置选择器模式为文件
        """
        self.mode = "file"

    def setFolderMode(self):
        """
        设置选择器模式为文件夹
        """
        self.mode = "folder"

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
        self.setText(f"导入{description}")

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
        if not zb.existPath(self.default_path):
            zb.createDir(zb.getFileDir(self.default_path))

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


class OpenFilePushButton(PushButton, OpenFileBase):

    def __init__(self, parent=None):
        super().__init__(parent)


class OpenFilePrimaryPushButton(PrimaryPushButton, OpenFileBase):

    def __init__(self, parent=None):
        super().__init__(parent)
