import win32gui
import win32con
import os,time
from PyQt5.Qt import QSizePolicy,QSystemTrayIcon,QIcon,QMenu,QAction,QFont
from PyQt5.QtCore import QEvent, QSize, pyqtSlot,pyqtSignal,Qt,QRect
from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout,QMessageBox,\
    QApplication, QWidget,QVBoxLayout,QRadioButton,QCheckBox,QDesktopWidget
from . import CloseWindow
from .resourse_cfg import *


class Titlebar(QWidget):
    # 默认基础样式参数
    TITLE_TEXT_COLOR = "white"
    BGD_COLOR = "#28AAAA"
    TITLEBAR_HEIGHT = 30
    ICON_SIZE = QSize(20, 20)
    MIN_BUTT_SIZE = QSize(27, 22)
    RET_BUTT_SIZE = QSize(27, 22)
    CLOSE_BUTT_SIZE = QSize(27, 22)
    TITLE_LABEL_NAME = "Titlebar_titleLabel"
    BACKGROUND_LABEL_NAME = "Titlebar_backgroundLabel"
    MIN_BUTT_NAME = "Titlebar_minimizeButton"
    RET_BUTT_NAME = "Titlebar_maximizeButton"
    CLOSE_BUTT_NAME = "Titlebar_closeButton"
    THEME_IMG_DIR = 'default'

    def __init__(self, parent, icon_name):
        super(Titlebar, self).__init__(parent)
        self.parentwidget = parent
        self.setFixedHeight(Titlebar.TITLEBAR_HEIGHT)
        self.icon_name = icon_name
        self.m_pBackgroundLabel = QLabel(self)
        self.m_pIconLabel = QLabel(self)
        self.m_pTitleLabel = QLabel(self)
        self.m_pMinimizeButton = QPushButton(self)
        self.m_pReturnButton = QPushButton(self)
        self.m_pCloseButton = QPushButton(self)
        self.m_pIconLabel.setFixedSize(Titlebar.ICON_SIZE)
        self.m_pIconLabel.setScaledContents(True)
        self.m_pTitleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.m_pBackgroundLabel.setObjectName(Titlebar.BACKGROUND_LABEL_NAME)
        # 三大金刚按钮大小
        self.m_pReturnButton.setFixedSize(Titlebar.RET_BUTT_SIZE)
        self.m_pMinimizeButton.setFixedSize(Titlebar.MIN_BUTT_SIZE)
        self.m_pCloseButton.setFixedSize(Titlebar.CLOSE_BUTT_SIZE)
        # 统一设置ObjName
        self.m_pTitleLabel.setObjectName(Titlebar.TITLE_LABEL_NAME)
        self.m_pBackgroundLabel.resize(self.parentwidget.width(), Titlebar.TITLEBAR_HEIGHT)
        self.m_pReturnButton.setObjectName(Titlebar.RET_BUTT_NAME)
        self.m_pMinimizeButton.setObjectName(Titlebar.MIN_BUTT_NAME)
        self.m_pCloseButton.setObjectName(Titlebar.CLOSE_BUTT_NAME)
        # 布局
        pLayout = QHBoxLayout(self)
        pLayout.addWidget(self.m_pIconLabel)
        pLayout.addSpacing(5)
        pLayout.addWidget(self.m_pTitleLabel)
        pLayout.addWidget(self.m_pReturnButton)
        pLayout.addWidget(self.m_pMinimizeButton)
        pLayout.addWidget(self.m_pCloseButton)
        pLayout.setSpacing(0)
        pLayout.setContentsMargins(5, 0, 5, 0)
        self.setLayout(pLayout)
        # 信号连接
        self.m_pReturnButton.clicked.connect(self.__slot_onclicked)
        self.m_pMinimizeButton.clicked.connect(self.__slot_onclicked)
        self.m_pCloseButton.clicked.connect(self.__slot_onclicked)
        # 置中
        self.center()
        # 设置默认样式(bar的字颜色和背景颜色)
        # self.setTitleBarStyle(Titlebar.BGD_COLOR, Titlebar.TITLE_TEXT_COLOR)

    def setTitleBarStyle(self, backgroundColor, textColor):
        # 标题字体颜色
        self.m_pTitleLabel.setStyleSheet("font-size:13px;margin-bottom:0px;color:%s" % (textColor))
        # 标题栏背景颜色
        self.m_pBackgroundLabel.setStyleSheet("background:%s" % (backgroundColor))

    def mousePressEvent(self, e):
        """
        使窗口能被拖动
        :param e:
        :return:
        """
        win32gui.ReleaseCapture()
        pWindow = self.window()
        if pWindow.isWindow():
            win32gui.SendMessage(pWindow.winId(), win32con.WM_SYSCOMMAND, win32con.SC_MOVE + win32con.HTCAPTION, 0)
        e.ignore()

    def eventFilter(self, object, e):
        if e.type() == QEvent.WindowTitleChange:
            if object != None:
                self.m_pTitleLabel.setText(object.windowTitle())
                return True
        if e.type() == QEvent.WindowIconChange:
            if object != None:
                icon = object.windowIcon()
                self.m_pIconLabel.setPixmap(icon.pixmap(self.m_pIconLabel.size()))
                return True
        if e.type() == QEvent.Resize:
            self.__setTitleBarSize(self.parentwidget.width())
            return True
        return QWidget.eventFilter(self, object, e)

    @pyqtSlot()
    def __slot_onclicked(self):
        pButton = self.sender()
        pWindow = self.window()
        if pWindow.isWindow():
            if pButton.objectName() == Titlebar.RET_BUTT_NAME:
                self.delete()
            if pButton.objectName() == Titlebar.MIN_BUTT_NAME:
                pWindow.showMinimized()
            elif pButton.objectName() == Titlebar.CLOSE_BUTT_NAME:
                self.close()
                
    def center(self):
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

    def delete(self):
        if os.path.exists('remember'):
            os.popen(r'attrib -s -r -h remember | del/s/q remember')
            QMessageBox.about(self,"成功","取消记住选择")

    def closeEvent(self,event):
        """
        关闭弹窗弹出
        :param event:
        :return:
        """
        if os.path.exists('remember'):
            with open('remember', 'r') as f:
                result = f.read()
            if result == "True":
                self.closer(True)
            else:
                event.ignore()
                self.closer(False)
            return
        event.ignore()
        self.newWindow_Close = CloseWindow.Window()
        self.newWindow_Close.Signal.connect(self.closer)

    def closer(self,choose):
        """
        托盘界面设置
        :param choose:
        :return:
        """
        if choose == True:
            QApplication.instance().quit()
        elif choose == False:
            self.window().hide()
            self.tray = QSystemTrayIcon(self)
            if os.path.exists(ICON_NORM):
                self.icon = QIcon(ICON_NORM)
            else:
                self.icon = QIcon((os.path.split(__file__)[0] + "\\beautifyUi\\").replace('\\', '/')+ICON_NORM)
            self.tray.setIcon(self.icon)
            self.tray.activated.connect(self.TuoPanEvent)
            self.tray.setToolTip(self.icon_name)
            self.tray_menu = QMenu(QApplication.desktop())
            self.RestoreAction = QAction(u'还原',self,triggered=self.window().show)
            self.QuitAction = QAction(u'退出',self,triggered=QApplication.instance().quit)
            self.tray_menu.addAction(self.RestoreAction)
            self.tray_menu.addAction(self.QuitAction)
            self.tray.setContextMenu(self.tray_menu)
            self.tray.show()
            self.tray.showMessage(self.icon_name, '托盘在这！', icon=1)
        else:
            QMessageBox.warning(self,"警告","系统出现问题,\n请稍后再试")

    def TuoPanEvent(self,reason):
        """
        托盘两键设置
        :param reason:
        :return:
        """
        qApp = QApplication.instance()
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isMinimized() or not self.isVisible():
                self.showNormal()
                self.activateWindow()
            else:
                self.showMinimized()

    def __setTitleBarSize(self, width):
        self.m_pBackgroundLabel.resize(width, Titlebar.TITLEBAR_HEIGHT)
