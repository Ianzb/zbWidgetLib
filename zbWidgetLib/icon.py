from .base import *

from aenum import Enum, extend_enum


class ZBF(FluentIconBase, Enum):
    def path(self, theme=Theme.AUTO):
        return zb.joinPath(ZBF._path, f"{self.value}_{getIconColor(theme)}.svg")

    @classmethod
    def setPath(cls, path):
        cls._path = path

    @classmethod
    def add(cls, name):
        if not hasattr(cls, name):
            extend_enum(cls, name, name)
