# -*- coding: utf-8 -*-

"""
WINDOWS 进程守护程序
作者:韦俊杰
最后编辑: 2018年07月02日

进程未处于系统进程列表时，自动重启程序

"""

import wmi
import os
import sys
import time
from configparser import ConfigParser

import logging
from logging.handlers import TimedRotatingFileHandler

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import UI_main

import threading

LOG_FORMAT = '%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s'
formatter = logging.Formatter(LOG_FORMAT)

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(os.path.join(os.getcwd(), 'log.txt'))
fh.setLevel(logging.DEBUG)
fh = TimedRotatingFileHandler(filename='log.txt',when='midnight',interval=1,backupCount=7)
#logging.handlers.suffix = "%Y-%m-%d"

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

CONFIGFILE = './config.ini'
config = ConfigParser()
config.read(CONFIGFILE)

ProgramPath = config.get('MonitorProgramPath', 'ProgramPath')
ProcessName = config.get('MonitorProcessName', 'ProcessName')
ScanTime = int(config.get('MonitorScanTime', 'ScanTime')) * 1000

count = 0

class mainshow(QtWidgets.QWidget, UI_main.Ui_Form):
    def __init__(self):
        super(mainshow,self).__init__()
        self.setupUi(self)

        #界面风格
        QApplication.setStyle('Fusion')
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint\
                            |Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)

        self.pname.setText(str(ProcessName))
        self.textBrowser.setText(str(ProgramPath))
        self.lcdNumber.setStyleSheet("background-color: yellow;color:red")
        self.lcdNumber.display(count)

        # loopt = threading.Thread(target=self.loop, daemon=True) #自动刷新数据的线程
        # loopt.start()
        # self.main()

        #self.pushButton_2.clicked.connect(self.loop)
        self.main()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.main)
        self.timer.start(ScanTime)

    def main(self):
        ProList = []  # 如果在main()函数之外ProList 不会清空列表内容.
        global count
        c = wmi.WMI()
        for process in c.Win32_Process():
            ProList.append(str(process.Name))

        if ProcessName in ProList:
            self.STU.setStyleSheet("background-color: none;color:green")
            self.STU.setText(str("进程 " + ProcessName + " 正常运行"))
            # if os.path.isdir("c:\MonitorWin32Process"):
            #     pass
            # else:
            #     os.makedirs("c:\MonitorWin32Process")

        else:
            self.STU.setStyleSheet("background-color: yellow;color:red")
            self.STU.setText(str("进程 " + ProcessName + " 已停止！正在重启..."))
            logger.warning("进程 " + ProcessName + " 已停止")
            count = count + 1
            self.lcdNumber.display(count)
            os.startfile(ProgramPath)

    # def loop(self):
    #     #self.pushButton_2.setDisabled(True)
    #     while True:
    #         self.main()
    #         time.sleep(300)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainW = mainshow()
    MainW.show()
    sys.exit(app.exec_())