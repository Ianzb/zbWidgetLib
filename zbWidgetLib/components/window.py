from qframelesswindow.windows import WindowsWindowEffect

from ..base import *


class WindowEffectBase:

    def __init__(self, *args):
        if not hasattr(self, "windowEffect"):
            self.windowEffect = WindowsWindowEffect(self)
        self._currentEffect = ""
        self._isEffectEnabled = False

        self._installHooks()

    def _installHooks(self):
        original_show_event = self.showEvent

        def patched_show_event(e):
            original_show_event(e)

            if self.isEffectEnabled():
                self.setEffect(self.currentEffect())

        self.showEvent = patched_show_event

    def setEffect(self, effect_type: str):
        """
        设置窗口效果
        :param effect_type: 效果类型：Mica, Mica Alt, Acrylic, Aero
        :return:
        """
        last_effect = self._currentEffect

        self.removeEffect()
        effect_type = effect_type.lower()
        if effect_type == "Mica".lower():
            if sys.platform != "win32" or sys.getwindowsversion().build < 22000:
                return
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
            self._currentEffect = "Mica"

        elif effect_type == "Mica Alt".lower():
            if sys.platform != "win32" or sys.getwindowsversion().build < 22000:
                return

            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme(), True)
            self._currentEffect = "Mica Alt"

        elif effect_type == "Acrylic".lower():
            if isDarkTheme():
                self.windowEffect.setAcrylicEffect(self.winId(), gradientColor="000000CC", animationId=1)
            else:
                self.windowEffect.setAcrylicEffect(self.winId(), gradientColor="F2F2F299", animationId=1)
            self._currentEffect = "Acrylic"

        elif effect_type == "Aero".lower():
            self.windowEffect.setAeroEffect(self.winId())
            self._currentEffect = "Aero"
        self._isEffectEnabled = True
        self._isMicaEnabled = True

        if self.window().isVisible() and ((last_effect not in ["Acrylic", "Aero"] and self._currentEffect in ["Acrylic", "Aero"]) or (isDarkTheme() and last_effect in ["Aero"] and self._currentEffect in ["Acrylic"])):
            self.window().hide()
            self.window().show()
        self.setBackgroundColor(self._normalBackgroundColor())

    def removeEffect(self):

        self._isMicaEnabled = False
        self._isEffectEnabled = False
        self._currentEffect = ""
        self.windowEffect.removeBackgroundEffect(self.winId())

    def isEffectEnabled(self):
        return self._isEffectEnabled

    def getCurrentEffect(self):
        return self._currentEffect

    def currentEffect(self):
        return self.getCurrentEffect()

    def _onThemeChangedFinished(self):
        if self.isEffectEnabled():
            if self.currentEffect() in ["Mica", "Mica Alt"]:
                self.setEffect(self.currentEffect())

    def _normalBackgroundColor(self):
        if not self._currentEffect:
            return self._darkBackgroundColor if isDarkTheme() else self._lightBackgroundColor
        if self.currentEffect() == "Acrylic":
            return QColor(0, 0, 0, 64) if isDarkTheme() else QColor(0, 0, 0, 0)
        return QColor(0, 0, 0, 0)

    def showEvent(self, e):
        super().showEvent(e)
        if self.isEffectEnabled():
            self.setEffect(self.currentEffect())


class Window(FluentWindow, WindowEffectBase):
    """
    主窗口
    """

    def __init__(self):
        super().__init__()

    def addPage(self, page, name: str, icon, pos: str):
        """
        添加导航栏页面简易版
        :param page: 页面对象
        :param pos: 位置top/scroll/bottom
        """
        page.setObjectName(name)
        return self.addSubInterface(page, icon, name, eval(f"NavigationItemPosition.{pos.upper()}"))

    def addSeparator(self, pos: str):
        """
        添加导航栏分割线简易版
        :param pos: 位置top/scroll/bottom
        """
        self.navigationInterface.addSeparator(eval(f"NavigationItemPosition.{pos.upper()}"))
