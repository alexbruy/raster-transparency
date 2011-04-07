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

    try:
      self.QgisVersion = unicode( QGis.QGIS_VERSION_INT )
    except:
      self.QgisVersion = unicode( QGis.qgisVersion )[ 0 ]

    # For i18n support
    userPluginPath = QFileInfo( QgsApplication.qgisUserDbFilePath() ).path() + "/python/plugins/raster_transparency"
    systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/raster_transparency"

    overrideLocale = QSettings().value( "locale/overrideFlag", QVariant( False ) ).toBool()
    if not overrideLocale:
      localeFullName = QLocale.system().name()
    else:
      localeFullName = QSettings().value( "locale/userLocale", QVariant( "" ) ).toString()

    if QFileInfo( userPluginPath ).exists():
      translationPath = userPluginPath + "/i18n/rastertransparency_" + localeFullName + ".qm"
    else:
      translationPath = systemPluginPath + "/i18n/rastertransparency_" + localeFullName + ".qm"

    self.localePath = translationPath
    if QFileInfo( self.localePath ).exists():
      self.translator = QTranslator()
      self.translator.load( self.localePath )
      QCoreApplication.installTranslator( self.translator )

  def initGui( self ):
    if int( self.QgisVersion ) < 10500:
      QMessageBox.warning( self.iface.mainWindow(), "RasterTransparency",
                           QCoreApplication.translate( "RasterTransparency", "Quantum GIS version detected: %1.%2\n" ).arg( self.QgisVersion[ 0 ] ).arg( self.QgisVersion[ 2 ] ) +
                           QCoreApplication.translate( "RasterTransparency", "This version of Raster Transparency requires at least QGIS version 1.5.0\nPlugin will not be enabled." ) )
      return None

    self.dockWidget = None

    # create action for plugin dockable window (show/hide)
    self.actionDock = QAction( QIcon( ":/icons/rastertransparency.png" ), "RasterTransparency", self.iface.mainWindow() )
    self.actionDock.setStatusTip( QCoreApplication.translate( "RasterTransparency", "Show/hide RasterTransparency dockwidget" ) )
    self.actionDock.setWhatsThis( QCoreApplication.translate( "RasterTransparency", "Show/hide RasterTransparency dockwidget" ) )
    self.actionDock.setCheckable( True )

    # create action for display plugin about dialog
    self.actionAbout = QAction( QIcon( ":/icons/rastertransparency.png" ), "About", self.iface.mainWindow() )
    self.actionAbout.setStatusTip( QCoreApplication.translate( "RasterTransparency", "About RasterTransparency" ) )
    self.actionAbout.setWhatsThis( QCoreApplication.translate( "RasterTransparency", "About RasterTransparency" ) )

    # connect actions to plugin functions
    QObject.connect( self.actionDock, SIGNAL( "triggered()" ), self.showHideDockWidget )
    QObject.connect( self.actionAbout, SIGNAL( "triggered()" ), self.about )

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
    self.pluginMenu.addAction( self.actionAbout )
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
    QObject.disconnect( self.iface, SIGNAL( "currentLayerChanged( QgsMapLayer* )" ), self.layerChanged )

    # remove the plugin menu items
    self.pluginMenu.removeAction( self.actionDock )
    self.pluginMenu.removeAction( self.actionAbout )
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
    if self.layer.type() != QgsMapLayer.RasterLayer:
      self.dockWidget.disableOrEnableControls( False )
      return

    # also disable it for multiband layers that not in single band style
    if self.layer.bandCount() > 1 and self.layer.drawingStyle() not in singleBandStyles:
      self.dockWidget.disableOrEnableControls( False )
      return

    # get maximum value from raster statistics
    stat = self.layer.bandStatistics( self.layer.grayBandName() )
    maxValue = stat.maximumValue
    self.dockWidget.updateSliders( maxValue )

    self.dockWidget.disableOrEnableControls( True )

  def about( self ):
    dlgAbout = QDialog()
    dlgAbout.setWindowTitle( QApplication.translate( "RasterTransparency", "About Raster Transparency", "Window title" ) )
    lines = QVBoxLayout( dlgAbout )
    title = QLabel( QApplication.translate( "RasterTransparency", "<b>Raster Transparency</b>" ) )
    title.setAlignment( Qt.AlignHCenter | Qt.AlignVCenter )
    lines.addWidget( title )
    version = QLabel( QApplication.translate( "RasterTransparency", "Version: %1" ).arg( mVersion ) )
    version.setAlignment( Qt.AlignHCenter | Qt.AlignVCenter )
    lines.addWidget( version )
    lines.addWidget( QLabel( QApplication.translate( "RasterTransparency", "Change raster transparency interactively" ) ) )
    lines.addWidget( QLabel( QApplication.translate( "RasterTransparency", "<b>Developers:</b>" ) ) )
    lines.addWidget( QLabel( "  Alexander Bruy" ) )
    lines.addWidget( QLabel( "  Maxim Dubinin" ) )
    lines.addWidget( QLabel( QApplication.translate( "RasterTransparency", "<b>Homepage:</b>") ) )

    overrideLocale = QSettings().value( "locale/overrideFlag", QVariant( False ) ).toBool()
    if not overrideLocale:
      localeFullName = QLocale.system().name()
    else:
      localeFullName = QSettings().value( "locale/userLocale", QVariant( "" ) ).toString()

    localeShortName = localeFullName[ 0:2 ]
    if localeShortName in [ "ru", "uk" ]:
      link = QLabel( "<a href=\"http://gis-lab.info/qa/raster-transparency.html\">http://gis-lab.info/qa/raster-transparency.html</a>" )
    else:
      link = QLabel( "<a href=\"http://gis-lab.info/qa/raster-transparency.html\">http://gis-lab.info/qa/raster-transparency.html</a>" )

    link.setOpenExternalLinks( True )
    lines.addWidget( link )

    btnClose = QPushButton( QApplication.translate( "RasterTransparency", "Close" ) )
    lines.addWidget( btnClose )
    QObject.connect( btnClose, SIGNAL( "clicked()" ), dlgAbout, SLOT( "close()" ) )

    dlgAbout.exec_()

  def __dockVisibilityChanged( self ):
    if self.dockWidget.isVisible():
      self.actionDock.setChecked( True )
    else:
      self.actionDock.setChecked( False )
