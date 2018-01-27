# -*- coding: utf-8 -*-

"""
***************************************************************************
    rastertransparencyplugin.py
    ---------------------
    Date                 : April 2011
    Copyright            : (C) 2011-2018 by Alexander Bruy
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
__date__ = 'April 2011'
__copyright__ = '(C) 2011-2018, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


import os

from qgis.PyQt.QtCore import Qt, QCoreApplication, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsApplication
from qgis.gui import QgsDockWidget

from rastertransparency.gui.rastertransparencywidget import RasterTransparencyWidget
from rastertransparency.gui.aboutdialog import AboutDialog

pluginPath = os.path.dirname(__file__)


class RasterTransparencyPlugin:

    def __init__(self, iface):
        self.iface = iface

        locale = QgsApplication.locale()
        qmPath = "{}/i18n/photo2shape_{}.qm".format(pluginPath, locale)

        if os.path.exists(qmPath):
            self.translator = QTranslator()
            self.translator.load(qmPath)
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        self.actionDock = QAction(self.tr("Raster Transparency"), self.iface.mainWindow())
        self.actionDock.setIcon(QIcon(os.path.join(pluginPath, "icons", "rastertransparency.png")))
        self.actionDock.setCheckable(True)
        self.actionDock.setObjectName("toggleRasterTransparecy")
        self.actionDock.toggled.connect(self.rasterTransparencyDock)

        self.actionAbout = QAction(self.tr("About RasterTransparency…"), self.iface.mainWindow())
        self.actionAbout.setIcon(QgsApplication.getThemeIcon("/mActionHelpContents.svg"))
        self.actionAbout.setObjectName("aboutRasterTransparency")
        self.actionAbout.triggered.connect(self.about)

        self.iface.addRasterToolBarIcon(self.actionDock)
        self.iface.addPluginToRasterMenu(self.tr("Raster transparency"), self.actionDock)
        self.iface.addPluginToRasterMenu(self.tr("Raster transparency"), self.actionAbout)

        self.dockWidget = QgsDockWidget()
        self.dockWidget.setWindowTitle(self.tr("Raster transparency"))
        self.dockWidget.setObjectName("RasterTransparency")

        self.transparencyWidget = RasterTransparencyWidget()
        self.dockWidget.setWidget(self.transparencyWidget)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
        self.dockWidget.hide()
        self.dockWidget.visibilityChanged.connect(self.actionDock.setChecked)

        self.iface.currentLayerChanged.connect(self.setTransparencyDockLayer)

    def unload(self):
        self.iface.currentLayerChanged.disconnect(self.setTransparencyDockLayer)

        self.iface.removeRasterToolBarIcon(self.actionDock)
        self.iface.removePluginRasterMenu(self.tr("Raster transparency"), self.actionDock)
        self.iface.removePluginRasterMenu(self.tr("Raster transparency"), self.actionAbout)

        self.dockWidget.close()
        del self.dockWidget
        self.dockWidget = None

    def rasterTransparencyDock(self, enabled):
        self.dockWidget.setUserVisible(enabled)
        self.setTransparencyDockLayer(self.iface.activeLayer())

    def setTransparencyDockLayer(self, layer):
        if layer is None:
            return

        self.transparencyWidget.setEnabled(True)
        if self.dockWidget.isVisible():
            self.transparencyWidget.setLayer(layer)

    #~ def layerChanged(self):
        #~ layer = self.iface.activeLayer()

        #~ if layer is None:
            #~ return

        #~ if layer.type() != QgsMapLayer.RasterLayer:
            #~ self.dockWidget.disableOrEnableControls(False)
            #~ return

        #~ if layer.providerType() not in ["gdal", "grass"]:
            #~ self.dockWidget.disableOrEnableControls(False)
            #~ return

        #~ if layer.bandCount() > 1 and layer.renderer().type() not in self.singleBandStyles:
            #~ self.dockWidget.disableOrEnableControls(False)
            #~ return

        #~ band = self.layer.renderer().usesBands()[0]
        #~ stat = self.layer.dataProvider().bandStatistics(band)
        #~ maxValue = int(stat.maximumValue)
        #~ minValue = int(stat.minimumValue)
        #~ self.dockWidget.updateSliders(maxValue, minValue)

        #~ self.dockWidget.disableOrEnableControls(True)

    def about(self):
        d = AboutDialog()
        d.exec_()

    def tr(self, text):
        return QCoreApplication.translate("RasterTransparency", text)
