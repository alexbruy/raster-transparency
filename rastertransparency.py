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

singleBandStyles = [ QgsRasterLayer.SingleBandGray, QgsRasterLayer.SingleBandPseudoColor, \
                     QgsRasterLayer.PalettedColor, QgsRasterLayer.PalettedSingleBandGray, \
                     QgsRasterLayer.PalettedSingleBandPseudoColor, \
                     QgsRasterLayer.MultiBandSingleBandGray, \
                     QgsRasterLayer.MultiBandSingleBandPseudoColor ]

class RasterTransparencyPlugin( object ):
  def __init__( self, iface ):
    self.iface = iface
    self.canvas = self.iface.mapCanvas()

    self.layer = None
    self.toolBar = None

  def initGui( self ):
    self.dockWidget = None

    # create action for plugin dockable window (show/hide)
    self.actionDock = QAction( QIcon( ":/icons/rastertransparency.png" ), "RasterTransparency", self.iface.mainWindow() )
    self.actionDock.setStatusTip( QCoreApplication.translate( "RasterTransparency", "Show/hide RasterTransparency dockwidget" ) )
    self.actionDock.setWhatsThis( QCoreApplication.translate( "RasterTransparency", "Show/hide RasterTransparency dockwidget" ) )
    self.actionDock.setCheckable( True )

    # connect actions to plugin functions
    QObject.connect( self.actionDock, SIGNAL( "triggered()" ), self.showHideDockWidget )

    # add button to the Raster toolbar
    try:
      self.iface.rasterToolBar().addAction( self.actionDock )
    except AttributeError:
      self.toolBar = self.iface.addToolBar( "Raster" )
      self.toolBar.setObjectName( "Raster" )
      self.toolBar.addAction( self.actionDock )

    # find the Raster menu
    rasterMenu = None
    menuBar = self.iface.mainWindow().menuBar()
    actions = menuBar.actions()
    rasterText = QCoreApplication.translate( "QgisApp", "&Raster" )

    for a in actions:
      if a.menu() != None and a.menu().title() == rasterText:
        rasterMenu = a.menu()
        break

    if rasterMenu == None:
      # no Raster menu, create and insert it before the Help menu
      self.rasterMenu = QMenu()
      self.rasterMenu.setTitle( rasterText )
      lastAction = actions[ len( actions ) - 1 ]
      menuBar.insertMenu( lastAction, self.menu )
    else:
      self.rasterMenu = rasterMenu
      #self.rasterMenu.addSeparator()

    calcAction = None
    i = 0
    calcText = QCoreApplication.translate( "QgisApp", "Raster calculator ..." )
    for a in self.rasterMenu.actions():
      if a.text() == calcText:
        calcAction = self.rasterMenu.actions()[ i + 1]
        break
      i += 1

    # add plugin to the Raster menu
    self.pluginMenu = QMenu( "Raster Transparency" )
    self.pluginMenu.addAction( self.actionDock )
    if calcAction is None:
      self.rasterMenu.addMenu( self.pluginMenu )
    else:
      self.rasterMenu.insertMenu( calcAction, self.pluginMenu )

    # create dockwidget
    self.dockWidget = RasterTransparencyDockWidget( self )
    self.iface.addDockWidget( Qt.LeftDockWidgetArea, self.dockWidget )
    QObject.connect( self.dockWidget, SIGNAL( "visibilityChanged( bool )" ), self.__dockVisibilityChanged )

    # track layer changing
    QObject.connect( self.iface, SIGNAL( "currentLayerChanged( QgsMapLayer* )" ), self.layerChanged )

  def unload( self ):
    # remove the plugin menu items
    self.pluginMenu.removeAction( self.actionDock )
    self.rasterMenu.removeAction( self.pluginMenu.menuAction() )

    # remove dock widget
    self.dockWidget.close()
    del self.dockWidget
    self.dockWidget = None

    # remove button
    if self.toolBar is None:
      self.iface.rasterToolBar().removeAction( self.actionDock )
    else:
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
    if self.layer.bandCount() > 1 and self.layer.drawingStyle() not in singleBandStyles:
      self.dockWidget.disableOrEnableControls( False )
      return

    # get maximum value from raster statistics
    stat = self.layer.bandStatistics( self.layer.grayBandName() )
    maxValue = stat.maximumValue
    self.dockWidget.updateSliders( maxValue )

    self.dockWidget.disableOrEnableControls( True )

  def __dockVisibilityChanged( self ):
    if self.dockWidget.isVisible():
      self.actionDock.setChecked( True )
    else:
      self.actionDock.setChecked( False )
