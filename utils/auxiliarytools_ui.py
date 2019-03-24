#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .get_resource_path import resource_path
from PyQt5 import QtCore, QtGui, QtWidgets


class AuxiliaryToolsWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(388, 634)
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path("logo.ico")))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout_top = QtWidgets.QHBoxLayout()
        self.horizontalLayout_top.setObjectName("horizontalLayout_top")

        self.original_image_demo = QtWidgets.QLabel(self.centralwidget)
        self.original_image_demo.setText("")
        self.original_image_demo.setPixmap(
            QtGui.QPixmap(resource_path("original.jpg"))
        )
        self.original_image_demo.setAlignment(QtCore.Qt.AlignCenter)
        self.original_image_demo.setObjectName("original_image_demo")
        self.horizontalLayout_top.addWidget(self.original_image_demo)

        self.landmark_image_demo = QtWidgets.QLabel(self.centralwidget)
        self.landmark_image_demo.setText("")
        self.landmark_image_demo.setPixmap(
            QtGui.QPixmap(resource_path("landmark.jpg"))
        )
        self.landmark_image_demo.setAlignment(QtCore.Qt.AlignCenter)
        self.landmark_image_demo.setObjectName("landmark_image_demo")
        self.horizontalLayout_top.addWidget(self.landmark_image_demo)

        self.verticalLayout.addLayout(self.horizontalLayout_top)

        self.list_widgets = QtWidgets.QHBoxLayout()
        self.list_widgets.setObjectName("list_widgets")

        self.images_list_widget = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.images_list_widget.sizePolicy().hasHeightForWidth()
        )
        self.images_list_widget.setSizePolicy(sizePolicy)
        self.images_list_widget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.images_list_widget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustIgnored
        )
        self.images_list_widget.setObjectName("images_list_widget")
        self.list_widgets.addWidget(self.images_list_widget)

        self.verticalLayout.addLayout(self.list_widgets)

        self.horizontalLayout_bottom = QtWidgets.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName("horizontalLayout_bottom")

        self.pushButton_back = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_back.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_back.setSizePolicy(sizePolicy)
        self.pushButton_back.setObjectName("pushButton_back")
        self.horizontalLayout_bottom.addWidget(self.pushButton_back)

        self.pushButton_next = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_next.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_next.setSizePolicy(sizePolicy)
        self.pushButton_next.setObjectName("pushButton_next")
        self.horizontalLayout_bottom.addWidget(self.pushButton_next)

        self.magnifier_window = QtWidgets.QLabel(self.centralwidget)
        self.magnifier_window.setText("")
        self.magnifier_window.setObjectName("magnifier_window")
        self.horizontalLayout_bottom.addWidget(self.magnifier_window)
        self.verticalLayout.addLayout(self.horizontalLayout_bottom)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Auxiliary Tools"))
        self.pushButton_back.setText(_translate("MainWindow", "<Back"))
        self.pushButton_next.setText(_translate("MainWindow", "Next>"))
