from .base import *

from aenum import Enum, extend_enum


class ZBF(FluentIconBase, Enum):

    def __init__(self, *args):
        self.use_theme_color = False
        self.light_color = QColor(0, 0, 0)
        self.dark_color = QColor(255, 255, 255)

    def path(self, theme=Theme.AUTO):
        if hasattr(self, "default_path"):
            path = self.default_path
        else:
            path = ""
        return zb.joinPath(path, self.value)

    @classmethod
    def setPath(cls, path: str):
        """
        设置在寻找数据不包括图标路径的图标时，默认寻找的路径
        :param path:
        """
        cls.default_path = path

    @classmethod
    def setDefaultPath(cls, path: str):
        """
        设置在寻找数据不包括图标路径的图标时，默认寻找的路径
        :param path:
        """
        cls.setPath(path)

    @classmethod
    def add(cls, name: str, data: str = None):
        """
        添加图片
        :param name: 调用时的名称
        :param data: 图片路径，不填默认使用name值，需要后缀名
        """
        if not data:
            data = name
        if not hasattr(cls, name):
            extend_enum(cls, name, data)

    @classmethod
    def addFromPath(cls, path: str):
        """
        从指定路径批量导入图标，会将去除后缀名的文件名称作为图标名称
        :param path: 文件夹路径
        """
        for i in zb.walkFile(path, True):
            ZBF.add(zb.getFileName(i, False), os.path.abspath(i))

    def useThemeColor(self, use_theme_color: bool = True):
        """
        使用程序主题色
        :param use_theme_color:
        """
        self.use_theme_color = use_theme_color

    def setColor(self, light_color: QColor, dark_color: QColor):
        """
        设置图标颜色
        :param light_color: 浅色模式下颜色，默认为黑色
        :param dark_color: 深色模式下颜色，默认为白色
        """
        self.light_color = light_color
        self.dark_color = dark_color

    def removeColor(self):
        """
        取消修改图标颜色，将显示图标本身的颜色
        """
        self.light_color = None
        self.dark_color = None

    def getLightColor(self):
        """
        获取当前设置的图标浅色模式下颜色
        :return:
        """
        return self.light_color

    def getDarkColor(self):
        """
        获取当前设置的图标深色模式下颜色
        :return:
        """
        return self.dark_color

    def lightColor(self):
        """
        获取当前设置的图标浅色模式下颜色
        :return:
        """
        return self.light_color

    def darkColor(self):
        """
        获取当前设置的图标深色模式下颜色
        :return:
        """
        return self.dark_color

    def setLightColor(self, light_color: QColor):
        """
        设置浅色模式下颜色
        :param light_color: 浅色模式下颜色，默认为黑色
        """
        self.light_color = light_color

    def removeLightColor(self):
        """
        取消修改浅色模式下图标颜色，将显示图标本身的颜色
        """
        self.light_color = None

    def setDarkColor(self, dark_color: QColor):
        """
        设置深色模式下颜色
        :param light_color: 深色模式下颜色，默认为白色
        """
        self.dark_color = dark_color

    def removeDarkColor(self):
        """
        取消修改深色模式下图标颜色，将显示图标本身的颜色
        """
        self.dark_color = None

    def render(self, painter, rect, theme=Theme.AUTO, indexes=None, **attributes):
        icon = self.path(theme)

        if not icon.endswith(".svg"):
            return super(FluentIconBase).render(painter, rect, theme, indexes, **attributes)
        if self.use_theme_color:
            color = themeColor()
        else:
            if theme == Theme.AUTO:
                color = self.dark_color if isDarkTheme() else self.light_color
            else:
                color = self.dark_color if theme == Theme.DARK else self.light_color
        if color:
            attributes.update(fill=color.name())
        icon = writeSvg(icon, indexes, **attributes).encode()
        drawSvgIcon(icon, painter, rect)
