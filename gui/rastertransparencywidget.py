# -*- coding: utf-8 -*-

"""
***************************************************************************
    rastertransparencywidget.py
    ---------------------
    Date                 : January 2018
    Copyright            : (C) 2018 by Alexander Bruy
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
__date__ = 'January 2018'
__copyright__ = '(C) 2018, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.PyQt import uic
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QCoreApplication

from qgis.gui import QgsMapLayerConfigWidgetFactory, QgsMapLayerConfigWidget
from qgis.core import QgsMapLayer, QgsRasterBandStats, QgsRasterTransparency, QgsMessageLog
from qgis.utils import iface

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(os.path.join(pluginPath, "ui", "rastertransparencywidgetbase.ui"))


class TransparencyPanelFactory(QgsMapLayerConfigWidgetFactory):
    def icon(self):
        return QIcon(os.path.join(pluginPath, "icons", "rastertransparency.png"))

    def title(self):
        return self.tr("Raster Transparency")

    def supportsStyleDock(self):
        return True

    def supportsLayer(self, layer):
        return layer.type() == QgsMapLayer.RasterLayer and len(layer.renderer().usesBands()) == 1

    def createWidget(self, layer, canvas, dockMode, parent):
        return RasterTransparencyWidget(layer, canvas, parent)

    def tr(self, text):
        return QCoreApplication.translate("TransparencyPanelFactory", text)


class RasterTransparencyWidget(QgsMapLayerConfigWidget, WIDGET):
    def __init__(self, layer, canvas, parent=None):
        super(RasterTransparencyWidget, self).__init__(layer, canvas, parent)
        self.setupUi(self)

        self.layer = layer
        self.canvas = canvas

        self.statistics = None
        self.pixelList = None

        self.spnLower.valueChanged.connect(self.sliderValues.setLower)
        self.spnUpper.valueChanged.connect(self.sliderValues.setUpper)

        self.sliderValues.lowerValueChanged.connect(self.spnLower.setValue)
        self.sliderValues.upperValueChanged.connect(self.spnUpper.setValue)

        self.spnLower.valueChanged.connect(self.widgetChanged.emit)
        self.spnUpper.valueChanged.connect(self.widgetChanged.emit)

        self.syncToLayer()

    def syncToLayer(self):
        band = self.layer.renderer().usesBands()[0]
        self.statistics = self.layer.dataProvider().bandStatistics(band, QgsRasterBandStats.Min | QgsRasterBandStats.Max)

        self.spnLower.setRange(int(self.statistics.minimumValue), int(self.statistics.maximumValue))
        self.spnUpper.setRange(int(self.statistics.minimumValue), int(self.statistics.maximumValue))
        self.sliderValues.setRange(int(self.statistics.minimumValue), int(self.statistics.maximumValue))

        # adjust controls to current transparency
        self.pixelList = self.layer.renderer().rasterTransparency().transparentSingleValuePixelList()
        if len(self.pixelList) == 0:
            self.spnLower.setValue(int(self.statistics.minimumValue))
            self.spnUpper.setValue(int(self.statistics.maximumValue))
            self.sliderValues.setInterval(int(self.statistics.minimumValue), int(self.statistics.maximumValue))
        elif len(self.pixelList) == 1:
            self.spnLower.setValue(int(self.pixelList[0].max))
        elif len(self.pixelList) == 2:
            self.spnLower.setValue(int(self.pixelList[0].max))
            self.spnUpper.setValue(int(self.pixelList[1].min))
        else:
            self.spnLower.setValue(int(self.pixelList[0].max))
            self.spnUpper.setValue(int(self.pixelList[1].min))
            QgsMessageLog.logMessage(self.tr("More than 2 transparency intervals defined."),
                                     self.tr("Raster transparency"))

    def apply(self):
        pixels = []
        if self.spnLower.value() != int(self.statistics.minimumValue):
            transparentPixel = QgsRasterTransparency.TransparentSingleValuePixel()
            transparentPixel.min = self.statistics.minimumValue
            transparentPixel.max = self.spnLower.value()
            transparentPixel.percentTransparent = 100
            pixels.append(transparentPixel)

        if self.spnUpper.value() != int(self.statistics.maximumValue):
            transparentPixel = QgsRasterTransparency.TransparentSingleValuePixel()
            transparentPixel.min = self.spnUpper.value()
            transparentPixel.max = self.statistics.maximumValue
            transparentPixel.percentTransparent = 100
            pixels.append(transparentPixel)

        if len(pixels) == 0:
            return

        renderer = self.layer.renderer()
        rasterTransparency = QgsRasterTransparency()

        if len(self.pixelList) <= 2:
            rasterTransparency.setTransparentSingleValuePixelList(pixels)
        else:
            for i, p in enumerate(pixels):
                self.pixelList[i] = p
            rasterTransparency.setTransparentSingleValuePixelList(self.pixelList)

        renderer.setRasterTransparency(rasterTransparency)
