from ..base import *


class NewInfoBadgePosition(Enum):
    """ Info badge position """
    CENTER = 7


@InfoBadgeManager.register(NewInfoBadgePosition.CENTER)
class BottomCenterInfoBadgeManager(InfoBadgeManager):
    """ Bottom left info badge manager """

    def position(self):
        x = self.target.geometry().center().x() - self.badge.width() // 2
        y = self.target.geometry().center().y() - self.badge.height() // 2
        return QPoint(x, y)
