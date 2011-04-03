# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rastertransparencydockwidgetbase.ui'
#
# Created: Sun Apr  3 16:13:53 2011
#      by: PyQt4 UI code generator 4.5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RasterTransparencyDockWidget(object):
    def setupUi(self, RasterTransparencyDockWidget):
        RasterTransparencyDockWidget.setObjectName("RasterTransparencyDockWidget")
        RasterTransparencyDockWidget.resize(302, 140)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sliderStart = QtGui.QSlider(self.dockWidgetContents)
        self.sliderStart.setProperty("value", QtCore.QVariant(0))
        self.sliderStart.setOrientation(QtCore.Qt.Horizontal)
        self.sliderStart.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sliderStart.setObjectName("sliderStart")
        self.horizontalLayout.addWidget(self.sliderStart)
        self.spinStart = QtGui.QSpinBox(self.dockWidgetContents)
        self.spinStart.setMaximum(100)
        self.spinStart.setObjectName("spinStart")
        self.horizontalLayout.addWidget(self.spinStart)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sliderEnd = QtGui.QSlider(self.dockWidgetContents)
        self.sliderEnd.setOrientation(QtCore.Qt.Horizontal)
        self.sliderEnd.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sliderEnd.setObjectName("sliderEnd")
        self.horizontalLayout_2.addWidget(self.sliderEnd)
        self.spinEnd = QtGui.QSpinBox(self.dockWidgetContents)
        self.spinEnd.setObjectName("spinEnd")
        self.horizontalLayout_2.addWidget(self.spinEnd)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        RasterTransparencyDockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(RasterTransparencyDockWidget)
        QtCore.QMetaObject.connectSlotsByName(RasterTransparencyDockWidget)

    def retranslateUi(self, RasterTransparencyDockWidget):
        RasterTransparencyDockWidget.setWindowTitle(QtGui.QApplication.translate("RasterTransparencyDockWidget", "Raster Transparency", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RasterTransparencyDockWidget", "Values min/max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RasterTransparencyDockWidget", "Values max/min", None, QtGui.QApplication.UnicodeUTF8))

