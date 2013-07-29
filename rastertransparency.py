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


import os
import ConfigParser

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from rastertransparencydockwidget import *

import resources_rc

class RasterTransparencyPlugin(object):

    singleBandStyles = ["paletted",
                        "singlebandgray",
                        "singlebandpseudocolor"
                       ]

    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        self.layer = None
        self.toolBar = None

        self.qgsVersion = unicode(QGis.QGIS_VERSION_INT)

        userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/raster_transparency"
        systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/raster_transparency"

        overrideLocale = bool(QSettings().value("locale/overrideFlag", False))
        if not overrideLocale:
            localeFullName = QLocale.system().name()
        else:
            localeFullName = QSettings().value("locale/userLocale", "")

        if QFileInfo(userPluginPath).exists():
            translationPath = userPluginPath + "/i18n/rastertransparency_" + localeFullName + ".qm"
        else:
            translationPath = systemPluginPath + "/i18n/rastertransparency_" + localeFullName + ".qm"

        self.localePath = translationPath
        if QFileInfo(self.localePath).exists():
            self.translator = QTranslator()
            self.translator.load(self.localePath)
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        if int(self.qgsVersion) < 10900:
            qgisVersion = self.qgsVersion[0] + "." + self.qgsVersion[2] + "." + self.qgsVersion[3]
            QMessageBox.warning(self.iface.mainWindow(),
                                "RasterTransparency",
                                QCoreApplication.translate("RasterTransparency", "QGIS version detected: ") + qgisVersion +
                                QCoreApplication.translate("RasterTransparency", "This version of Raster Transparency requires at least QGIS version 2.0.\nPlugin will not be enabled."))
            return None

        self.dockWidget = None

        self.actionDock = QAction(QIcon(":/icons/rastertransparency.png"), "RasterTransparency", self.iface.mainWindow())
        self.actionDock.setStatusTip(QCoreApplication.translate("RasterTransparency", "Show/hide RasterTransparency dockwidget"))
        self.actionDock.setWhatsThis(QCoreApplication.translate("RasterTransparency", "Show/hide RasterTransparency dockwidget"))
        self.actionDock.setCheckable(True)

        self.actionAbout = QAction(QIcon(":/icons/about.png"), "About", self.iface.mainWindow())
        self.actionAbout.setStatusTip(QCoreApplication.translate("RasterTransparency", "About Raster Transparency"))
        self.actionAbout.setWhatsThis(QCoreApplication.translate("RasterTransparency", "About Raster Transparency"))

        self.actionDock.triggered.connect(self.showHideDockWidget)
        self.actionAbout.triggered.connect(self.about)

        self.iface.addRasterToolBarIcon(self.actionDock)
        self.iface.addPluginToRasterMenu(QCoreApplication.translate("RasterTransparency", "Raster transparency"), self.actionDock)
        self.iface.addPluginToRasterMenu(QCoreApplication.translate("RasterTransparency", "Raster transparency"), self.actionAbout)

        self.dockWidget = RasterTransparencyDockWidget(self)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
        self.dockWidget.visibilityChanged.connect(self.__dockVisibilityChanged)

        self.iface.currentLayerChanged.connect(self.layerChanged)
        self.layerChanged()

    def unload(self):
        self.iface.currentLayerChanged.disconnect(self.layerChanged)

        self.iface.removeRasterToolBarIcon(self.actionDock)
        self.iface.removePluginRasterMenu(QCoreApplication.translate("RasterTransparency", "Raster transparency"), self.actionDock)
        self.iface.removePluginRasterMenu(QCoreApplication.translate("RasterTransparency", "Raster transparency"), self.actionAbout)

        self.dockWidget.close()
        del self.dockWidget
        self.dockWidget = None

    def showHideDockWidget(self):
        if self.dockWidget.isVisible():
            self.dockWidget.hide()
        else:
            self.dockWidget.show()

    def layerChanged(self):
        self.layer = self.iface.activeLayer()

        if self.layer is None:
            return

        if self.layer.type() != QgsMapLayer.RasterLayer:
            self.dockWidget.disableOrEnableControls(False)
            return

        if self.layer.providerType() not in ["gdal", "grass"]:
            self.dockWidget.disableOrEnableControls(False)
            return

        if self.layer.bandCount() > 1 and self.layer.renderer().type() not in self.singleBandStyles:
            self.dockWidget.disableOrEnableControls(False)
            return

        band = self.layer.renderer().usesBands()[0]
        stat = self.layer.dataProvider().bandStatistics(band)
        maxValue = int(stat.maximumValue)
        minValue = int(stat.minimumValue)
        self.dockWidget.updateSliders(maxValue, minValue)

        self.dockWidget.disableOrEnableControls(True)

    def about(self):
        dlgAbout = QDialog()
        dlgAbout.setWindowTitle(QApplication.translate("RasterTransparency", "About Raster Transparency", "Window title"))
        lines = QVBoxLayout(dlgAbout)
        title = QLabel(QApplication.translate("RasterTransparency", "<b>Raster Transparency</b>"))
        title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        lines.addWidget(title)

        cfg = ConfigParser.SafeConfigParser()
        cfg.read(os.path.join(os.path.dirname(__file__), "metadata.txt"))
        version = cfg.get("general", "version")

        version = QLabel(QApplication.translate("RasterTransparency", "Version: %s") % (version))
        version.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        lines.addWidget(version)
        lines.addWidget(QLabel(QApplication.translate("RasterTransparency", "Change raster transparency interactively")))
        lines.addWidget(QLabel(QApplication.translate("RasterTransparency", "<b>Developers:</b>")))
        lines.addWidget(QLabel("  Alexander Bruy"))
        lines.addWidget(QLabel(QApplication.translate("RasterTransparency", "<b>Homepage:</b>")))

        overrideLocale = bool(QSettings().value("locale/overrideFlag", False))
        if not overrideLocale:
            localeFullName = QLocale.system().name()
        else:
            localeFullName = QSettings().value("locale/userLocale", "")

        localeShortName = localeFullName[0:2]
        if localeShortName in ["ru", "uk"]:
            link = QLabel("<a href=\"http://gis-lab.info/qa/raster-transparency.html\">http://gis-lab.info/qa/raster-transparency.html</a>")
        else:
            link = QLabel("<a href=\"http://gis-lab.info/qa/raster-transparency.html\">http://gis-lab.info/qa/raster-transparency.html</a>")

        link.setOpenExternalLinks(True)
        lines.addWidget(link)

        btnClose = QPushButton(QApplication.translate("RasterTransparency", "Close"))
        lines.addWidget(btnClose)
        btnClose.clicked.connect(dlgAbout.close())

        dlgAbout.exec_()

    def __dockVisibilityChanged(self):
        if self.dockWidget.isVisible():
            self.actionDock.setChecked(True)
        else:
            self.actionDock.setChecked(False)
