import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from testQt import testConnect

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = testConnect.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
