from .base import *

import win32con
import win32gui
from ctypes import byref


import qframelesswindow

@classmethod
def toggleMaxState(cls, window):
    QT_VERSION = tuple(int(v) for v in qVersion().split('.'))


    if QT_VERSION < (6, 8, 0):
        if window.isMaximized():
            window.showNormal()
        else:
            window.showMaximized()
    else:
        if window.isMaximized():

            win32gui.PostMessage(int(window.winId()), win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        else:
            window.windowEffect.disableBlurBehindWindow(window.winId())
            window.windowEffect.removeWindowAnimation(window.winId())
            window.windowEffect.enableBlurBehindWindow(window.winId())
            window.windowEffect.addWindowAnimation(window.winId())
            win32gui.PostMessage(int(window.winId()), win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)

    qframelesswindow.utils.win32_utils.releaseMouseLeftButton(window.winId())


def disableBlurBehindWindow(self, hWnd):
    """ disable the blur effect behind the whole client
    Parameters

        hWnd: int or `sip.voidptr`
        Window handle"""
    blurBehind = qframelesswindow.windows.c_structures.DWM_BLURBEHIND(1, False, 0, False)
    self.DwmEnableBlurBehindWindow(int(hWnd), byref(blurBehind))

@staticmethod
def removeWindowAnimation(hWnd):
    """ Disables maximize and minimize animation of the window by removing the relevant window styles. """
    hWnd = int(hWnd)
    style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
    style &= ~win32con.WS_MINIMIZEBOX
    style &= ~win32con.WS_MAXIMIZEBOX
    style &= ~win32con.WS_CAPTION
    style &= ~win32con.WS_THICKFRAME
    win32gui.SetWindowLong(hWnd, win32con.GWL_STYLE, style)
    win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOZORDER |
                          win32con.SWP_FRAMECHANGED)

qframelesswindow.utils.win32_utils.WindowsMoveResize.toggleMaxState = toggleMaxState
qframelesswindow.windows.WindowsWindowEffect.disableBlurBehindWindow = disableBlurBehindWindow
qframelesswindow.windows.WindowsWindowEffect.removeWindowAnimation = removeWindowAnimation


def setToolTip(widget, text: str):
    widget.setToolTip(text)
    if not hasattr(widget, "newToolTipEventFilter"):
        widget.newToolTipEventFilter = ToolTipFilter(widget, 1000)
    widget.installEventFilter(widget.newToolTipEventFilter)


def removeToolTip(widget):
    if hasattr(widget, "newToolTipEventFilter"):
        widget.removeEventFilter(widget.newToolTipEventFilter)
        widget.newToolTipEventFilter.deleteLater()
        del widget.newToolTipEventFilter
    widget.setToolTip("")


QWidget.setNewToolTip = setToolTip
QWidget.removeNewToolTip = removeToolTip


def setSelectable(widget):
    widget.setTextInteractionFlags(Qt.TextSelectableByMouse)
    widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)


QLabel.setSelectable = setSelectable
