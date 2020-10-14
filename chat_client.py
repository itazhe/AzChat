#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
客户端

pyqt中文学习网站：http://code.py40.com/pyqt5/16.html

'''
import socket
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextCursor


class Interface(QWidget):
    '''
    界面
    '''
    def __init__(self):
        super().__init__()

        self.chat()

    def chat(self):
        '''
        聊天
        '''
        # 设置窗口的 位置 和 大小
        self.setGeometry(600, 300, 650, 450)
        # 设置窗口标题
        self.setWindowTitle("AzChat")
        # 设置窗口图标
        self.setWindowIcon(QIcon(r'Python的Socket网络编程\AzChat聊天工具\chat.png'))


        # 聊天框
        self.show_text = QTextEdit()
        # 禁止输入
        self.show_text.setFocusPolicy(Qt.NoFocus)
        # 输入框
        self.input_text = QTextEdit()
        # 发送按钮
        self.send_btn = QPushButton("发送")
        # 按钮事件
        self.send_btn.clicked[bool].connect(self.chat_btn)

        
        
        # 页面布局 QVBoxLayout() 纵向布局 
        layout = QVBoxLayout()
        layout.addWidget(self.show_text)
        layout.addWidget(self.input_text)
        layout.addWidget(self.send_btn)

        self.setLayout(layout)

        # 显示
        self.show()


    def chat_btn(self):
        '''
        聊天框按钮
        '''
        # self.input_text.toPlainText() 获取输入框信息
        # self.show_text.setPlainText() 设置聊天框信息

        # 将光标移动到末尾
        self.show_text.moveCursor(QTextCursor.End)
        # 换行添加信息
        self.show_text.append(self.input_text.toPlainText())
        # 清空输入框
        self.input_text.clear()




if __name__ == '__main__':
    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数
    app = QApplication(sys.argv)
    # 调用类
    Inter = Interface()
    # 保证程序干净的退出
    sys.exit(app.exec_())