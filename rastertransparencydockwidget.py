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

from rastertransparencydockwidgetbase import Ui_RasterTransparencyDockWidget

class RasterTransparencyDockWidget( QDockWidget, Ui_RasterTransparencyDockWidget, object ):
  def __init__( self, plugin ):
    QDockWidget.__init__( self, None )
    self.setupUi( self )
    self.setAllowedAreas( Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea )

    self.plugin = plugin

    self.manageGui()

    # connect signals and slots
    QObject.connect( self.sliderStart, SIGNAL( "valueChanged( int )" ), self.__updateSpinStart )
    QObject.connect( self.spinStart, SIGNAL( "valueChanged( int )" ), self.__updateSliderStart )
    QObject.connect( self.sliderEnd, SIGNAL( "valueChanged( int )" ), self.__updateSpinEnd )
    QObject.connect( self.spinEnd, SIGNAL( "valueChanged( int )" ), self.__updateSliderEnd )
    QObject.connect( self.sliderStart, SIGNAL( "sliderReleased ()" ), self.updateRasterTransparency )
    QObject.connect( self.sliderEnd, SIGNAL( "sliderReleased ()" ), self.updateRasterTransparency )

  def manageGui( self ):
    pass

  def updateRasterTransparency( self ):
    transparencyList = []
    for v in range( 0, self.slider.value() + 1 ):
      tr = QgsRasterTransparency.TransparentSingleValuePixel()
      tr.pixelValue = v
      tr.percentTransparent = 100
      transparencyList.append( tr )
    # update layer transparency
    layer = self.plugin.iface.mapCanvas().currentLayer()
    layer.rasterTransparency().setTransparentSingleValuePixelList( transparencyList )
    self.plugin.iface.mapCanvas().refresh()

  def __updateSpinStart( self, value ):
    self.spinStart.setValue( value )

  def __updateSliderStart( self, value ):
    self.sliderStart.setValue( value )

  def __updateSpinEnd( self, value ):
    self.spinEnd.setValue( value )

  def __updateSliderEnd( self, value ):
    self.sliderEnd.setValue( value )

  def disableOrEnableControls( self, disable ):
    #QMessageBox.warning( None, "DEBUG", "Disable or enable" )
    self.label.setEnabled( disable )
    self.sliderStart.setEnabled( disable )
    self.spinStart.setEnabled( disable )
    self.label_2.setEnabled( disable )
    self.sliderEnd.setEnabled( disable )
    self.spinEnd.setEnabled( disable )

  def setupSliders( self, minValue, maxValue ):
    pass

