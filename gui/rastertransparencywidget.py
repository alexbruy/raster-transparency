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

from qgis.core import QgsSettings, QgsRasterTransparency
from qgis.utils import iface

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(os.path.join(pluginPath, "ui", "rastertransparencywidgetbase.ui"))


class RasterTransparencyWidget(BASE, WIDGET):
    def __init__(self, parent=None):
        super(RasterTransparencyWidget, self).__init__(parent)
        self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0)

    def setLayer(self, layer):
        pass
