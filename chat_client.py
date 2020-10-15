#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
客户端

pyqt中文学习网站：http://code.py40.com/pyqt5/16.html

'''
import socket
import sys
from threading import Thread
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
        # 创建线程 接收数据
        Thread(target=self.recv_finfor).start()

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
        input_infor = self.input_text.toPlainText()

        # 将光标移动到末尾
        self.show_text.moveCursor(QTextCursor.End)
        # 换行添加信息 并设置颜色
        self.show_text.append('<font color=\"#0000FF\">' + input_infor + '</font>')
        # 清空输入框
        self.input_text.clear()

        self.send_fser(input_infor)


    def send_fser(self, input_infor):
        '''
        将消息发送给服务器
        '''
        # 这个 encode 编码建议放在send外面，不然可能会出现编码错误！
        input_infor = input_infor.encode()
        # 报头，告诉服务器信息的长度
        data_len = "{:<15}".format(len(input_infor)).encode()
        print("{:<15}".format(len(input_infor)) + '###')
        ##################################
        ################################## 差 发送不成功

        # 发送消息
        sock.send(data_len + input_infor)

    
    def recv_finfor(self):
        '''
        接收服务器消息
        '''
        global sock

        while True:
            try:
                while True:
                    # 接收报头
                    msg_data_len = sock.recv(15)
                    # 如果报头长度为0就退出，即防止 空消息
                    if not msg_data_len:
                        break
                    # 去除右边多余空格
                    msg_len = int(msg_data_len.decode().rstrip())

                    # 接收数据长度
                    recv_size = 0
                    # 接收的数据
                    msg_data = b''
                    # 循环接收
                    while recv_size < msg_len:
                        # 接收数据大小的数据
                        temp_data = sock.recv(msg_len - recv_size)
                        # 如果没接受到，代表接收完毕，退出
                        if not temp_data:
                            break
                        # 每次接收到的数据添加到msg_data里
                        msg_data += temp_data
                        # 每次接收到的数据长度加到rece_size上
                        recv_size += len(temp_data)
                    # while循环执行完毕就会执行else
                    else:
                        # 将接收到的消息显示到聊天框  并设置颜色
                        self.show_text.append('<font color=\"#FF7F00\">' + msg_data.decode() + '</font>')
                    break
            finally:
                sock.close()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('127.0.0.1', 9999))


if __name__ == '__main__':
    # 创建套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定地址
    sock.connect(('127.0.0.1', 9999))

    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数
    app = QApplication(sys.argv)
    # 调用类
    Inter = Interface()
    # 保证程序干净的退出
    sys.exit(app.exec_())