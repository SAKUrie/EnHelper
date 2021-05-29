import sys
import Const
from pymssql import connect
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QWidget,QGraphicsObject

# 常量定义
server = "127.0.0.1"
password = "qwer"
user = "usr"


class loginUI(QGraphicsObject):
    switch_window = pyqtSignal()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(463, 363)
        MainWindow.setMinimumSize(QtCore.QSize(463, 363))
        MainWindow.setMaximumSize(QtCore.QSize(463, 363))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 110, 401, 221))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 50, 141, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(190, 50, 141, 81))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_4.addWidget(self.lineEdit_3)

        self.pwd_line = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.pwd_line.setObjectName("lineEdit_4")
        self.pwd_line.setEchoMode(QLineEdit.Password)
        self.verticalLayout_4.addWidget(self.pwd_line)

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(150, 160, 93, 29))
        self.pushButton.setMinimumSize(QtCore.QSize(93, 29))
        self.pushButton.setMaximumSize(QtCore.QSize(93, 29))
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.Login)

        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(30, 20, 401, 80))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame_2)
        self.textBrowser.setGeometry(QtCore.QRect(-10, -9, 421, 101))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EnHelper"))
        self.label_4.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-size:8pt;\">用户名：</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "密码："))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.textBrowser.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'SimSun\'; font-size:7.2pt; font-weight:400; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'verdana\'; font-size:14pt;\">EnHelper</span></p>\n"
                                            "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'微软雅黑\'; font-size:14pt;\">单词学习小助手</span></p></body></html>"))

    def Login(self):
        UserName = self.lineEdit_3.text()
        Passwd = self.pwd_line.text()
        # if UserName == "123" and Passwd == "123":
        #     print("ok")
        #     self.switch_window.emit()
        #     print("Signal ok")
        conn = connect(server, user, password, "EnHelper")
        cur = conn.cursor()
        cur.execute("Select * From Users")
        row = cur.fetchone()
        login = 0
        while row:
            # 获取名称字段的值
            if login == 1:
                break
            name = row[0]
            passwd = row[2]
            if name == UserName and Passwd == passwd:
                Const.userid_now = row[1]
                print(Const.userid_now)
                login = 1
                Const.username_now = row[0]
                self.switch_window.emit()
                print("login signal ok")

            row = cur.fetchone()
        if login == 0:
            print("Fail")
            QMessageBox.critical(QWidget(), "登陆失败", "用户名或密码错误")
            # 保留用户名删除密码，光标停留在密码处
            self.pwd_line.clear()
            self.pwd_line.setFocus()
        cur.close()
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = loginUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
