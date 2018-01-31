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

from qgis.PyQt.QtCore import QCoreApplication, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsApplication

from raster_transparency.gui.rastertransparencywidget import TransparencyPanelFactory
from raster_transparency.gui.aboutdialog import AboutDialog

pluginPath = os.path.dirname(__file__)


class RasterTransparencyPlugin:

    def __init__(self, iface):
        self.iface = iface

        locale = QgsApplication.locale()
        qmPath = "{}/i18n/rastertransparency_{}.qm".format(pluginPath, locale)

        if os.path.exists(qmPath):
            self.translator = QTranslator()
            self.translator.load(qmPath)
            QCoreApplication.installTranslator(self.translator)

        self.factory = TransparencyPanelFactory()

    def initGui(self):
        self.actionAbout = QAction(self.tr("About RasterTransparency…"), self.iface.mainWindow())
        self.actionAbout.setIcon(QgsApplication.getThemeIcon("/mActionHelpContents.svg"))
        self.actionAbout.setObjectName("aboutRasterTransparency")
        self.actionAbout.triggered.connect(self.about)

        self.iface.addPluginToRasterMenu(self.tr("Raster transparency"), self.actionAbout)

        self.iface.registerMapLayerConfigWidgetFactory(self.factory)

    def unload(self):
        self.iface.removePluginRasterMenu(self.tr("Raster transparency"), self.actionAbout)

        self.iface.unregisterMapLayerConfigWidgetFactory(self.factory)

    def about(self):
        d = AboutDialog()
        d.exec_()

    def tr(self, text):
        return QCoreApplication.translate("RasterTransparency", text)
