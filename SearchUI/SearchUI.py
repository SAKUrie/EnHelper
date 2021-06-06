# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SearchUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys

import pymssql
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import Const


class SearchUI(QMainWindow):
    back_signal = pyqtSignal()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 580)
        MainWindow.setMouseTracking(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 181, 521))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.UserName = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        self.UserName.setFont(font)
        self.UserName.setAlignment(QtCore.Qt.AlignCenter)
        self.UserName.setObjectName("UserName")
        self.verticalLayout.addWidget(self.UserName)

        self.word_rbtn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.word_rbtn.setObjectName("word_rbtn")
        self.verticalLayout.addWidget(self.word_rbtn, 0, QtCore.Qt.AlignHCenter)

        self.sentence_rbtn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.sentence_rbtn.setObjectName("sentence_rbtn")
        self.verticalLayout.addWidget(self.sentence_rbtn, 0, QtCore.Qt.AlignHCenter)

        self.back_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.back_btn.clicked.connect(self.back)

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.back_btn.setFont(font)
        self.back_btn.setObjectName("back_btn")
        self.verticalLayout.addWidget(self.back_btn)
        self.produced = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.produced.setMinimumSize(QtCore.QSize(179, 0))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.produced.setFont(font)
        self.produced.setAlignment(QtCore.Qt.AlignCenter)
        self.produced.setObjectName("produced")
        self.verticalLayout.addWidget(self.produced, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(210, 30, 561, 521))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.inputEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.inputEdit.setObjectName("inputEdit")
        self.verticalLayout_2.addWidget(self.inputEdit)
        self.search_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.search_btn.setObjectName("search_btn")
        self.search_btn.clicked.connect(lambda: self.search(MainWindow))

        self.verticalLayout_2.addWidget(self.search_btn)
        self.outputEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.outputEdit.setReadOnly(True)
        self.outputEdit.setObjectName("outputEdit")
        self.verticalLayout_2.addWidget(self.outputEdit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EnHelper[查询]"))
        self.UserName.setText(_translate("MainWindow", "UserName:{}".format(Const.username_now)))
        self.word_rbtn.setText(_translate("MainWindow", "单词查询"))
        self.sentence_rbtn.setText(_translate("MainWindow", "例句查询"))
        self.back_btn.setText(_translate("MainWindow", "返回"))
        self.produced.setText(_translate("MainWindow", "Produced by SakuRie"))
        self.label.setText(_translate("MainWindow", "请输入单词或例句"))
        self.search_btn.setText(_translate("MainWindow", "查询"))

    def message(self, Q, s, title="Info"):
        msg = QMessageBox(Q)
        msg.setWindowTitle(title)
        msg.setText(s)
        print("output:" + s)
        msg.show()
        msg.buttonClicked.connect(msg.exec_)

    def search(self,Q):
        text = self.inputEdit.text()
        output = ""

        conn = pymssql.connect(Const.server, Const.user, Const.password, "EnHelper")
        cur = conn.cursor()

        print(self.word_rbtn.isChecked())
        print(self.sentence_rbtn.isChecked())

        if self.word_rbtn.isChecked():

            print("Word Search")
            sql = "select * from FullWord where Word = '{}'".format(text)
            cur.execute(sql)
            row = cur.fetchone()
            if row is None:
                self.message(Q,"查询单词不存在","!!!!!!!!!")
            else:
                output = "单词:{}\n词性:{}\n释义:{}\n例句:{}\n例句释义:{}\n".format(
                    row[1],row[2],row[3],row[5],row[6]
                )
                self.outputEdit.setText(output)
            cur.close()
            conn.close()


        if self.sentence_rbtn.isChecked():
            print("Sentence Search")
            sql = "select * from FullWord where Sentence = '{}'".format(text)
            cur.execute(sql)
            row = cur.fetchone()
            if row is None:
                self.message(Q,"查询例句不存在","!!!!!!!!!")
            else:
                output = "单词:{}\n词性:{}\n释义:{}\n例句:{}\n例句释义:{}\n".format(
                    row[1],row[2],row[3],row[5],row[6]
                )
                self.outputEdit.setText(output)
            cur.close()
            conn.close()

    def back(self):
        self.back_signal.emit()
        print("back_signal")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = SearchUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())