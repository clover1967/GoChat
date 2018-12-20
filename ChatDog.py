#python3

import sys
import socket

from SignIn import SignIn_W
from SignUp import SignUp_W

import qdarkstyle
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir, QFileInfo, Qt

class ChatDog(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(350, 700)
        self.setWindowTitle("ChatDog")
        self.setUpUI()
        self.show()
        '''
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('ChatDog')

        newAct = QAction( '关于 ChatDog', self)
        newAct.triggered.connect(self.about)
        fileMenu.addAction(newAct)

        newAct = QAction('退出', self)
        newAct.triggered.connect(self.close)
        fileMenu.addAction(newAct)


        self.btn = QPushButton("登录", self)
        self.btn.resize(200, 80)
        self.btn.move((self.width() - self.btn.width()) / 2, (self.height() - self.btn.height()) /2 - self.btn.height() / 2 )
        self.btn.setFont(QFont("", 20, QFont.Bold))
        self.btn.clicked.connect(self.SignIn)

        self.btn2 = QPushButton("注册", self)
        self.btn2.resize(200, 80)
        self.btn2.move((self.width() - self.btn2.width()) / 2, (self.height() - self.btn2.height()) / 2 +self.btn2.height() /2 )
        self.btn2.setFont(QFont("", 20, QFont.Bold))
        self.btn2.clicked.connect(self.SignUp)

        self.show()
        '''
    def setUpUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('ChatDog')

        newAct = QAction( '关于 ChatDog', self)
        newAct.triggered.connect(self.about)
        fileMenu.addAction(newAct)

        newAct = QAction('退出', self)
        newAct.triggered.connect(self.close)
        fileMenu.addAction(newAct)

        menubar1 = self.menuBar()
        fileMenu = menubar1.addMenu('添加')

        newAct = QAction( '添加好友', self)
        newAct.triggered.connect(self.unwrite)
        fileMenu.addAction(newAct)

        newAct = QAction('新建群聊', self)
        newAct.triggered.connect(self.unwrite)
        fileMenu.addAction(newAct)


        self.btn = QPushButton("登录", self)
        self.btn.resize(200, 80)
        self.btn.move((self.width() - self.btn.width()) / 2, (self.height() - self.btn.height()) /2 - self.btn.height() / 2 )
        self.btn.setFont(QFont("", 20, QFont.Bold))
        self.btn.clicked.connect(self.SignIn)

        self.btn2 = QPushButton("注册", self)
        self.btn2.resize(200, 80)
        self.btn2.move((self.width() - self.btn2.width()) / 2, (self.height() - self.btn2.height()) / 2 +self.btn2.height() /2 )
        self.btn2.setFont(QFont("", 20, QFont.Bold))
        self.btn2.clicked.connect(self.SignUp)

    #事件
    def unwrite(self):
        _a_ = 1;

    def SignIn(self):
        self.SignInWindow = SignIn_W();
        self.SignInWindow.show();
        self.ShowFriends();

    def SignUp(self):
        self.SignUpWindow = SignUp_W();
        self.SignUpWindow.show();

    ##def Chatting_W(self):
    def ShowFriends(self):
        '''
        获取好友列表
        '''


        self.show();

    ## 右键菜单
    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.addAction('刷新', )
        menu.addSeparator()
        menu.addSeparator()
        menu.addAction('添加好友', )
        menu.addSeparator()
        menu.addAction('新建群聊',)
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
    viewer = ChatDog()
    sys.exit(app.exec_())
