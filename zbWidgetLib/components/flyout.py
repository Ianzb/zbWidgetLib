from ..base import *


class NewFlyoutAnimationType(Enum):
    """ Flyout animation type """
    FADE_IN = 4
    NONE = 6


@FlyoutAnimationManager.register(NewFlyoutAnimationType.FADE_IN)
class FadeInFlyoutAnimationManager(FlyoutAnimationManager):
    """ Fade in flyout animation manager """

    def position(self, target: QWidget):
        """ return the top left position relative to the target """
        w = self.flyout
        pos = target.mapToGlobal(QPoint(0, target.height()))
        x = pos.x() + target.width() // 2 - w.sizeHint().width() // 2
        y = pos.y() - w.layout().contentsMargins().top() + 8
        return QPoint(x, y)

    def exec(self, pos: QPoint):
        self.flyout.move(self._adjustPosition(pos))
        self.aniGroup.removeAnimation(self.slideAni)
        self.aniGroup.start()


@FlyoutAnimationManager.register(NewFlyoutAnimationType.NONE)
class DummyFlyoutAnimationManager(FlyoutAnimationManager):
    """ Dummy flyout animation manager """

    def exec(self, pos: QPoint):
        """ start animation """
        self.flyout.move(self._adjustPosition(pos))

    def position(self, target: QWidget):
        """ return the top left position relative to the target """
        w = self.flyout
        pos = target.mapToGlobal(QPoint(0, target.height()))
        x = pos.x() + target.width() // 2 - w.sizeHint().width() // 2
        y = pos.y() - w.layout().contentsMargins().top() + 8
        return QPoint(x, y)