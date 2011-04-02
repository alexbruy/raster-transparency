# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rastertransparencydockwidgetbase.ui'
#
# Created: Sat Apr  2 11:42:03 2011
#      by: PyQt4 UI code generator 4.5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RasterTransparencyDockWidget(object):
    def setupUi(self, RasterTransparencyDockWidget):
        RasterTransparencyDockWidget.setObjectName("RasterTransparencyDockWidget")
        RasterTransparencyDockWidget.resize(294, 65)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.slider = QtGui.QSlider(self.dockWidgetContents)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setProperty("value", QtCore.QVariant(0))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.slider.setTickInterval(20)
        self.slider.setObjectName("slider")
        self.horizontalLayout.addWidget(self.slider)
        self.spinBox = QtGui.QSpinBox(self.dockWidgetContents)
        self.spinBox.setMaximum(100)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        RasterTransparencyDockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(RasterTransparencyDockWidget)
        QtCore.QMetaObject.connectSlotsByName(RasterTransparencyDockWidget)

    def retranslateUi(self, RasterTransparencyDockWidget):
        RasterTransparencyDockWidget.setWindowTitle(QtGui.QApplication.translate("RasterTransparencyDockWidget", "Raster Transparency", None, QtGui.QApplication.UnicodeUTF8))

