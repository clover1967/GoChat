#python3

import sys
import socket
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir, QFileInfo, Qt

class ChatDog(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(1000, 800)
        self.setWindowTitle("ChatDog")

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
        self.btn.clicked.connect(self.Login)

        self.btn2 = QPushButton("注册", self)
        self.btn2.resize(200, 80)
        self.btn2.move((self.width() - self.btn2.width()) / 2, (self.height() - self.btn2.height()) / 2 +self.btn2.height() /2 )
        self.btn2.setFont(QFont("", 20, QFont.Bold))
        #self.btn2.clicked.connect(self.SaveAll)

        self.show()

    #事件
    def Login(self):
        self.LoginWindow = LoginWindow();
        self.LoginWindow.show()


    #更新标题信息
    def updateView(self):

        self.view.setTransform(QTransform().scale(self.zoom, self.zoom))

        self.title = os.path.basename(self.key)
        size = self.fileSize(self.key)
        self.setWindowTitle("%s(%sx%s,%s %s) - ImageGo - 第%s/%s张 %.2f%%" % (
            self.title, self.img.width(), self.img.height(), size[0], size[1],
            self.index + 1, self.count, self.zoom * 100))

    # 右键菜单
    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.addAction('放大', self.zoomIn)
        menu.addAction('缩小', self.zoomOut)
        menu.addSeparator()
        menu.addSeparator()
        menu.addAction('下一张', partial(self.dirBrowse, 1))
        menu.addAction('上一张', partial(self.dirBrowse, -1))
        menu.addSeparator()
        menu.addAction('适合屏幕', self.fitView)
        menu.addAction('实际尺寸', self.zoomReset)
        menu.addSeparator()
        menu.addAction('打开', self.open)
        menu.addAction('另存为(图片缩放，格式转化)', self.SaveAs)
        menu.addAction('批量格式转换', self.SaveAll)

        menu.exec_(event.globalPos())


    def about(self):
        QMessageBox.about(self, "关于ChatDog",
                          "<b>ChatDog</b>        <br>"
                          "Author  : Sunrui Liu, Zhongli Wu  <br>"
                          "Version : 0.9      <br>")


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setUpUI();

    def setUpUI(self):
        self.resize(900, 600)
        self.setWindowTitle("欢迎登陆图书馆管理系统")
        self.signUpLabel = QLabel("注   册")
        self.signUpLabel.setAlignment(Qt.AlignCenter)
        # self.signUpLabel.setFixedWidth(300)
        self.signUpLabel.setFixedHeight(100)
        font = QFont()
        font.setPixelSize(36)
        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)
        self.signUpLabel.setFont(font)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.signUpLabel, Qt.AlignHCenter)
        self.setLayout(self.layout)
        # 表单，包括学号，姓名，密码，确认密码
        self.formlayout = QFormLayout()
        font.setPixelSize(18)
        # Row1
        self.studentIdLabel = QLabel("学    号: ")
        self.studentIdLabel.setFont(font)
        self.studentIdLineEdit = QLineEdit()
        self.studentIdLineEdit.setFixedWidth(180)
        self.studentIdLineEdit.setFixedHeight(32)
        self.studentIdLineEdit.setFont(lineEditFont)
        self.studentIdLineEdit.setMaxLength(10)
        #self.formlayout.addRow(self.studentIdLabel, self.studentIdLineEdit)

        # Row2
        self.studentNameLabel = QLabel("姓    名: ")
        self.studentNameLabel.setFont(font)
        self.studentNameLineEdit = QLineEdit()
        self.studentNameLineEdit.setFixedHeight(32)
        self.studentNameLineEdit.setFixedWidth(180)
        self.studentNameLineEdit.setFont(lineEditFont)
        self.studentNameLineEdit.setMaxLength(10)
        #self.formlayout.addRow(self.studentNameLabel, self.studentNameLineEdit)

        lineEditFont.setPixelSize(10)

        # Row3
        self.passwordLabel = QLabel("密    码: ")
        self.passwordLabel.setFont(font)
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setFixedWidth(180)
        self.passwordLineEdit.setFixedHeight(32)
        self.passwordLineEdit.setFont(lineEditFont)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit.setMaxLength(16)
        #self.formlayout.addRow(self.passwordLabel, self.passwordLineEdit)

        # Row4
        self.passwordConfirmLabel = QLabel("确认密码: ")
        self.passwordConfirmLabel.setFont(font)
        self.passwordConfirmLineEdit = QLineEdit()
        self.passwordConfirmLineEdit.setFixedWidth(180)
        self.passwordConfirmLineEdit.setFixedHeight(32)
        self.passwordConfirmLineEdit.setFont(lineEditFont)
        self.passwordConfirmLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordConfirmLineEdit.setMaxLength(16)
        self.formlayout.addRow(self.passwordConfirmLabel, self.passwordConfirmLineEdit)

        # Row5
        self.signUpbutton = QPushButton("注 册")
        self.signUpbutton.setFixedWidth(120)
        self.signUpbutton.setFixedHeight(30)
        self.signUpbutton.setFont(font)
        self.formlayout.addRow("", self.signUpbutton)
        widget = QWidget()
        widget.setLayout(self.formlayout)
        widget.setFixedHeight(250)
        widget.setFixedWidth(300)
        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(widget, Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(self.Hlayout)
        self.layout.addWidget(widget, Qt.AlignHCenter)

        # 设置验证
        reg = QRegExp("PB[0~9]{8}")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.studentIdLineEdit.setValidator(pValidator)

        reg = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg)
        self.passwordLineEdit.setValidator(pValidator)
        self.passwordConfirmLineEdit.setValidator(pValidator)
        self.signUpbutton.clicked.connect(self.SignUp)
        self.studentIdLineEdit.returnPressed.connect(self.SignUp)
        self.studentNameLineEdit.returnPressed.connect(self.SignUp)
        self.passwordLineEdit.returnPressed.connect(self.SignUp)
        self.passwordConfirmLineEdit.returnPressed.connect(self.SignUp)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ChatDog()
    sys.exit(app.exec_())
