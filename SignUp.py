import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
from Clinet import Clinet_S


class SignUp_W(QWidget):
    student_signup_signal = pyqtSignal(str)

    def __init__(self, client):
        super().__init__()
        self.resize(300, 600)

        self.setWindowTitle("GoChat")
        self.setUpUI()
        self.client = client

    def setUpUI(self):
        self.resize(300, 600)
        self.setWindowTitle("ChatDog")
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
        # 表单，包括ID，密码，确认密码
        self.formlayout = QFormLayout()
        font.setPixelSize(18)
        # Row1
        self.IdLabel = QLabel("账    号: ")
        self.IdLabel.setFont(font)
        self.IdLineEdit = QLineEdit()
        self.IdLineEdit.setFixedWidth(180)
        self.IdLineEdit.setFixedHeight(32)
        self.IdLineEdit.setFont(lineEditFont)
        self.IdLineEdit.setMaxLength(10)
        self.formlayout.addRow(self.IdLabel, self.IdLineEdit)

        # Row2
        '''
        self.studentNameLabel = QLabel("昵    称: ")
        self.studentNameLabel.setFont(font)
        self.studentNameLineEdit = QLineEdit()
        self.studentNameLineEdit.setFixedHeight(32)
        self.studentNameLineEdit.setFixedWidth(180)
        self.studentNameLineEdit.setFont(lineEditFont)
        self.studentNameLineEdit.setMaxLength(10)
        self.formlayout.addRow(self.studentNameLabel, self.studentNameLineEdit)

        lineEditFont.setPixelSize(10)
        '''

        # Row3
        self.passwordLabel = QLabel("密    码: ")
        self.passwordLabel.setFont(font)
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setFixedWidth(180)
        self.passwordLineEdit.setFixedHeight(32)
        self.passwordLineEdit.setFont(lineEditFont)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit.setMaxLength(16)
        self.formlayout.addRow(self.passwordLabel, self.passwordLineEdit)

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
        reg = QRegExp("PB[0~9]{7}")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.IdLineEdit.setValidator(pValidator)

        reg = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg)
        self.passwordLineEdit.setValidator(pValidator)
        self.passwordConfirmLineEdit.setValidator(pValidator)
        self.signUpbutton.clicked.connect(self.SignUp)
        self.IdLineEdit.returnPressed.connect(self.SignUp)
        #self.studentNameLineEdit.returnPressed.connect(self.SignUp)
        self.passwordLineEdit.returnPressed.connect(self.SignUp)
        self.passwordConfirmLineEdit.returnPressed.connect(self.SignUp)

    def SignUp(self):
        Id = self.IdLineEdit.text()

        #studentName = self.studentNameLineEdit.text()
        password = self.passwordLineEdit.text()
        confirmPassword = self.passwordConfirmLineEdit.text()
        if (Id == "" or password == "" or confirmPassword == ""):
            print(QMessageBox.warning(self, "警告", "表单不可为空，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            if (confirmPassword != password):
                print(QMessageBox.warning(self, "警告", "两次输入密码不一致，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
                return
            elif (confirmPassword == password):
                print(password)
                passwd_s = Clinet_S.hash(password)

                str = "1" + Id + passwd_s;
                str = str.encode('ascii')
                self.client.tcp_send(str)

                '''
                if (False):
                    print(QMessageBox.warning(self, "警告", "该账号已存在,请重新输入", QMessageBox.Yes, QMessageBox.Yes))
                    return
                else:
                    print(QMessageBox.information(self, "提醒", "您已成功注册账号!", QMessageBox.Yes, QMessageBox.Yes))
                    print(Id)
                return
                '''
            '''
            # 需要处理逻辑，1.账号已存在;2.密码不匹配;3.插入user表
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/LibraryManagement.db')
            db.open()
            query = QSqlQuery()
            if (confirmPassword != password):
                print(QMessageBox.warning(self, "警告", "两次输入密码不一致，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
                return
            elif (confirmPassword == password):
                # md5编码
                hl = hashlib.md5()
                hl.update(password.encode(encoding='utf-8'))
                md5password = hl.hexdigest()
                sql = "SELECT * FROM user WHERE StudentId='%s'" % (studentId)
                query.exec_(sql)
                if (query.next()):
                    print(QMessageBox.warning(self, "警告", "该账号已存在,请重新输入", QMessageBox.Yes, QMessageBox.Yes))
                    return
                else:
                    sql = "INSERT INTO user VALUES ('%s','%s','%s',0,0,0)" % (
                        studentId, studentName, md5password)
                    db.exec_(sql)
                    db.commit()
                    print(QMessageBox.information(self, "提醒", "您已成功注册账号!", QMessageBox.Yes, QMessageBox.Yes))
                    self.student_signup_signal.emit(studentId)
                db.close()
                return
            '''

"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = SignUpWidget()
    mainMindow.show()
    sys.exit(app.exec_())
"""
