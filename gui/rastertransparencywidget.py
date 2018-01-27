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
from qgis.core import QgsMapLayer
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
        return layer.type() == QgsMapLayer.RasterLayer

    def createWidget(self, layer, canvas, dockMode, parent):
        return RasterTransparencyWidget(layer, canvas, parent)

    def tr(self, text):
        return QCoreApplication.translate("TransparencyPanelFactory", text)


class RasterTransparencyWidget(QgsMapLayerConfigWidget, WIDGET):
    def __init__(self, layer, canvas, parent=None):
        super(RasterTransparencyWidget, self).__init__(layer, canvas, parent)
        self.setupUi(self)

    def syncToLayer(self):
        pass

    def apply(self):
        pass
