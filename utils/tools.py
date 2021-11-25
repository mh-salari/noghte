#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .get_resource_path import resource_path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtWidgets import (
    QMainWindow,
    QListWidget,
    QLabel,
    QDesktopWidget,
    QSizePolicy,
)
from PyQt5.QtGui import QPainter, QPen, QPixmap, QImage

import cv2
import numpy as np

from utils.auxiliarytools_ui import AuxiliaryToolsWindow


tmp_landmark_name_list = np.loadtxt(
    resource_path("landmark_name.txt"), dtype=str
)


class LandmarksListWidget(QListWidget):
    current_item_num = 0
    modify = False

    def __init__(self, name_list=tmp_landmark_name_list):
        super().__init__()
        self.insertItems(0, name_list)
        self.setMinimumWidth(self.sizeHintForColumn(0))
        first_list_item = self.item(self.current_item_num)
        self.setCurrentItem(first_list_item)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.setObjectName("landmarks_list")

    noItemInList = pyqtSignal()

    def select_next_item(self):
        if self.modify:
            self.modify = False
        else:
            self.current_item_num += 1
        next_item = self.item(self.current_item_num)
        if next_item is None:
            self.noItemInList.emit()
        self.setCurrentItem(next_item)

    itemClicked = pyqtSignal(int)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        num = self.currentIndex().row()
        if num < self.current_item_num:
            super().mousePressEvent(event)
            self.itemClicked.emit(num)
            self.modify = True
        else:
            current_item_num = self.item(self.current_item_num)
            self.setCurrentItem(current_item_num)

    def clear_current_item_num(self):
        self.current_item_num = 0
        first_list_item = self.item(self.current_item_num)
        self.setCurrentItem(first_list_item)

    def mouseMoveEvent(self, *args, **kwargs):
        pass

    def on_item_selected(self):
        pass


class ToolWidget(QMainWindow, AuxiliaryToolsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(20, 50)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(Qt.Widget)
        self.landmarks_list = LandmarksListWidget()
        self.list_widgets.addWidget(self.landmarks_list)

    def show_bigger_img(self, part):
        self.magnifier_window.setPixmap(part)


def cv_resize_img(img_path):
    global ghight
    global gwitgh
    cv_img = cv2.imread(img_path)
    height, width, channel = cv_img.shape
    ghight, gwitgh = (height, width)
    cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB, cv_img)
    cp = QDesktopWidget().availableGeometry()
    scale = height / cp.bottom() * 1.1
    cv_img = cv2.resize(cv_img, (int(width / scale), int(height / scale)))
    return cv_img, scale


def cv2qt(cv_img):
    height, width, channel = cv_img.shape
    byte_per_line = channel * width
    q_img = QImage(
        cv_img.data, width, height, byte_per_line, QImage.Format_RGB888
    )
    q_pixmap = QPixmap.fromImage(q_img)
    return q_pixmap


def qt2cv(q_pixmap):

    q_img = q_pixmap.toImage()
    q_img = q_img.convertToFormat(4)

    width = q_img.width()
    height = q_img.height()

    ptr = q_img.bits()
    ptr.setsize(q_img.byteCount())
    cv_img = np.array(ptr).reshape(height, width, 4)
    cv_img = cv_img[:, :, 0:3]
    return cv_img


class ImgLabel(QLabel):
    points_list = []
    cv_img = None
    cv_img_red_dot = None
    scale = 0
    i = 0
    modify = False
    modify_index = -1
    noRedDot = False
    save_path = ""

    def __init__(self, img_path, save_path):
        super().__init__()
        self.setupUI()
        if img_path is None or save_path is None:
            return
        self.save_path = save_path
        cv_img, self.scale = cv_resize_img(img_path)
        self.cv_img = np.array(cv_img)
        self.cv_img_red_dot = np.array(cv_img)
        q_pixmap = cv2qt(cv_img)
        self.setPixmap(q_pixmap)

    def change_img(self, img_path, save_path):
        self.points_list = []
        self.cv_img = None
        self.cv_img_red_dot = None
        self.scale = 0
        self.i = 0
        self.modify = False
        self.modify_index = -1
        self.noRedDot = False
        self.save_path = save_path
        cv_img, self.scale = cv_resize_img(img_path)
        self.cv_img = np.array(cv_img)
        self.cv_img_red_dot = np.array(cv_img)
        q_pixmap = cv2qt(cv_img)
        self.setPixmap(q_pixmap)

    def setupUI(self):
        self.setCursor(QtCore.Qt.CrossCursor)
        self.setEnabled(True)
        self.setAlignment(Qt.AlignCenter)
        # size_policy = QSizePolicy()
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setObjectName("img_label")
        self.setMouseTracking(True)

    mouseClicked = pyqtSignal(name="mouseClicked")

    def mousePressEvent(self, event):
        if self.noRedDot is False:
            x = event.x()
            y = event.y()
            point = QPoint(x, y)

            if self.modify:
                self.points_list[self.modify_index] = point
                self.modify = False
                self.modify_index = -1
            else:
                self.points_list.append(point)

            self.cv_img_red_dot = np.array(self.cv_img)
            for idx, point in enumerate(self.points_list):
                cv2.putText(
                    self.cv_img_red_dot,
                    f"{idx+1}",
                    (point.x() + 5, point.y() + 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    1,
                )
                cv2.rectangle(
                    self.cv_img_red_dot,
                    (point.x() - 2, point.y() - 2),
                    (point.x() + 2, point.y() + 2),
                    (255, 0, 0),
                    -1,
                )

            q_pixmap = cv2qt(self.cv_img_red_dot)
            self.setPixmap(q_pixmap)

            self.update()
            self.mouseMoveEvent(event)
            self.save_points_txt()
            self.mouseClicked.emit()

    mouseMoved = pyqtSignal(QPixmap, name="mouseMoved")

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        w = 50
        cv_now = self.cv_img_red_dot
        cv_img_part = np.array(cv_now[y - w : y + w, x - w : x + w])
        if cv_img_part.shape != (w * 2, w * 2, 3):
            return
        cv_img_part = cv2.resize(cv_img_part, (w * 4, w * 4))
        cv2.line(cv_img_part, (0, 2 * w), (4 * w, 2 * w), (255, 255, 255), 1)
        cv2.line(cv_img_part, (2 * w, 0), (2 * w, 4 * w), (255, 255, 255), 1)
        cv_enlarged_img_part = cv2qt(cv_img_part)
        self.mouseMoved.emit(cv_enlarged_img_part)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
        for p in self.points_list:
            painter.drawPoint(p)

    def on_list_clicked(self, i):
        self.noRedDot = False
        if i < len(self.points_list):
            self.modify = True
            self.modify_index = i

    def no_item(self):
        self.noRedDot = True

    def save_points_txt(self,):
        global ghight
        global gwitgh
        with open(self.save_path, "w") as f:
            f.write("version: 0.1\n")
            f.write(f"width: {gwitgh}\n")
            f.write(f"height: {ghight}\n")

            f.write(f"n_points: {len(self.points_list)}\n")
            f.write("{\n")
            for i in self.points_list:
                x = int(i.x() * self.scale)
                y = int(i.y() * self.scale)
                f.write(f"{x},{y}\n")
            f.write("}")
