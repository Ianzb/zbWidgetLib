from ..base import *


class CustomProgressRing(QProgressBar):
    """环形进度条。

    支持确定和不确定（转圈）两种模式，包含值动画与不确定动画控制。
    """

    def __init__(self, parent=None, useAni=True, indeterminate=False,
                 drawBackground=True, duration=1000, size=80, strokeWidth=6):
        """
        :param parent: 父组件
        :param useAni: 是否在确定模式下使用值动画
        :param indeterminate: 是否为不确定模式
        :param drawBackground: 是否绘制背景
        :param duration: 动画时长（毫秒）
        :param size: 组件尺寸
        :param strokeWidth: 线条粗细
        """
        super().__init__(parent)

        # 模式与外观
        self._indeterminate = indeterminate
        self._useAni = useAni
        self._drawBackground = drawBackground
        self._duration = duration
        self._size = size
        self._strokeWidth = strokeWidth

        # 颜色
        self.lightBackgroundColor = QColor(0, 0, 0, 34 if drawBackground else 0)
        self.darkBackgroundColor = QColor(255, 255, 255, 34 if drawBackground else 0)
        self._lightBarColor = QColor()
        self._darkBarColor = QColor()

        # 动画属性
        self._animStartAngle = -180
        self._spanAngle = 0
        self._animationGroup = None

        # 值动画
        self._val = 0
        self._targetVal = 0
        self._valueAnimation = QPropertyAnimation(self, b'val', self)
        self._valueAnimation.setDuration(150)
        self._valueAnimation.setEasingCurve(QEasingCurve.OutQuad)

        self._initAnimations()

        setFont(self)
        self.setFixedSize(size, size)
        self.setTextVisible(False)

        self.valueChanged.connect(self._onValueChanged)

        if indeterminate and useAni:
            self.startIndeterminateAnimation()

    def _initAnimations(self):
        """初始化动画组。"""
        self.startAngleAni1 = QPropertyAnimation(self, b'animStartAngle', self)
        self.startAngleAni2 = QPropertyAnimation(self, b'animStartAngle', self)
        self.spanAngleAni1 = QPropertyAnimation(self, b'spanAngle', self)
        self.spanAngleAni2 = QPropertyAnimation(self, b'spanAngle', self)

        self.startAngleAniGroup = QSequentialAnimationGroup(self)
        self.spanAngleAniGroup = QSequentialAnimationGroup(self)

        self.startAngleAni1.setDuration(self._duration)
        self.startAngleAni1.setStartValue(0)
        self.startAngleAni1.setEndValue(450)

        self.startAngleAni2.setDuration(self._duration)
        self.startAngleAni2.setStartValue(450)
        self.startAngleAni2.setEndValue(1080)

        self.startAngleAniGroup.addAnimation(self.startAngleAni1)
        self.startAngleAniGroup.addAnimation(self.startAngleAni2)

        self.spanAngleAni1.setDuration(self._duration)
        self.spanAngleAni1.setStartValue(0)
        self.spanAngleAni1.setEndValue(180)

        self.spanAngleAni2.setDuration(self._duration)
        self.spanAngleAni2.setStartValue(180)
        self.spanAngleAni2.setEndValue(0)

        self.spanAngleAniGroup.addAnimation(self.spanAngleAni1)
        self.spanAngleAniGroup.addAnimation(self.spanAngleAni2)

        self._animationGroup = QParallelAnimationGroup(self)
        self._animationGroup.addAnimation(self.startAngleAniGroup)
        self._animationGroup.addAnimation(self.spanAngleAniGroup)
        self._animationGroup.setLoopCount(-1)

    def getVal(self):
        """返回内部动画值。"""
        return self._val

    def setVal(self, v: float):
        """设置内部动画值并触发更新。"""
        self._val = v
        self.setValue(v)
        self.update()

    def _onValueChanged(self, value):
        """处理 valueChanged 信号。"""
        if not self._indeterminate and self._useAni:
            if self._valueAnimation.state() == QPropertyAnimation.Running:
                self._valueAnimation.stop()

            self._valueAnimation.setStartValue(self._val)
            self._valueAnimation.setEndValue(float(value))
            self._valueAnimation.setDuration(150)
            self._valueAnimation.start()

            self._targetVal = value
            super().setValue(value)
        else:
            self._val = value
            self._targetVal = value
            super().setValue(value)
            if not self._indeterminate:
                self.update()

    def setUseAni(self, use_ani: bool):
        """启用或禁用确定模式下的值动画。"""
        self._useAni = use_ani

    def getUseAni(self):
        """返回是否启用值动画。"""
        return self._useAni

    @Property(float)
    def val(self):
        return self._val

    @val.setter
    def val(self, value: float):
        if self._val != value:
            self._val = value
            if not self._indeterminate:
                self.update()

    @Property(int)
    def animStartAngle(self):
        return self._animStartAngle

    @animStartAngle.setter
    def animStartAngle(self, angle: int):
        if self._animStartAngle != angle:
            self._animStartAngle = angle
            if self._indeterminate:
                self.update()

    @Property(int)
    def spanAngle(self):
        return self._spanAngle

    @spanAngle.setter
    def spanAngle(self, angle: int):
        if self._spanAngle != angle:
            self._spanAngle = angle
            if self._indeterminate:
                self.update()

    # 公共接口
    def isIndeterminate(self):
        """返回是否为不确定模式。"""
        return self._indeterminate

    def setIndeterminate(self, indeterminate: bool):
        """设置不确定模式并启动/停止对应动画。"""
        if self._indeterminate != indeterminate:
            self._indeterminate = indeterminate

            if indeterminate:
                self.startIndeterminateAnimation()
            else:
                self.stopIndeterminateAnimation()

            self.update()

    def isDeterminate(self):
        """返回是否为确定模式（isIndeterminate 的反义）。"""
        return not self.isIndeterminate()

    def setDetermined(self, determined: bool):
        """设置为确定模式（等价于 setIndeterminate(not determined)）。"""
        self.setIndeterminate(not bool(determined))

    setDeterminate = setDetermined

    def getDrawBackground(self):
        """返回是否绘制背景。"""
        return self._drawBackground

    def setDrawBackground(self, draw: bool):
        """设置是否绘制背景。"""
        if self._drawBackground != draw:
            self._drawBackground = draw
            self.lightBackgroundColor = QColor(0, 0, 0, 34 if draw else 0)
            self.darkBackgroundColor = QColor(255, 255, 255, 34 if draw else 0)
            self.update()

    def getDuration(self):
        """返回动画时长（毫秒）。"""
        return self._duration

    def setDuration(self, duration: int):
        """设置动画时长并更新相关动画。"""
        if self._duration != duration:
            self._duration = duration
            if hasattr(self, 'startAngleAni1'):
                self.startAngleAni1.setDuration(duration)
                self.startAngleAni2.setDuration(duration)
                self.spanAngleAni1.setDuration(duration)
                self.spanAngleAni2.setDuration(duration)

    def getSize(self):
        return self._size

    def setSize(self, size: int):
        if self._size != size:
            self._size = size
            self.setFixedSize(size, size)
            self.update()

    def getStrokeWidth(self):
        return self._strokeWidth

    def setStrokeWidth(self, width: int):
        if self._strokeWidth != width:
            self._strokeWidth = width
            self.update()

    def startIndeterminateAnimation(self):
        """启动不确定模式动画。"""
        if self._animationGroup and not self._animationGroup.state() == QPropertyAnimation.Running:
            self._animStartAngle = 0
            self._spanAngle = 0
            self._animationGroup.start()

    def stopIndeterminateAnimation(self):
        """停止不确定模式动画。"""
        if self._animationGroup:
            self._animationGroup.stop()
            self._animStartAngle = 0
            self._spanAngle = 0

    def barColor(self):
        """返回当前进度条颜色（考虑主题和自定义颜色）。"""
        if self._lightBarColor.isValid():
            return self._lightBarColor if not isDarkTheme() else self._darkBarColor
        return themeColor()

    def setCustomBarColor(self, light, dark):
        self._lightBarColor = QColor(light)
        self._darkBarColor = QColor(dark)
        self.update()

    def setCustomBackgroundColor(self, light, dark):
        self.lightBackgroundColor = QColor(light)
        self.darkBackgroundColor = QColor(dark)
        self.update()

    def _drawText(self, painter: QPainter, text: str):
        """在组件中央绘制文本。"""
        painter.setFont(self.font())
        painter.setPen(Qt.white if isDarkTheme() else Qt.black)
        painter.drawText(self.rect(), Qt.AlignCenter, text)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        cw = self._strokeWidth
        w = min(self.height(), self.width()) - cw
        rc = QRectF(cw / 2, self.height() / 2 - w / 2, w, w)

        if self._drawBackground:
            bc = self.darkBackgroundColor if isDarkTheme() else self.lightBackgroundColor
            pen = QPen(bc, cw, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawArc(rc, 0, 360 * 16)

        if self._indeterminate:
            pen = QPen(self.barColor(), cw, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)

            start_angle = -self._animStartAngle + 180
            painter.drawArc(rc, (start_angle % 360) * 16, -self._spanAngle * 16)

        else:
            if self.maximum() <= self.minimum():
                return

            progress = self._val - self.minimum()
            total = self.maximum() - self.minimum()

            if total > 0:
                degree = int(progress / total * 360)
            else:
                degree = 0

            if degree > 0:
                pen = QPen(self.barColor(), cw, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                painter.setPen(pen)

                start_angle = 90 * 16
                span_angle = -degree * 16
                painter.drawArc(rc, start_angle, span_angle)

            if self.isTextVisible() and total > 0:
                actual_progress = self.value() - self.minimum()
                progress_percent = int(actual_progress / total * 100) if total > 0 else 0
                self._drawText(painter, f"{progress_percent}%")

    def setValue(self, value: int):
        super().setValue(value)

    # Qt 属性
    indeterminate = Property(bool, isIndeterminate, setIndeterminate)
    drawBackground = Property(bool, getDrawBackground, setDrawBackground)
    duration = Property(int, getDuration, setDuration)
    size = Property(int, getSize, setSize)
    strokeWidth = Property(int, getStrokeWidth, setStrokeWidth)


class PartialProgressRing(CustomProgressRing):
    """部分圆环进度条，范围受限的转圈动画。"""

    def __init__(
            self,
            parent=None,
            useAni=True,
            indeterminate=False,
            drawBackground=True,
            startAngle=90,
            maxAngle=360,
            duration=500,
            size=80,
            strokeWidth=6
    ):
        """
        :param startAngle: 起始角度
        :param maxAngle: 最大跨度角度
        其它参数同 CustomProgressRing
        """
        super().__init__(
            parent,
            useAni,
            indeterminate,
            drawBackground,
            duration,
            size,
            strokeWidth
        )

        self._startAngle = startAngle % 360
        self._maxAngle = min(max(0, maxAngle), 360)

        self._barStart = 0.0
        self._barSpan = 0.0

        self._partialAnimationGroup = None
        self._initPartialAnimations()

        if indeterminate and useAni:
            self.startIndeterminateAnimation()

    def _initPartialAnimations(self):
        """初始化部分环动画。"""
        if self._partialAnimationGroup:
            self._partialAnimationGroup.stop()

        self.barStartAni = QPropertyAnimation(self, b"barStart", self)
        self.barStartAni.setDuration(self._duration * 2)
        self.barStartAni.setStartValue(0.0)
        self.barStartAni.setEndValue(1.0)

        max_span = min(0.5, self._maxAngle / 360.0)

        self.barSpanGrow = QPropertyAnimation(self, b"barSpan", self)
        self.barSpanGrow.setDuration(self._duration)
        self.barSpanGrow.setStartValue(0.0)
        self.barSpanGrow.setEndValue(max_span)
        self.barSpanGrow.setEasingCurve(QEasingCurve.OutQuad)

        self.barSpanShrink = QPropertyAnimation(self, b"barSpan", self)
        self.barSpanShrink.setDuration(self._duration)
        self.barSpanShrink.setStartValue(max_span)
        self.barSpanShrink.setEndValue(0.0)
        self.barSpanShrink.setEasingCurve(QEasingCurve.InQuad)

        spanGroup = QSequentialAnimationGroup(self)
        spanGroup.addAnimation(self.barSpanGrow)
        spanGroup.addAnimation(self.barSpanShrink)

        self._partialAnimationGroup = QParallelAnimationGroup(self)
        self._partialAnimationGroup.addAnimation(self.barStartAni)
        self._partialAnimationGroup.addAnimation(spanGroup)
        self._partialAnimationGroup.setLoopCount(-1)

    # Qt Property
    @Property(float)
    def barStart(self):
        return self._barStart

    @barStart.setter
    def barStart(self, value):
        self._barStart = value
        if self._indeterminate:
            self.update()

    @Property(float)
    def barSpan(self):
        return self._barSpan

    @barSpan.setter
    def barSpan(self, value):
        self._barSpan = value
        if self._indeterminate:
            self.update()

    def getStartAngle(self):
        return self._startAngle

    def setStartAngle(self, angle):
        self._startAngle = angle % 360
        self.update()

    def getMaxAngle(self):
        return self._maxAngle

    def setMaxAngle(self, angle):
        self._maxAngle = min(max(0, angle), 360)
        self._initPartialAnimations()
        if self._indeterminate:
            self.startIndeterminateAnimation()
        self.update()

    startAngle = Property(int, getStartAngle, setStartAngle)
    maxAngle = Property(int, getMaxAngle, setMaxAngle)

    def startIndeterminateAnimation(self):
        if self._partialAnimationGroup:
            self._barStart = 0.0
            self._barSpan = 0.0
            self._partialAnimationGroup.start()

    def stopIndeterminateAnimation(self):
        if self._partialAnimationGroup:
            self._partialAnimationGroup.stop()
            self._barStart = 0.0
            self._barSpan = 0.0
            self.update()

    def setIndeterminate(self, indeterminate):
        if self._indeterminate != indeterminate:
            self._indeterminate = indeterminate
            if indeterminate:
                self.startIndeterminateAnimation()
            else:
                self.stopIndeterminateAnimation()

    def isDeterminate(self):
        """返回是否为确定模式。"""
        return not self.isIndeterminate()

    def setDetermined(self, determined: bool):
        """设置为确定模式。"""
        self.setIndeterminate(not bool(determined))

    setDeterminate = setDetermined

    def _angleToQt(self, angle):
        return ((450 - angle) % 360) * 16

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        cw = self._strokeWidth
        w = min(self.width(), self.height()) - cw
        rc = QRectF(cw / 2, self.height() / 2 - w / 2, w, w)

        if self._drawBackground:
            bc = self.darkBackgroundColor if isDarkTheme() else self.lightBackgroundColor
            painter.setPen(QPen(bc, cw, Qt.SolidLine, Qt.RoundCap))
            painter.drawArc(
                rc,
                self._angleToQt(self._startAngle),
                -self._maxAngle * 16
            )

        if self._indeterminate:
            painter.setPen(QPen(self.barColor(), cw, Qt.SolidLine, Qt.RoundCap))

            start_ratio = self._barStart
            span_ratio = self._barSpan

            if start_ratio + span_ratio > 1.0:
                span_ratio = 1.0 - start_ratio

            if span_ratio <= 0:
                return

            actual_start = self._startAngle + start_ratio * self._maxAngle
            actual_span = span_ratio * self._maxAngle

            painter.drawArc(
                rc,
                self._angleToQt(actual_start),
                -actual_span * 16
            )
            return

        if self.maximum() <= self.minimum():
            return

        progress = self._val - self.minimum()
        total = self.maximum() - self.minimum()

        if total > 0:
            degree = int(progress / total * self._maxAngle)
        else:
            degree = 0

        if degree > 0:
            painter.setPen(QPen(self.barColor(), cw, Qt.SolidLine, Qt.RoundCap))
            painter.drawArc(
                rc,
                self._angleToQt(self._startAngle),
                -degree * 16
            )

        if self.isTextVisible() and total > 0:
            actual_progress = self.value() - self.minimum()
            progress_percent = int(actual_progress / total * 100) if total > 0 else 0
            self._drawText(painter, f"{progress_percent}%")


class CustomProgressBar(QProgressBar):
    """横向进度条，支持确定/不确定模式。"""

    def __init__(self, parent=None, useAni=True, indeterminate=False,
                 drawBackground=True, height=4, radius=None):
        """
        :param height: 进度条高度
        :param radius: 圆角半径
        其它参数同 CustomProgressRing
        """
        super().__init__(parent)

        self._indeterminate = indeterminate
        self._useAni = useAni
        self._drawBackground = drawBackground
        self._height = height
        self._radius = radius if radius is not None else height / 2

        self.lightBackgroundColor = QColor(0, 0, 0, 155)
        self.darkBackgroundColor = QColor(255, 255, 255, 155)
        self._lightBarColor = QColor()
        self._darkBarColor = QColor()

        self._isPaused = False
        self._isError = False

        self._val = 0
        self._valueAnimation = QPropertyAnimation(self, b'val', self)
        self._valueAnimation.setDuration(150)

        self._shortPos = 0
        self._longPos = 0
        self._indeterminateAnimationGroup = None

        self._initAnimations()

        self.setFixedHeight(height)
        self.valueChanged.connect(self._onValueChanged)
        self.setValue(0)

        if indeterminate:
            self.startIndeterminateAnimation()

    def _initAnimations(self):
        self._valueAnimation.setDuration(150)

        self.shortBarAni = QPropertyAnimation(self, b'shortPos', self)
        self.longBarAni = QPropertyAnimation(self, b'longPos', self)

        self.shortBarAni.setDuration(833)
        self.longBarAni.setDuration(1167)
        self.shortBarAni.setStartValue(0)
        self.longBarAni.setStartValue(0)
        self.shortBarAni.setEndValue(1.45)
        self.longBarAni.setEndValue(1.75)
        self.longBarAni.setEasingCurve(QEasingCurve.OutQuad)

        self.longBarAniGroup = QSequentialAnimationGroup(self)
        self.longBarAniGroup.addPause(785)
        self.longBarAniGroup.addAnimation(self.longBarAni)

        self._indeterminateAnimationGroup = QParallelAnimationGroup(self)
        self._indeterminateAnimationGroup.addAnimation(self.shortBarAni)
        self._indeterminateAnimationGroup.addAnimation(self.longBarAniGroup)
        self._indeterminateAnimationGroup.setLoopCount(-1)

    def getVal(self):
        return self._val

    def setVal(self, v: float):
        self._val = v
        self.setValue(v)
        self.update()

    @Property(float)
    def val(self):
        return self._val

    @val.setter
    def val(self, v: float):
        if self._val != v:
            self._val = v
            if not self._indeterminate:
                self.update()

    @Property(float)
    def shortPos(self):
        return self._shortPos

    @shortPos.setter
    def shortPos(self, p):
        if self._shortPos != p:
            self._shortPos = p
            if self._indeterminate:
                self.update()

    @Property(float)
    def longPos(self):
        return self._longPos

    @longPos.setter
    def longPos(self, p):
        if self._longPos != p:
            self._longPos = p
            if self._indeterminate:
                self.update()

    def isIndeterminate(self):
        """返回是否为不确定模式。"""
        return self._indeterminate

    def setIndeterminate(self, indeterminate: bool):
        """设置不确定模式并启动/停止对应动画。"""
        if self._indeterminate != indeterminate:
            self._indeterminate = indeterminate

            if indeterminate:
                self.startIndeterminateAnimation()
            else:
                self.stopIndeterminateAnimation()

            self.update()

    def isDeterminate(self):
        """返回是否为确定模式。"""
        return not self.isIndeterminate()

    def setDetermined(self, determined: bool):
        """设置为确定模式。"""
        self.setIndeterminate(not bool(determined))

    setDeterminate = setDetermined

    def isUseAni(self):
        return self._useAni

    def setUseAni(self, isUse: bool):
        if self._useAni != isUse:
            self._useAni = isUse
            self.update()

    def getDrawBackground(self):
        return self._drawBackground

    def setDrawBackground(self, draw: bool):
        if self._drawBackground != draw:
            self._drawBackground = draw
            self.update()

    def getHeight(self):
        return self._height

    def setHeight(self, height: int):
        if self._height != height:
            self._height = height
            self.setFixedHeight(height)
            self._radius = height / 2
            self.update()

    def getRadius(self):
        return self._radius

    def setRadius(self, radius: int):
        if self._radius != radius:
            self._radius = radius
            self.update()

    def _onValueChanged(self, value):
        if not self._indeterminate and self._useAni:
            if self._valueAnimation.state() == QPropertyAnimation.Running:
                self._valueAnimation.stop()

            self._valueAnimation.setStartValue(self._val)
            self._valueAnimation.setEndValue(float(value))
            self._valueAnimation.start()

            super().setValue(value)
        else:
            self._val = value
            super().setValue(value)
            if not self._indeterminate:
                self.update()

    def startIndeterminateAnimation(self):
        """启动不确定模式动画。"""
        if (self._indeterminateAnimationGroup and
                not self._indeterminateAnimationGroup.state() == QParallelAnimationGroup.Running):
            self._shortPos = 0
            self._longPos = 0
            self._indeterminateAnimationGroup.start()

    def stopIndeterminateAnimation(self):
        """停止不确定模式动画。"""
        if self._indeterminateAnimationGroup:
            self._indeterminateAnimationGroup.stop()
            self._shortPos = 0
            self._longPos = 0
            self.update()

    def lightBarColor(self):
        return self._lightBarColor if self._lightBarColor.isValid() else themeColor()

    def darkBarColor(self):
        return self._darkBarColor if self._darkBarColor.isValid() else themeColor()

    def setCustomBarColor(self, light, dark):
        self._lightBarColor = QColor(light)
        self._darkBarColor = QColor(dark)
        self.update()

    def setCustomBackgroundColor(self, light, dark):
        self.lightBackgroundColor = QColor(light)
        self.darkBackgroundColor = QColor(dark)
        self.update()

    def resume(self):
        self._isPaused = False
        self._isError = False
        self.update()

    def pause(self):
        self._isPaused = True
        if self._indeterminate:
            self._indeterminateAnimationGroup.pause()
        self.update()

    def setPaused(self, isPaused: bool):
        if self._isPaused != isPaused:
            self._isPaused = isPaused
            if self._indeterminate:
                if isPaused:
                    self._indeterminateAnimationGroup.pause()
                else:
                    self._indeterminateAnimationGroup.resume()
            self.update()

    def isPaused(self):
        return self._isPaused

    def error(self):
        self._isError = True
        if self._indeterminate:
            self._indeterminateAnimationGroup.stop()
        self.update()

    def setError(self, isError: bool):
        if self._isError != isError:
            self._isError = isError
            if isError:
                self.error()
            else:
                self.resume()

    def isError(self):
        return self._isError

    def barColor(self):
        if self.isPaused():
            return QColor(252, 225, 0) if isDarkTheme() else QColor(157, 93, 0)

        if self.isError():
            return QColor(255, 153, 164) if isDarkTheme() else QColor(196, 43, 28)

        return self.darkBarColor() if isDarkTheme() else self.lightBarColor()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        if self._drawBackground:
            bc = self.darkBackgroundColor if isDarkTheme() else self.lightBackgroundColor
            painter.setPen(bc)
            from math import floor
            y = floor(self.height() / 2)
            painter.drawLine(0, y, self.width(), y)

        if self._indeterminate:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.barColor())

            x = int((self._shortPos - 0.4) * self.width())
            w = int(0.4 * self.width())
            painter.drawRoundedRect(x, 0, w, self.height(), self._radius, self._radius)

            x = int((self._longPos - 0.6) * self.width())
            w = int(0.6 * self.width())
            painter.drawRoundedRect(x, 0, w, self.height(), self._radius, self._radius)

        else:
            if self.minimum() >= self.maximum():
                return

            painter.setPen(Qt.NoPen)
            painter.setBrush(self.barColor())
            w = int(self._val / (self.maximum() - self.minimum()) * self.width())
            painter.drawRoundedRect(0, 0, w, self.height(), self._radius, self._radius)

    def setValue(self, value: int):
        super().setValue(value)

    # Qt 属性
    indeterminate = Property(bool, isIndeterminate, setIndeterminate)
    useAni = Property(bool, isUseAni, setUseAni)
    drawBackground = Property(bool, getDrawBackground, setDrawBackground)
    heightProp = Property(int, getHeight, setHeight)
    radius = Property(float, getRadius, setRadius)
    val = Property(float, getVal, setVal)
