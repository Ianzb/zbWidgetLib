from .base import *

from aenum import Enum, extend_enum


class ZBF(FluentIconBase, Enum):
    def __init__(self, *args):
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

    def setColor(self, light_color: QColor, dark_color: QColor):
        self.light_color = light_color
        self.dark_color = dark_color

    def removeColor(self):
        self.light_color = None
        self.dark_color = None

    def getLightColor(self):
        return self.light_color

    def getDarkColor(self):
        return self.dark_color

    def lightColor(self):
        return self.light_color

    def darkColor(self):
        return self.dark_color

    def setLightColor(self, light_color: QColor):
        self.light_color = light_color

    def removeLightColor(self):
        self.light_color = None

    def setDarkColor(self, dark_color: QColor):
        self.dark_color = dark_color

    def removeDarkColor(self):
        self.dark_color = None

    def render(self, painter, rect, theme=Theme.AUTO, indexes=None, **attributes):
        icon = self.path(theme)

        if not icon.endswith(".svg"):
            return super(FluentIconBase).render(painter, rect, theme, indexes, **attributes)

        if theme == Theme.AUTO:
            color = self.dark_color if isDarkTheme() else self.light_color
        else:
            color = self.dark_color if theme == Theme.DARK else self.light_color
        if color:
            attributes.update(fill=color.name())
        icon = writeSvg(icon, indexes, **attributes).encode()
        drawSvgIcon(icon, painter, rect)
