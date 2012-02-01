# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rastertransparencydockwidgetbase.ui'
#
# Created: Wed Feb  1 13:42:26 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RasterTransparencyDockWidget(object):
    def setupUi(self, RasterTransparencyDockWidget):
        RasterTransparencyDockWidget.setObjectName(_fromUtf8("RasterTransparencyDockWidget"))
        RasterTransparencyDockWidget.resize(302, 182)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.sliderStart = QtGui.QSlider(self.dockWidgetContents)
        self.sliderStart.setProperty(_fromUtf8("value"), 0)
        self.sliderStart.setOrientation(QtCore.Qt.Horizontal)
        self.sliderStart.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sliderStart.setObjectName(_fromUtf8("sliderStart"))
        self.horizontalLayout.addWidget(self.sliderStart)
        self.spinStart = QtGui.QSpinBox(self.dockWidgetContents)
        self.spinStart.setMaximum(100)
        self.spinStart.setObjectName(_fromUtf8("spinStart"))
        self.horizontalLayout.addWidget(self.spinStart)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.sliderEnd = QtGui.QSlider(self.dockWidgetContents)
        self.sliderEnd.setOrientation(QtCore.Qt.Horizontal)
        self.sliderEnd.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sliderEnd.setObjectName(_fromUtf8("sliderEnd"))
        self.horizontalLayout_2.addWidget(self.sliderEnd)
        self.spinEnd = QtGui.QSpinBox(self.dockWidgetContents)
        self.spinEnd.setObjectName(_fromUtf8("spinEnd"))
        self.horizontalLayout_2.addWidget(self.spinEnd)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.chkManualUpdate = QtGui.QCheckBox(self.dockWidgetContents)
        self.chkManualUpdate.setObjectName(_fromUtf8("chkManualUpdate"))
        self.horizontalLayout_3.addWidget(self.chkManualUpdate)
        self.btnRefresh = QtGui.QPushButton(self.dockWidgetContents)
        self.btnRefresh.setObjectName(_fromUtf8("btnRefresh"))
        self.horizontalLayout_3.addWidget(self.btnRefresh)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        RasterTransparencyDockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(RasterTransparencyDockWidget)
        QtCore.QMetaObject.connectSlotsByName(RasterTransparencyDockWidget)

    def retranslateUi(self, RasterTransparencyDockWidget):
        RasterTransparencyDockWidget.setWindowTitle(QtGui.QApplication.translate("RasterTransparencyDockWidget", "Raster Transparency", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RasterTransparencyDockWidget", "Values min/max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RasterTransparencyDockWidget", "Values max/min", None, QtGui.QApplication.UnicodeUTF8))
        self.chkManualUpdate.setText(QtGui.QApplication.translate("RasterTransparencyDockWidget", "Manual update", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRefresh.setText(QtGui.QApplication.translate("RasterTransparencyDockWidget", "Refresh", None, QtGui.QApplication.UnicodeUTF8))

