# -*- coding: utf-8 -*-

#******************************************************************************
#
# RasterTransparency
# ---------------------------------------------------------
# Interactively setup raster transparency
#
# Copyright (C) 2010-2013 Alexander Bruy (alexander.bruy@gmail.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************


from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from ui_rastertransparencydockwidgetbase import Ui_RasterTransparencyDockWidget


class RasterTransparencyDockWidget(QDockWidget, Ui_RasterTransparencyDockWidget, object):
    def __init__(self, plugin):
        QDockWidget.__init__(self, None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.plugin = plugin
        self.maxVal = 0
        self.minVal = 0

        # connect signals and slots
        QObject.connect(self.chkManualUpdate, SIGNAL("stateChanged(int)"), self.__toggleRefresh)
        QObject.connect(self.btnRefresh, SIGNAL("clicked()"), self.updateRasterTransparency)

        QObject.connect(self.sliderStart, SIGNAL("valueChanged(int)"), self.__updateSpinStart)
        QObject.connect(self.spinStart, SIGNAL("valueChanged(int)"), self.__updateSliderStart)
        QObject.connect(self.sliderEnd, SIGNAL("valueChanged(int)"), self.__updateSpinEnd)
        QObject.connect(self.spinEnd, SIGNAL("valueChanged(int)"), self.__updateSliderEnd)

        settings = QSettings("NextGIS", "RasterTransparency")
        self.chkManualUpdate.setChecked(settings.value("manualUpdate", False).toBool())

    def updateRasterTransparency(self):
        transparencyList = []

        if self.sliderStart.value() != 0:
            transparencyList.extend(self.generateTransparencyList(0, self.sliderStart.value()))

        if self.sliderEnd.value() != self.maxVal:
            transparencyList.extend(self.generateTransparencyList(self.sliderEnd.value(), self.maxVal))

        # update layer transparency
        layer = self.plugin.iface.mapCanvas().currentLayer()
        layer.setCacheImage(None)
        layer.rasterTransparency().setTransparentSingleValuePixelList(transparencyList)
        self.plugin.iface.mapCanvas().refresh()

    def __updateSpinStart(self, value):
        endValue = self.sliderEnd.value()
        if value >= endValue:
            self.spinStart.setValue(endValue - 1)
            self.sliderStart.setValue(endValue - 1)
            return
        self.spinStart.setValue(value)

        if not self.chkManualUpdate.isChecked():
            self.updateRasterTransparency()

    def __updateSliderStart(self, value):
        endValue = self.spinEnd.value()
        if value >= endValue:
            self.spinStart.setValue(endValue - 1)
            self.sliderStart.setValue(endValue - 1)
            return
        self.sliderStart.setValue(value)

    def __updateSpinEnd(self, value):
        startValue = self.sliderStart.value()
        if value <= startValue:
            self.spinEnd.setValue(startValue + 1)
            self.sliderEnd.setValue(startValue + 1)
            return
        self.spinEnd.setValue(value)

        if not self.chkManualUpdate.isChecked():
            self.updateRasterTransparency()

    def __updateSliderEnd(self, value):
        startValue = self.sliderStart.value()
        if value <= startValue:
            self.spinEnd.setValue(startValue + 1)
            self.sliderEnd.setValue(startValue + 1)
            return
        self.sliderEnd.setValue(value)

    def __toggleRefresh(self):
        settings = QSettings("NextGIS", "RasterTransparency")
        settings.setValue("manualUpdate", self.chkManualUpdate.isChecked())

        if self.chkManualUpdate.isChecked():
            self.btnRefresh.setEnabled(True)
            QObject.disconnect(self.sliderStart, SIGNAL("sliderReleased ()"), self.updateRasterTransparency)
            QObject.disconnect(self.sliderEnd, SIGNAL("sliderReleased ()"), self.updateRasterTransparency)
        else:
            self.btnRefresh.setEnabled(False)
            QObject.connect(self.sliderStart, SIGNAL("sliderReleased ()"), self.updateRasterTransparency)
            QObject.connect(self.sliderEnd, SIGNAL("sliderReleased ()"), self.updateRasterTransparency)

    def disableOrEnableControls(self, disable):
        self.label.setEnabled(disable)
        self.sliderStart.setEnabled(disable)
        self.spinStart.setEnabled(disable)
        self.label_2.setEnabled(disable)
        self.sliderEnd.setEnabled(disable)
        self.spinEnd.setEnabled(disable)

    def updateSliders(self, maxValue, minValue):
        self.maxVal = int(maxValue)
        self.minVal = int(minValue)

        self.spinStart.setMaximum(int(self.maxVal))
        self.spinStart.setMinimum(int(self.minVal))
        self.spinStart.setValue(int(self.minVal))

        self.spinEnd.setMaximum(int(self.maxVal))
        self.spinEnd.setMinimum(int(self.minVal))
        self.spinEnd.setValue(int(self.maxVal))

        self.sliderStart.setMinimum(int(self.minVal))
        self.sliderStart.setMaximum(int(self.maxVal))
        self.sliderStart.setValue(int(self.minVal))

        self.sliderEnd.setMinimum(int(self.minVal))
        self.sliderEnd.setMaximum(int(self.maxVal))
        self.sliderEnd.setValue(int(self.maxVal))

    def generateTransparencyList(self, minVal, maxVal):
        trList = []
        for v in range(int(minVal), int(maxVal + 1)):
            tr = QgsRasterTransparency.TransparentSingleValuePixel()
            tr.pixelValue = v
            tr.percentTransparent = 100
            trList.append(tr)
        return trList
