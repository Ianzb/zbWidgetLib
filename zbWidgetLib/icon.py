from .base import *


class ZBF(FluentIconBase, Enum):
    FluentAppsList = "FluentAppsList"



    def path(self, theme=Theme.AUTO):
        return f':/zbWidgetLib/icons/{self.value}_{getIconColor(theme)}.svg'
