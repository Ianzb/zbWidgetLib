from .base import *

from aenum import Enum, extend_enum


class ZBF(FluentIconBase, Enum):
    def __init__(self, *args):
        self.use_theme_color = False
        self.light_color = QColor(0, 0, 0)
        self.dark_color = QColor(255, 255, 255)

    def path(self, theme=Theme.AUTO):
        return zb.joinPath(ZBF._path, f"{self.value}.svg")

    @classmethod
    def setPath(cls, path):
        cls._path = path

    @classmethod
    def add(cls, name):
        if not hasattr(cls, name):
            extend_enum(cls, name, name)

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
