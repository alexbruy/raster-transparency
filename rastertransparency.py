# -*- coding: utf-8 -*-

#******************************************************************************
#
# RasterTransparency
# ---------------------------------------------------------
# Interactively setup raster transparency
#
# Copyright (C) 2010 Alexander Bruy (alexander.bruy@gmail.com)
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

from rastertransparencydockwidget import *

from __init__ import mVersion

import resources

class RasterTransparencyPlugin( object ):
  def __init__( self, iface ):
    self.iface = iface
    self.canvas = self.iface.mapCanvas()

    self.outputLayer = None

  def initGui( self ):
    self.dockWidget = None

    # create action for plugin dockable window (show/hide)
    self.actionDock = QAction( QIcon( ":/icons/rastertransparency.png" ), "RasterTransparency", self.iface.mainWindow() )
    self.actionDock.setStatusTip( QCoreApplication.translate( "RasterTransparency", "Show/hide RasterTransparency dockwidget" ) )
    self.actionDock.setWhatsThis( QCoreApplication.translate( "RasterTransparency", "Show/hide RasterTransparency dockwidget" ) )
    self.actionDock.setCheckable( True )

    # connect actions to plugin functions
    QObject.connect( self.actionDock, SIGNAL( "triggered()" ), self.showHideDockWidget )

    # create a toolbar
    self.toolBar = self.iface.addToolBar( "RasterTransparency" )
    self.toolBar.setObjectName( "RasterTransparency" )
    self.toolBar.addAction( self.actionDock )

    # populate plugins menu
    self.iface.addPluginToMenu( "Raster Transparency", self.actionDock)

    # create dockwidget
    self.dockWidget = RasterTransparencyDockWidget( self )
    self.iface.addDockWidget( Qt.LeftDockWidgetArea, self.dockWidget )
    QObject.connect( self.dockWidget, SIGNAL( "visibilityChanged( bool )" ), self.__dockVisibilityChanged )

    # track layer changing
    QObject.connect( self.iface, SIGNAL( "currentLayerChanged( QgsMapLayer* )" ), self.layerChanged )

  def unload( self ):
    # remove the plugin menu items
    self.iface.removePluginMenu( "Raster Transparency", self.actionDock)

    # remove dock widget
    self.dockWidget.close()
    del self.dockWidget
    self.dockWidget = None

    # remove toolbar
    del self.toolBar

  def showHideDockWidget( self ):
    if self.dockWidget.isVisible():
      self.dockWidget.hide()
    else:
      self.dockWidget.show()

  def layerChanged( self ):
    self.layer = self.iface.activeLayer()

    if self.layer is None:
      return

    # disable plugin for vector layers
    if self.layer.type() == QgsMapLayer.VectorLayer and self.layer.type() != QgsMapLayer.RasterLayer:
      self.dockWidget.disableOrEnableControls( False )
      return

    # also disable it for multiband layers
    if self.layer.bandCount() > 1:
      self.dockWidget.disableOrEnableControls( False )
      return

    # calculate statistics
    stat = self.layer.bandStatistics( 1 )
    maxValue = stat.maximumValue
    self.dockWidget.updateSliders( maxValue )

    self.dockWidget.disableOrEnableControls( True )

  def __dockVisibilityChanged( self ):
    if self.dockWidget.isVisible():
      self.actionDock.setChecked( True )
    else:
      self.actionDock.setChecked( False )
