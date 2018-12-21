# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
from PyQt5.QtSql import *




class ChatWindow_W(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(700, 500)

        self.setWindowTitle("GoChat")
        self.setUpUI()

    def setUpUI(self):
        self.layout = QVBoxLayout(self)

        # Table和Model
        self.RecordsLabel = QLabel("历史消息")
        self.RecordsLabel.setFixedHeight(32)
        self.RecordsLabel.setFixedWidth(80)
        self.NewLabel = QLabel("新消息")
        self.NewLabel.setFixedHeight(32)
        self.NewLabel.setFixedWidth(60)
        font = QFont()
        font.setPixelSize(18)
        self.RecordsLabel.setFont(font)
        self.NewLabel.setFont(font)

        self.Records = QTextBrowser()
        self.NewMessage =  QTextEdit()

        self.SendButton = QPushButton("发送")
        self.SendButton.clicked.connect(self.send_msg)

        #布局
        self.layout.addWidget(self.RecordsLabel)
        self.layout.addWidget(self.Records)
        self.layout.addWidget(self.NewLabel)
        self.layout.addWidget(self.NewMessage)
        self.layout.addWidget(self.SendButton)

        self.setLayout(self.layout)
        self.show()

    ##补充代码
    def send_msg(self):
        return 0;


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    viewer = ChatWindow_W()
    viewer.show()
    sys.exit(app.exec_())
