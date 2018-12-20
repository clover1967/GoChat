# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
from PyQt5.QtSql import *




class ChatWindow_W(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(700, 500)
        '''
        用户名
        '''
        self.setWindowTitle("GoChat")
        self.setUpUI()

    def setUpUI(self):
        self.layout = QVBoxLayout(self)

        # Table和Model
        self.Records = QTextEdit()
        self.NewMessge =  QTextEdit()
        self.SendButton = QPushButton("发送")

        self.layout.addWidget(self.Records)
        self.layout.addWidget(self.NewMessage)
        self.layout.addWidget(self.SentButton)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    viewer = GoChat()
    viewer.show()
    sys.exit(app.exec_())
