from ..base import *


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
        file_name = [i for i in file_name if i]
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

    def setFileMode(self):
        """
        设置选择器模式为文件
        """
        self.mode = "file"
        self._setText()

    def setFolderMode(self):
        """
        设置选择器模式为文件夹
        """
        self.mode = "folder"
        self._setText()

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
