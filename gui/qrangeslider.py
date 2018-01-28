# -*- coding: utf-8 -*-

"""
***************************************************************************
    qrangeslider.py
    ---------------------
    Date                 : August 2017
    Copyright            : (C) 2017-2018 by Alexander Bruy
    Email                : alexander dot bruy at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy'
__date__ = 'August 2017'
__copyright__ = '(C) 2017-2018, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtGui import (QPainter,
                             QPen,
                             QPalette,
                             QLinearGradient
                            )
from qgis.PyQt.QtCore import (pyqtProperty,
                              pyqtSignal,
                              Q_ENUMS,
                              Qt,
                              QEvent,
                              QRect,
                              QPoint
                             )
from qgis.PyQt.QtWidgets import (QSlider,
                                 QStyle,
                                 QStylePainter,
                                 QStyleOptionSlider)


class QRangeSlider(QSlider):

    class HandleMovement:
        FreeMovement = 0
        NoCrossing = 1
        NoOverlapping = 2

    class ActiveHandle:
        LowerHandle = 0
        UpperHandle = 1
        NoHandle = 2

    Q_ENUMS(HandleMovement)
    Q_ENUMS(ActiveHandle)

    lowerValueChanged = pyqtSignal(int)
    upperValueChanged = pyqtSignal(int)
    intervalChanged = pyqtSignal(int, int)

    sliderPressed = pyqtSignal(int)

    HANDLES = [ActiveHandle.LowerHandle, ActiveHandle.UpperHandle]

    def __init__(self, parent=None):
        super(QRangeSlider, self).__init__(parent)

        self.lower = self.minimum()
        self.upper = self.maximum()

        self.lowerPosition = self.lower
        self.upperPosition = self.upper

        self.movement = QRangeSlider.HandleMovement.FreeMovement
        self.activeHandle = QRangeSlider.ActiveHandle.NoHandle

        self.pressedControl = QStyle.SC_None

        self.hoverRect = QRect()
        self.hoverControl = QStyle.SC_None

        self.clickOffset = 0

    def lower(self):
        return self.lower

    def setLower(self, value):
        self.lower = value
        self.update()
        self.lowerValueChanged.emit(value)

    #lower = pyqtProperty("double", lower, setLower, notify=lowerValueChanged)

    def upper(self):
        return self.upper

    def setUpper(self, value):
        self.upper = value
        self.update()
        self.upperValueChanged.emit(value)

    #upper = pyqtProperty("double", upper, setUpper, notify=upperValueChanged)

    def interval(self):
        return [self.lower, self.upper]

    def setInterval(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.update()
        self.intervalChanged.emit(lower, upper)

    #interval = pyqtProperty("double, double", interval, setInterval, notify=intervalChanged)

    def paintEvent(self, event):
        painter = QPainter(self)

        opt = QStyleOptionSlider()
        self.initStyleOption(opt)

        # first draw groove with or without ticks
        opt.subControls = QStyle.SC_SliderGroove

        if self.tickPosition() != self.NoTicks:
            opt.subControls |= QStyle.SC_SliderTickmarks

        if self.pressedControl != QStyle.SC_SliderHandle:
            opt.activeSubControls = self.pressedControl
            opt.state |= QStyle.State_Sunken;
        elif self.hoverControl != QStyle.SC_SliderHandle:
            opt.activeSubControls = self.hoverControl

        self.style().drawComplexControl(QStyle.CC_Slider, opt, painter)

        # then draw interval
        # first obtain position of the lower and upper handles
        opt.sliderPosition = self.lower
        lowerHandleRect = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)
        lowerHandlePosition = self._pick(lowerHandleRect.center())
        opt.sliderPosition = self.upper
        upperHandleRect = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)
        upperHandlePosition = self._pick(upperHandleRect.center())

        minPosition = min(lowerHandlePosition, upperHandlePosition)
        maxPosition = max(lowerHandlePosition, upperHandlePosition)
        center = QRect(lowerHandleRect.center(), upperHandleRect.center()).center()
        if self.orientation() == Qt.Horizontal:
            spanRect = QRect(QPoint(minPosition, center.y() - 2), QPoint(maxPosition, center.y() + 1))
        else:
            spanRect = QRect(QPoint(center.x() - 2, minPosition), QPoint(center.x() + 1, maxPosition))

        grooveRect = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)

        #painter.setPen(QPen(self.palette().color(QPalette.Dark).lighter(110), 0))
        if opt.orientation == Qt.Horizontal:
            grooveRect.adjust(0, 0, -1, 0)
            self._setupPainter(painter, grooveRect.center().x(), grooveRect.top(), grooveRect.center().x(), grooveRect.bottom())
        else:
            grooveRect.adjust(0, 0, 0, -1)
            self._setupPainter(painter, grooveRect.left(), grooveRect.center().y(), grooveRect.right(), grooveRect.center().y())

        painter.drawRect(spanRect.intersected(grooveRect))

        # finally draw handles
        opt.subControls = QStyle.SC_SliderHandle
        for handle, value in zip(self.HANDLES, self.interval()):
            if self.activeHandle == handle and self.pressedControl == QStyle.SC_SliderHandle:
                opt.activeSubControls = self.pressedControl
                opt.state |= QStyle.State_Sunken
            elif self.activeHandle == handle and self.hoverControl == QStyle.SC_SliderHandle:
                opt.activeSubControls = self.hoverControl

            opt.sliderPosition = value
            opt.sliderValue = value
            self.style().drawComplexControl(QStyle.CC_Slider, opt, painter)

    def mousePressEvent(self, event):
        if self.maximum() == self.minimum() or event.buttons() ^ event.button():
            event.ignore()
            return

        event.accept()
        if event.button():
            oldHandle = self.activeHandle

            # determine which handle was pressed
            opt = QStyleOptionSlider()
            self.initStyleOption(opt)

            for handle, value in zip(self.HANDLES, self.interval()):
                opt.sliderPosition = value
                control = self.style().hitTestComplexControl(QStyle.CC_Slider, opt, event.pos(), self)
                if control == QStyle.SC_SliderHandle:
                    self.activeHandle = handle
                    self.pressedControl = control

                    sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)
                    self.clickOffset = self._pick(event.pos() - sr.topLeft())
                    self.setSliderDown(True)
                    self.sliderPressed.emit(self.activeHandle)
                    break

            if self.activeHandle != oldHandle:
                self.update()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        if self.pressedControl == QStyle.SC_None or event.buttons():
            event.ignore()
            return

        event.accept()
        oldPressed = self.pressedControl
        oldHandle = self.activeHandle
        self.pressedControl = QStyle.SC_None
        if oldPressed == QStyle.SC_SliderHandle:
            self.setSliderDown(False)
            self.activeHandle = QRangeSlider.ActiveHandle.NoHandle

        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        opt.subControls = oldPressed
        if oldHandle == QRangeSlider.ActiveHandle.LowerHandle:
            opt.sliderPosition = self.lower
        elif oldHandle == QRangeSlider.ActiveHandle.UpperHandle:
            opt.sliderPosition = self.upper
        self.update(self.style().subControlRect(QStyle.CC_Slider, opt, oldPressed, self))

    def mouseMoveEvent(self, event):
        if self.pressedControl != QStyle.SC_SliderHandle:
            event.ignore()
            return

        event.accept()
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)

        newPosition = self._pixelPosToRangeValue(self._pick(event.pos()) - self.clickOffset)

        # move active handle
        if self.activeHandle == QRangeSlider.ActiveHandle.LowerHandle:
            if self.movement == QRangeSlider.HandleMovement.NoCrossing:
                newPosition = min(newPosition, self.upper)
            elif self.movement == QRangeSlider.HandleMovement.NoOverlapping:
                newPosition = min(newPosition, self.upper - 1)

            if self.movement == QRangeSlider.HandleMovement.FreeMovement and newPosition > self.upper:
                self._swapHandles()
        elif self.activeHandle == QRangeSlider.ActiveHandle.UpperHandle:
            if self.movement == QRangeSlider.HandleMovement.NoCrossing:
                newPosition = max(newPosition, self.lower)
            elif self.movement == QRangeSlider.HandleMovement.NoOverlapping:
                newPosition = max(newPosition, self.lower + 1)

            if self.movement == QRangeSlider.HandleMovement.FreeMovement and newPosition < self.lower:
                self._swapHandles()

        self._setSliderPosition(newPosition, self.activeHandle)

    def event(self, event):
        eventType = event.type()
        if eventType in (QEvent.HoverEnter, QEvent.HoverLeave, QEvent.HoverMove):
            self._updateHoverControl(event.pos())

        return super(QRangeSlider, self).event(event)

    def _pick(self, point):
        return point.x() if self.orientation() == Qt.Horizontal else point.y()

    def _pixelPosToRangeValue(self, pos):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)

        gr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)
        if self.orientation() == Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1

        return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), pos - sliderMin,
                                              sliderMax - sliderMin, opt.upsideDown)

    def _updateHoverControl(self, pos):
        lastHoverRect = self.hoverRect
        lastHoverControl = self.hoverControl
        doesHover = self.testAttribute(Qt.WA_Hover)
        if lastHoverControl != self._newHoverControl(pos) and doesHover:
            self.update(lastHoverRect)
            self.update(self.hoverRect)
            return True

        return not doesHover

    def _newHoverControl(self, pos):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)

        opt.subControls = QStyle.SC_All
        grooveRect = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        tickmarksRect = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderTickmarks, self)
        opt.sliderPosition = self.lower
        lowerHandleRect = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)
        opt.sliderPosition = self.upper
        upperHandleRect = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)

        if lowerHandleRect.contains(pos):
            self.hoverRect = lowerHandleRect
            self.hoverControl = QStyle.SC_SliderHandle
        if upperHandleRect.contains(pos):
            self.hoverRect = upperHandleRect
            self.hoverControl = QStyle.SC_SliderHandle
        elif grooveRect.contains(pos):
            self.hoverRect = grooveRect
            self.hoverControl = QStyle.SC_SliderGroove
        elif tickmarksRect.contains(pos):
            self.hoverRect = tickmarksRect
            self.hoverControl = QStyle.SC_SliderTickmarks
        else:
            self.hoverRect = QRect()
            self.hoverControl = QStyle.SC_None

        return self.hoverControl

    def _setupPainter(self, painter, x1, y1, x2, y2):
        highlight = self.palette().color(QPalette.Highlight)
        gradient = QLinearGradient(x1, y1, x2, y2)
        gradient.setColorAt(0, highlight.darker(120))
        gradient.setColorAt(1, highlight.lighter(108))
        painter.setBrush(gradient)

        if self.orientation() == Qt.Horizontal:
            painter.setPen(QPen(highlight.darker(130), 0))
        else:
            painter.setPen(QPen(highlight.darker(150), 0))

    def _setSliderPosition(self, position, handle):
        if handle == QRangeSlider.ActiveHandle.LowerHandle:
            self.lower = position
            self.lowerValueChanged.emit(position)
        elif handle == QRangeSlider.ActiveHandle.UpperHandle:
            self.upper = position
            self.upperValueChanged.emit(position)

        self.update()

    def _swapHandles(self):
        self.lower, self.upper = self.upper, self.lower
        if self.activeHandle == QRangeSlider.ActiveHandle.UpperHandle:
            self.activeHandle = QRangeSlider.ActiveHandle.LowerHandle
        else:
            self.activeHandle = QRangeSlider.ActiveHandle.UpperHandle
