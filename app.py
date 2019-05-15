# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QDesktopWidget,QGraphicsPixmapItem,QFileDialog,QGraphicsScene,QApplication
from PyQt5.QtGui import QPixmap,QImage
from Image import *
import cv2
import numpy as np
from graphics import GraphicsView,GraphicsPixmapItem



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("银行卡号识别")
        MainWindow.setFixedSize(825,570)
        center = QDesktopWidget().screenGeometry()  
        MainWindow.move((center.width()-825)/2,(center.height()-570)/2)
        MainWindow.resize(825, 617)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(670, 190, 151, 341))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_2.addWidget(self.pushButton_4)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.graphicsView = GraphicsView(self.centralwidget)
        self.graphicsView.setEnabled(True)
        self.graphicsView.setGeometry(QtCore.QRect(10, 180, 652, 352))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_3.setGeometry(QtCore.QRect(10, 30, 502, 52))
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 100, 500, 50))
        self.label.setObjectName("label")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(550, 150, 112, 23))
        self.radioButton.setObjectName("radioButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 825, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        MainWindow.setStyleSheet("QMainWindow{background:#66B3FF}")
        self.graphicsView.setStyleSheet("QGraphicsView{background:#66B3FF}")
        self.graphicsView_3.setStyleSheet("QGraphicsView{background:#66B3FF}")

        self.pushButton_3.setText(_translate("MainWindow", "打开图片"))
        self.pushButton_3.setIcon(QtGui.QIcon("icons/open.svg"))
        self.pushButton_3.setIconSize(QtCore.QSize(20,20))
        self.pushButton_3.setStyleSheet("QPushButton{background:#16A085;border:none;color:#000000;font-size:15px;}"
        "QPushButton:hover{background-color:#008080;}")

        self.pushButton_2.setText(_translate("MainWindow", "卡号定位"))
        self.pushButton_2.setIcon(QtGui.QIcon("icons/locate.svg"))
        self.pushButton_2.setIconSize(QtCore.QSize(20,20))
        self.pushButton_2.setStyleSheet("QPushButton{background:#FFA500;border:none;color:#000000;font-size:15px;}"
        "QPushButton:hover{background-color:#D26900;}")

        self.pushButton_4.setText(_translate("MainWindow", "卡号识别"))
        self.pushButton_4.setIcon(QtGui.QIcon("icons/bank_card.svg"))
        self.pushButton_4.setIconSize(QtCore.QSize(20,20))
        self.pushButton_4.setStyleSheet("QPushButton{background:#9F35FF;border:none;color:#000000;font-size:15px}"
        "QPushButton:hover{background-color:#9932CC;}")

        self.pushButton.setText(_translate("MainWindow", "退出"))
        self.pushButton.setIcon(QtGui.QIcon("icons/close_.svg"))
        self.pushButton.setIconSize(QtCore.QSize(20,20))
        self.pushButton.setStyleSheet("QPushButton{background:#CE0000;border:none;color:#000000;font-size:15px;}"
        "QPushButton:hover{background-color:#8B0000;}")


        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.radioButton.setText(_translate("MainWindow", "手动定位"))
        self.pushButton.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.clickOpen)
        self.pushButton_2.clicked.connect(self.clickLocation)
        self.radioButton.setCheckable(True)
        self.radioButton.toggled.connect(self.checkbox)
        

        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.messageBox = QMessageBox()
        self.messageBox.setStyleSheet("QMessageBox{background-color:#CE0000;border:none;color:#000000;font-size:15px;}")

    def close(self):
        reply = self.messageBox.question(None,"Quit","确定要关闭该程序？",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            sys.exit()


    def clickOpen(self):
        imgName,imgType = QFileDialog.getOpenFileName(None,"打开图片","","*.jpg;;*.png;;*.jpeg;;All Files(*)")
        img = cv2.imread(imgName)
        self.image = Image(img)
        H,W,C = self.image.img.shape
        P = 3 * W
        qimage = QImage(self.image.img.data,W,H,P,QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qimage)
        self.graphicsView.setSceneRect(0,0,650,350)
        self.graphicsView.setItem(pixmap)
        self.graphicsView.Scene()
        self.graphicsView.setStyleSheet("QGraphicsView{background-color:#66B3FF}")

        if self.radioButton.isChecked() == True:
            self.graphicsView.image_item.setStart(True)


    def clickLocation(self):
        if self.radioButton.isChecked() == False:
            self.graphicsView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))

            Img = self.image.pos_img
            Img = cv2.resize(Img,(500,50),cv2.INTER_NEAREST)
            H,W,_ = Img.shape
            P = 3 * W
            Img = QImage(Img.data,W,H,P,QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(Img)
            Item = QGraphicsPixmapItem(pixmap)

            self.graphicsView_3Scene = QGraphicsScene()
            self.graphicsView_3Scene.addItem(Item)
            self.graphicsView_3.setSceneRect(0,0,500,50)
            self.graphicsView_3.setStyleSheet("QGraphicsView{background-color:#66B3FF}")
            self.graphicsView_3.setScene(self.graphicsView_3Scene)
            backImg = self.image.remove_back_img.copy()
            cv2.rectangle(backImg,(self.image.W_start,self.image.H_start),(self.image.W_end,self.image.H_end),(0,0,255),2)
            backImg = cv2.resize(backImg,(650,350),cv2.INTER_NEAREST)
            H,W,_ = backImg.shape
            P = 3 * W
            backImg = QImage(backImg.data,W,H,P,QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(backImg)

            self.graphicsView.setItem(pixmap)
            self.graphicsView.Scene()

        else:
            backImg = self.image.remove_back_img.copy()
            Img = backImg[int(self.graphicsView.image_item.start_point.y()):int(self.graphicsView.image_item.end_point.y()),
            int(self.graphicsView.image_item.start_point.x()):int(self.graphicsView.image_item.end_point.x())]
            Img = cv2.resize(Img,(500,50),cv2.INTER_NEAREST)
            Img = QImage(Img.data,500,50,1500,QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(Img)
            Item = QGraphicsPixmapItem(pixmap)
            self.graphicsView_3Scene = QGraphicsScene()
            self.graphicsView_3Scene.addItem(Item)
            self.graphicsView_3.setSceneRect(0,0,500,50)
            self.graphicsView_3.setStyleSheet("QGraphicsView{background-color:#66B3FF}")
            self.graphicsView_3.setScene(self.graphicsView_3Scene)

    def checkbox(self):
        if self.radioButton.isChecked() == True:
            self.graphicsView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
            backImg = self.image.remove_back_img
            backImg = cv2.resize(backImg,(650,350),cv2.INTER_NEAREST)
            H,W,_ = backImg.shape
            P = 3 * W
            backImg = QImage(backImg.data,W,H,P,QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(backImg)
            self.graphicsView.setItem(pixmap)
            self.graphicsView.Scene()
            self.graphicsView.image_item.setStart(True)
            print(self.graphicsView.image_item.isStart)
        elif self.radioButton.isChecked() == True:
            self.graphicsView.image_item.setStart(False)
            self.graphicsView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
