from .base import *


class ZBF(FluentIconBase, Enum):
    apps_list_filled = "apps_list_filled"
    apps_list = "apps_list"


    def path(self, theme=Theme.AUTO):
        return f':/zbWidgetLib/icons/{self.value}_{getIconColor(theme)}.svg'
