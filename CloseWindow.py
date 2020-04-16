import os,time
from PyQt5.Qt import QSystemTrayIcon,QIcon,QMenu,QAction,QFont,QCursor
from PyQt5.QtCore import QEvent, QSize, pyqtSlot,pyqtSignal,Qt,QRect
from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout,QFrame,\
    QApplication, QWidget,QVBoxLayout,QRadioButton,QCheckBox,QDesktopWidget
class Window(QWidget):
    Signal = pyqtSignal(bool)
    def __init__(self):
        super(Window,self).__init__()
        self.setWindowTitle("关闭")
        self.setupUi()
        self.show()
        self.resize(393, 238)
        self.center()
    def setupUi(self):
        self.widget = QWidget()
        self.Layout = QVBoxLayout(self.widget)
        self.Layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.Layout)
        self.setWindowFlag(Qt.Tool)
        self.main_widget = QWidget()
        self.Layout.addWidget(self.main_widget)
        self.closed = QPushButton(self.main_widget)
        self.closed.setGeometry(QRect(352, 10, 21, 21))
        self.closed.setObjectName("close")
        self.closed.setStyleSheet('''
        QPushButton{background:#FF6347;border-radius:10px}
        QPushButton:hover{background:red}''')
        self.close_label = QLabel(self.main_widget)
        self.close_label.setText("关闭")
        self.close_label.setGeometry(QRect(10, 10, 61, 31))
        self.close_label.setFont(QFont("Roman times",11))
        self.line = QFrame(self.main_widget)
        self.line.setGeometry(QRect(10, 30, 371, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.closer = QLabel(self.main_widget)
        self.closer.setGeometry(QRect(0, 50, 161, 30))
        self.closer.setText("是否确认关闭")
        self.closer.setFont(QFont("Roman times",15,QFont.Bold))
        self.close1 = QRadioButton(self.main_widget)
        self.close1.setGeometry(QRect(90, 100, 130, 30))
        self.close1.setText("直接关闭")
        self.close1.setChecked(True)
        self.close1.setFont(QFont("Roman times",15,QFont.Bold))
        self.close2 = QRadioButton(self.main_widget)
        self.close2.setGeometry(QRect(90, 140, 161, 30))
        self.close2.setText("最小化托盘")
        self.close2.setFont(QFont("Roman times",15,QFont.Bold))
        self.remember = QCheckBox(self.main_widget)
        self.remember.setGeometry(QRect(10, 190, 110, 30))
        self.remember.setText("记住选择")
        self.remember.setFont(QFont("Roman times",12,QFont.Bold))
        self.ok_btn = QPushButton(self.main_widget)
        self.ok_btn.setGeometry(QRect(200, 200, 80, 30))
        self.ok_btn.setText("确认")
        self.ok_btn.clicked.connect(self.on_clicked)
        self.exit_out = QPushButton(self.main_widget)
        self.exit_out.setGeometry(QRect(300, 200, 80, 30))
        self.exit_out.setText("取消")
        self.exit_out.clicked.connect(self.close)
        self.setWindowFlags(Qt.FramelessWindowHint)
    def mousePressEvent(self, event):
        try:
            if event.button()==Qt.LeftButton:
                self.m_flag=True
                self.m_Position=event.globalPos()-self.pos()
                event.accept()
                self.setCursor(QCursor(Qt.OpenHandCursor))
        except:
            pass
    def mouseMoveEvent(self, QMouseEvent):
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos()-self.m_Position)
                QMouseEvent.accept()
        except:
            pass
    def mouseReleaseEvent(self, QMouseEvent):
        try:
            self.m_flag=False
            self.setCursor(QCursor(Qt.ArrowCursor))
        except:
            pass
    def on_clicked(self):
        self.close()
        if self.close1.isChecked():
            self.chooses = True
        elif self.close2.isChecked():
            self.chooses = False
        self.Signal.emit(self.chooses)
        self.choose()
    def center(self):
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())
    def choose(self):
        if self.remember.isChecked():
            if os.path.exists('remember'):
                os.popen(r'attrib -s -r -h remember')
                time.sleep(0.5)
            with open('remember',"w") as f:
                f.write("{}".format(self.chooses))
                os.popen(r'attrib +s +r +h remember')