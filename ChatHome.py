# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
from PyQt5.QtSql import *

from ChatWindow import ChatWindow_W



class ChatHome_W(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 600)
        self.setWindowTitle("GoChat")
        self.setUpUI()

    def setUpUI(self):
        self.layout = QVBoxLayout()
        self.FriendLabel = QLabel("好友")
        self.FriendLabel.setFixedHeight(32)
        self.FriendLabel.setFixedWidth(60)
        font = QFont()
        font.setPixelSize(18)
        self.FriendLabel.setFont(font)

        self.FriendTableView = QTableView()
        self.FriendTableView.horizontalHeader().setStretchLastSection(True)
        self.FriendTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.FriendTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        '''
        读取好友表单
        [账号，是否在线]
        '''

        self.layout.addWidget(self.FriendLabel)
        self.layout.addWidget(self.FriendTableView)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    viewer = GoChat()
    viewer.show()
    sys.exit(app.exec_())
