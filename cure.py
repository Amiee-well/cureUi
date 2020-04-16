import json
import os
from random import choice
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp

from . import WindowWithTitleBar
from . import simple_qss

"""
注意:托盘图标默认名称为icon.jpg,改变该图标可在运行目录下放置该图片
- 使用示例:
    from cureUi import cure
    app = QApplication(sys.argv)
    win = cure.Windows(Examples(), 'tray name', 'pink', 'program name', 'myicon.ico')
    sys.exit(app.exec_())
"""
RESOURCE_DIR = 'beautifyUi'

def Windows(mainWidget, icon_name, theme=None, title='QCureWindow', ico_path=''):
    """
    快速创建彩色窗 (带TitleBar)
    :param mainWidget:
    :param theme:
    :param title:
    :param ico_path:
    :return:
    """
    theme = set_theme(theme)
    coolWindow = WindowWithTitleBar.WindowWithTitleBar(mainWidget, icon_name)
    coolWindow.setWindowTitle(title)
    coolWindow.setWindowIcon(QIcon(ico_path))
    coolWindow.show()
    setTheme(theme)
    return coolWindow


def set_theme(theme):
    """
    判断theme值是否为随机返回
    :param theme:
    :return:
    """
    if theme == True:
        dirList = []
        if os.path.isfile(RESOURCE_DIR):
            path = RESOURCE_DIR
        else:
            path = (os.path.split(__file__)[0] + '\\' + RESOURCE_DIR + '\\').replace('\\', '/')
        for i in os.listdir(path):
            if os.path.isdir(path + i):
                dirList.append(i)
        if len(dirList) > 0:
            return choice(dirList)
        else:
            return theme
    else:
        return theme


def setTheme(theme):
    """
    根据theme.json设置主题的qss (只改样式不加Titlebar)
    :param theme:
    :return:
    """
    THEME_FILE = RESOURCE_DIR + '/theme.json'
    if os.path.isfile(THEME_FILE):
        path = THEME_FILE
    else:
        path = (os.path.split(__file__)[0] + '\\' + THEME_FILE).replace('\\', '/')
    tDict = json.load(open(path))
    # theme.json的theme的优先级比setTheme中的theme的优先级高
    configTheme = tDict.get('theme')
    if configTheme is None or configTheme == '' or tDict.get(configTheme) is None:
        colorDict = tDict.get(theme)
    else:
        colorDict = tDict.get(configTheme)
    if colorDict is None:
        qss = simple_qss.getDefaultQss()
    else:
        qss = simple_qss.getQss(colorDict['fontLight'], colorDict['fontDark'], colorDict['normal'], colorDict['light'],
                                colorDict['deep'], colorDict['disLight'], colorDict['disDark'], theme)
    qApp.setStyleSheet(qss)
