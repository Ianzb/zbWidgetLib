from ..base import *


class SimpleSplashScreen(SplashScreen):
    """ Splash screen """

    def __init__(self, icon: str | QIcon | FluentIconBase, parent=None, enableShadow=True):
        super().__init__(icon, parent, enableShadow)

    def eventFilter(self, obj, e: QEvent):
        if obj is self.parent():
            if e.type() == QEvent.Resize:
                self.resize(e.size())
        return super(SplashScreen, self).eventFilter(obj, e)
