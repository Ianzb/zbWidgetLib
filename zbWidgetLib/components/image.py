from ..base import *
from concurrent.futures import ThreadPoolExecutor

from qfluentwidgets.common.icon import toQIcon


class Image(QLabel):
    def __init__(self, parent=None):
        """
        图片组件
        """
        super().__init__(parent=parent)
        self.setFixedSize(48, 48)
        self.setScaledContents(True)

    def setImg(self, img: str | FluentIconBase):
        """
        设置图片
        :param img: 路径
        :param url: 链接
        :param thread_pool: 下载线程池
        """
        self.loading = False
        if isinstance(img, str):
            self.setPixmap(QPixmap(img))
        elif isinstance(img, FluentIconBase):
            self.setPixmap(toQIcon(img).pixmap(QSize(100, 100)))


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
    def _(self, img: str | FluentIconBase, url: str = None, parent=None, thread_pool: ThreadPoolExecutor = None):
        """
        图片组件（可实时下载）
        :param img: 路径
        :param url: 链接
        :param parent:
        :param thread_pool: 线程池
        """
        self.__init__(parent)
        if img:
            self.setImg(img, url, thread_pool)

    @__init__.register
    def _(self, img: str | FluentIconBase, parent=None):
        """
        :param img: 路径
        """
        self.__init__(parent)
        if img:
            self.setImg(img)

    def setImg(self, img: str | FluentIconBase, url: str = None, thread_pool: ThreadPoolExecutor = None):
        """
        设置图片
        :param img: 路径
        :param url: 链接
        :param thread_pool: 下载线程池
        """
        if url:
            self.loading = True
            self.path = img
            self.url = url

            thread_pool.submit(self.download)
        else:
            self.loading = False
            if isinstance(img, str):
                self.setPixmap(QPixmap(img))
            elif isinstance(img, FluentIconBase):
                self.setPixmap(toQIcon(img).pixmap(QSize(100, 100)))

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
