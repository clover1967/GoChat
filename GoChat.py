#python3

import sys
import socket

from LogIn import LogIn_W
from SignUp import SignUp_W
from ChatHome import ChatHome_W
from ChatWindow import ChatWindow_W
from Clinet import Clinet_S

import qdarkstyle
import sip
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir, QFileInfo, Qt

class GoChat(QMainWindow):
    #clinet = Clinet_S();
    def __init__(self):
        super().__init__()
        #服务开启
        self.clinet = Clinet_S();
        #self.clinet = Clinet_S();

        self.resize(300, 600)
        self.setWindowTitle("GoChat")
        self.widget = LogIn_W(self.clinet)
        self.setCentralWidget(self.widget)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('ChatDog')

        self.InfoAction = QAction( '关于 ChatDog', self)
        self.InfoAction.triggered.connect(self.about)
        fileMenu.addAction(self.InfoAction)

        self.LogInAction = QAction( '登录', self)
        self.LogInAction.triggered.connect(self.LogIn)
        fileMenu.addAction(self.LogInAction)

        self.SignUpAction = QAction( '注册', self)
        self.SignUpAction.triggered.connect(self.SignUp)
        fileMenu.addAction(self.SignUpAction)

        self.ExitAction = QAction('退出', self)
        self.ExitAction.triggered.connect(self.close)
        fileMenu.addAction(self.ExitAction)

        menubar1 = self.menuBar()
        fileMenu = menubar1.addMenu('添加')

        self.AddFriendsAction = QAction( '添加好友', self)
        self.AddFriendsAction.triggered.connect(self.unwrite)
        fileMenu.addAction(self.AddFriendsAction)
        self.AddFriendsAction.setEnabled(False)

        #

    #事件
    def unwrite(self):
        _a_ = 1;

    def LogIn(self):
        sip.delete(self.widget)
        self.widget = LogIn_W(self.clinet);
        self.setCentralWidget(self.widget)

    def SignUp(self):
        sip.delete(self.widget)
        self.widget = SignUp_W(self.clinet);
        self.setCentralWidget(self.widget)


    ##def Chatting_W(self):
    def ShowFriends(self):
        sip.delete(self.widget)
        self.widget = ChatHome_W();
        self.setCentralWidget(self.widget)
        self.AddFriendsAction.setEnabled(True)

    def unuse(self):
        self.ChatWindow = ChatWindow_W();
        self.ChatWindow.show()



    ## 右键菜单
    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.addAction('刷新', self.unuse)
        menu.addSeparator()
        menu.addAction('添加好友', )
        menu.addSeparator()

        menu.exec_(event.globalPos())

    def about(self):
        QMessageBox.about(self, "关于ChatDog",
                          "<b>ChatDog</b>        <br>"
                          "Author  : Sunrui Liu, Zhongli Wu  <br>"
                          "Version : 0.9      <br>")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    viewer = GoChat()
    viewer.show()
    sys.exit(app.exec_())
