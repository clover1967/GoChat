#!/usr/bin/python3
import os
import shutil
import sys
from functools import partial
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir, QFileInfo, Qt
from PIL import Image

#QMainWindow
class ImageGo(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(1000, 800)
        self.setWindowTitle("ImageGo")

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('ImageGo')

        newAct = QAction( '关于 ImageGo', self)
        newAct.triggered.connect(self.about)
        fileMenu.addAction(newAct)

        newAct = QAction('退出', self)
        newAct.triggered.connect(self.close)
        fileMenu.addAction(newAct)

        self.formats = ('.jpg', '.bmp', '.gif', '.tif', '.png')
        self.file_path = QDir.currentPath()     # 获取当前文件路径

        self.btn = QPushButton("打开图片", self)
        self.btn.resize(200, 80)
        self.btn.move((self.width() - self.btn.width()) / 2, (self.height() - self.btn.height()) /2 - self.btn.height() / 2 )
        self.btn.setFont(QFont("", 20, QFont.Bold))
        self.btn.clicked.connect(self.btnClicked)

        self.btn2 = QPushButton("格式转换", self)
        self.btn2.resize(200, 80)
        self.btn2.move((self.width() - self.btn2.width()) / 2, (self.height() - self.btn2.height()) / 2 +self.btn2.height() /2 )
        self.btn2.setFont(QFont("", 20, QFont.Bold))
        self.btn2.clicked.connect(self.SaveAll)

        self.show()

    def btnClicked(self):
        self.open()

    #获取图像列表
    def open(self, file=None):
        if file is None:
            self.chooseFile()
        else:
            self.key = file.replace("\\", "/")

        if self.key:
            self.btn.setEnabled(False)                      # 选择了文件按钮消失
            self.imgfiles = []                              # 如果选择了文件则则重新获取图像列表
            self.file_path = os.path.dirname(self.key)      # 获取文件路径
            try:
                for file in os.listdir(self.file_path):
                    if os.path.splitext(file)[1].lower() in self.formats:
                        self.imgfiles.append(self.file_path + "/" + file)
                self.count = len(self.imgfiles)             # 图像列表总数量
                self.index = self.imgfiles.index(self.key)  # 当前图像在图像列表中位置
            except FileNotFoundError:
                print("文件目录不存在！")

        self.showImage()

    # 选择图片文件
    def chooseFile(self):
        self.key, _ = QFileDialog.getOpenFileName(self, "选择文件", self.file_path,
                                                  "图片文件 (*.jpg *.bmp *.gif *.tif *.png)")

    def showImage(self):

        if self.key:
            print(QPixmap(self.key))
            self.img = QPixmap(self.key)
            if self.img.isNull():
                print(self.imgfiles)
                print(self.key)
                print(self.img)
                QMessageBox.information(
                    self, "ImageGo", "不能打开文件：%s！" % self.key)
                return

            self.scene = QGraphicsScene()
            self.view = QGraphicsView(self.scene)
            self.view.setDragMode(QGraphicsView.ScrollHandDrag)

            self.scene.clear()
            self.view.resetTransform()
            self.scene.addPixmap(self.img)

            #选择与缩放系数
            self.zoom = 1

            # 如果图片尺寸＞窗口尺寸，计算缩放系数进行缩放
            if self.img.width() > self.width() or self.img.height() > self.height():
                self.zoom = min(self.width() / self.img.width(),
                                self.height() / self.img.height()) * 0.995

            width = self.img.width()
            height = self.img.height()

            self.view.resize(width, height)
            self.setCentralWidget(self.view)
            self.updateView()
            self.show()

    #获取文件大小
    def fileSize(self, file):
        size = QFileInfo(file).size()

        if size < 1024:
            return str(size), "B"
        elif 1024 <= size < 1024 * 1024:
            return str(round(size / 1024, 2)), "KB"
        else:
            return str(round(size / 1024 / 1024, 2)), "MB"

    #图片缩小
    def zoomIn(self):
        if (self.zoom < 10):
            self.zoom *= 1.05
        self.updateView()

    #图片放大
    def zoomOut(self):
        if (self.zoom > 0.05):
            self.zoom /= 1.05
        self.updateView()

    #图片缩放到初始大小
    def zoomReset(self):
        self.zoom = 1
        self.updateView()

    #将图片调至屏幕合适大小
    def fitView(self):

        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.zoom = self.view.transform().m11()
        self.updateView()

    #更新标题信息
    def updateView(self):

        self.view.setTransform(QTransform().scale(self.zoom, self.zoom))

        self.title = os.path.basename(self.key)
        size = self.fileSize(self.key)
        self.setWindowTitle("%s(%sx%s,%s %s) - ImageGo - 第%s/%s张 %.2f%%" % (
            self.title, self.img.width(), self.img.height(), size[0], size[1],
            self.index + 1, self.count, self.zoom * 100))

    #下一张与上一张
    def dirBrowse(self, direc):

        if self.count > 1:
            self.index += direc
            if self.index > self.count - 1:
                self.index = 0
            elif self.index < 0:
                self.index = self.count - 1

            self.key = self.imgfiles[self.index]

            self.showImage()

    #鼠标滚动缩放
    def wheelEvent(self, event):

        moose = event.angleDelta().y() / 120
        if moose > 0:
            self.zoomIn()
        elif moose < 0:
            self.zoomOut()

    #另存为 支持大小缩放 格式转化
    def SaveAs(self):

        value, _= QInputDialog.getDouble(self, "图片缩放", "请输入缩放大小:", 1, 0.05, 10, 4)
        file, ok2 = QFileDialog.getSaveFileName(self, "文件另存为", self.file_path,
                                                "*.jpg;; *.bmp;; *.gif;; *.tif;; *.png")
        if ok2  :
            im = Image.open(self.imgfiles[self.index])
            i = len(file)

            path, _ = os.path.split(file)
            name, form = os.path.splitext(_)
            print(form)

            w, h = im.size
            im.thumbnail((w * value, h * value))

            if (form == '.tif'):
                print(path +" " +  name + ' .jpg')
                im.save(path + name + '.jpg')
                im2 = Image.open(path + name + '.jpg')
                im2.save(file)
                os.remove(path + name + '.jpg')
            else:
                print(file)
                im.save(file)

    #批量转化调用
    def SaveAll(self):
        self.SaveAllWindow = SaveAllWindow();
        self.SaveAllWindow.show()

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
    #图像转换器浏览器信息
    def about(self):
        QMessageBox.about(self, "关于ImageGo",
                          "<b>ImageGo</b>        <br>"
                          "Author  : Xinming Xu  <br>"
                          "Version : 1.0       <br>")



# 批量转化模块
class SaveAllWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.sec = 0
        self.setWindowTitle('全部另存为')
        self.resize(700,500)
        self.ok1 = False
        self.ok2 = False
        self.ok3 = False
        #G1 = QGridLayout(self)
        ##全局布局（注意参数 self）
        G1 = QVBoxLayout(self) #垂直布局
        #G12 = QVBoxLayout() #垂直布局

        ##局部布局
        G11 = QHBoxLayout()
        G12 = QHBoxLayout()
        G13 = QHBoxLayout()
        G14 = QHBoxLayout()


        btn1 = QPushButton(self, text = "选择文件")
        btn2 = QPushButton(self, text = "选择转换文件格式")
        btn3 = QPushButton(self, text = "选择储存地址")
        btn4 = QPushButton(self, text = "确认")
        #for btn in (btn1, btn2, btn3, btn4):
            #G11.addWidget(btn)

        btn1.clicked.connect(self.ChooseFile)
        btn2.clicked.connect(self.ChooseForm)
        btn3.clicked.connect(self.ChooseDir)
        btn4.clicked.connect(self.Change)

        self.text1 = QLineEdit()
        self.text2 = QLineEdit()
        self.text3 = QLineEdit()

        G11.addWidget(btn1);
        G11.addWidget(self.text1);
        G12.addWidget(btn2);
        G12.addWidget(self.text2);
        G13.addWidget(btn3);
        G13.addWidget(self.text3);
        G14.addWidget(btn4);


        G1.addLayout(G11)
        G1.addLayout(G12)
        G1.addLayout(G13)
        G1.addLayout(G14)

        self.setLayout(G1)
        self.show()

    # 文件选择
    def ChooseFile(self, event):

        self.Files, _ = QFileDialog.getOpenFileNames(self,
                                    "多文件选择",
                                    "/",
                                    "All Files (*);;Text Files (*.txt)")
        self.ok1 = True
        self.text1.setText(str(self.Files))
        print(self.Files)
    # 转化格式选择
    def ChooseForm(self, event):
        items = ['jpg', 'bmp', 'gif', 'tif', 'png']
        self.form, self.ok2 = QInputDialog.getItem(self, "输入框标题", "请选择格式:", items, 0, True)
        if (self.ok2 == False):
            self.text2.setText("")
        else:
            self.text2.setText(str(self.form))
        print(self.form)
    #储存目录选择
    def ChooseDir(self, event): # 文件：文件夹
        self.dir = QFileDialog.getExistingDirectory(self, "选取文件夹", "/")# 起始路径
        self.ok3 = True
        self.text3.setText(str(self.dir))
        print(self.dir)

    #转化处理
    def Change(self, event):
        print(self.ok1, self.ok2, self.ok3)
        print(self.Files)
        if(self.ok1 and self.ok2 and self.ok3):
            i = 0
            for file in self.Files:
                im = Image.open(file)
                path, _ = os.path.split(file)
                name, form = os.path.splitext(_)
                im = im.convert('RGB')
                #bmp转tif会出现问题，#当转出格式self.form=tif时，先统一转换成jpg，再从jpg转换成tif
                if (self.form =='tif' ):
                    im.save(self.dir + "/"+ "31415926" + "."+"jpg")
                    im2 = Image.open(self.dir + "/"+ "31415926" + "."+"jpg")
                    im2.save(self.dir + "/"+ name + "."+"tif")
                    os.remove(self.dir + "/"+ "31415926" + "."+"jpg")
                else:
                    #转入格式form=gif时，gif转gif的bug修正
                    if (form == '.gif' and self.form == 'gif'):
                        #shutil.copyfile(文件1，文件2)：不用打开文件，直接用文件名进行覆盖copy。
                        shutil.copyfile(file,self.dir + "/"+ name + "."+self.form)
                    else:
                        im.save(self.dir + "/"+ name + "."+self.form)

            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageGo()
    sys.exit(app.exec_())
