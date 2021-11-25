#!/usr/bin/env python3
# coding:utf-8
import os
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QApplication,
    QMainWindow,
    QFileDialog,
)
from utils.mainwindow_ui import MainWindow

from utils.tools import ToolWidget, ImgLabel

IMG_FORMAT = ["bmp", "jpg", "png", "tif", "peg"]


class Main(QMainWindow, MainWindow):
    tool_widget = None
    file_name = ""
    label_dir = ""
    img_dir = ""
    file_name_list = []
    current_img_num = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.center()
        self.setWindowTitle("Noghte")
        self.img_label = ImgLabel(None, None)

        self.horizontalLayout_2.addWidget(self.img_label)
        # self.open_img()
        self.actionOpen.triggered.connect(self.open_img)
        self.actionOpen_Dir.triggered.connect(self.open_dir)
        self.showMaximized()
        self.show()

    def set_tool_widget(self, tool_widget):
        self.tool_widget = tool_widget
        self.img_label.mouseMoved.connect(self.tool_widget.show_bigger_img)
        self.img_label.mouseClicked.connect(
            self.tool_widget.landmarks_list.select_next_item
        )

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        # self.setGeometry(QDesktopWidget().availableGeometry())

    def open_img(self):
        filename_choose, filetype = QFileDialog.getOpenFileName(
            self, "Select image", os.getcwd(), "jpg (*.jpg)"
        )
        if filename_choose == "":
            return
        img_path = filename_choose

        self.label_dir = os.path.dirname(img_path) + "/" + "landmarks/"
        if not os.path.isdir(self.label_dir):
            os.mkdir(self.label_dir)
        save_path = self.label_dir + os.path.split(img_path)[-1][:-3] + "pts"

        tool.images_list_widget.insertItems(0, [os.path.split(img_path)[-1]])
        self.show_img_in_label(img_path, save_path)

    def show_img_in_label(self, img_path, save_path):
        self.img_label.change_img(img_path, save_path)
        self.tool_widget.show()

    def open_dir(self):
        dir_choose = QFileDialog.getExistingDirectory(
            self, "Select folder", os.getcwd()
        )
        if dir_choose == "":
            return
        dir_path = dir_choose
        self.img_dir = dir_path
        self.label_dir = dir_path + "/landmarks"

        tmp_list = os.listdir(self.img_dir)
        for tmp in tmp_list:
            if tmp[-3:] in IMG_FORMAT:
                self.file_name_list.append(tmp)
        if self.file_name_list is []:
            return
        self.current_img_num = 0

        tool.images_list_widget.insertItems(0, self.file_name_list)

        self.labeling_next_img()

    def labeling_next_img(self):
        if not os.path.isdir(self.label_dir):
            os.mkdir(self.label_dir)

        tool.images_list_widget.setCurrentItem(
            tool.images_list_widget.item(self.current_img_num)
        )
        self.tool_widget.landmarks_list.clear_current_item_num()
        img_path = (
            self.img_dir + "/" + self.file_name_list[self.current_img_num]
        )
        label_path = (
            self.label_dir
            + "/"
            + self.file_name_list[self.current_img_num][:-3]
            + "pts"
        )

        print(img_path, label_path)
        self.show_img_in_label(img_path, label_path)

    def next_img(self):
        if self.current_img_num >= len(self.file_name_list) - 1:
            self.current_img_num = len(self.file_name_list) - 1
            return
        else:
            self.current_img_num += 1
            self.labeling_next_img()

    def previous_img(self):
        if self.current_img_num <= 0:
            self.current_img_num = 0
            return
        else:
            self.current_img_num -= 1
            self.labeling_next_img()

    def closeEvent(self, e):
        super().closeEvent(e)
        QCoreApplication.instance().quit()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = Main()

    tool = ToolWidget()
    ex.set_tool_widget(tool)
    ex.actionAuxiliaryTools.triggered.connect(tool.show)
    tool.landmarks_list.itemClicked.connect(ex.img_label.on_list_clicked)
    tool.landmarks_list.noItemInList.connect(ex.img_label.no_item)
    tool.pushButton_next.clicked.connect(ex.next_img)
    tool.pushButton_back.clicked.connect(ex.previous_img)

    sys.exit(app.exec_())
