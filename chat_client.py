#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
客户端

pyqt中文学习网站：http://code.py40.com/pyqt5/16.html

'''
import socket
import sys
from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFormLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QTextCursor, QPalette, QBrush, QPixmap, QFont
import json




class LoginInterface(QWidget):
    '''
    登录
    '''
    def __init__(self):
        super().__init__()
        
        # self.chat()
        self.login()
        # self.select_chat()
    
    
    def login(self):
        '''
        登录界面
        '''
        # 设置窗口的 位置 和 大小
        self.setGeometry(690, 360, 550, 400)
        # 设置窗口标题
        self.setWindowTitle("AzChat")
        # 无边框
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口图标
        self.setWindowIcon(QIcon(r'Python的Socket网络编程\AzChat聊天工具\chat.png'))

        # 设置背景图片
        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QPixmap(r"Python的Socket网络编程\AzChat聊天工具\bj.png")))
        # self.setPalette(palette)
        # 设置样式颜色
        qssStyle = '''
           QWidget{background-color: #2F4F4F}
           QPushButton{color: #B0E2FF}
           '''
        #加载设置好的样式
        self.setStyleSheet(qssStyle)

        # 用户名
        self.label_u = QLabel()
        self.label_u.setText('<font color=\"#B0E2FF\">'+ "用户名" + '</font>')
        self.label_u.setFont(QFont('Arial', 15))
        self.lineedit_u = QLineEdit()
        # self.lineedit_u.setPlaceholderText("用户名")

        # 密码
        self.label_p = QLabel()
        self.label_p.setText('<font color=\"#B0E2FF\">'+ "密码" + '</font>')
        self.label_p.setFont(QFont('Arial', 15))
        self.lineedit_p = QLineEdit()
        # 密码回显效果设置
        self.lineedit_p.setEchoMode(QLineEdit.Password)
        # self.lineedit_p.setPlaceholderText("密码")

        self.lineedit_u.setFont(QFont('Arial',15))
        self.lineedit_p.setFont(QFont('Arial',15))

        
        self.label_fg = QLabel()
        self.label_fg.setText('<font color=\"#B0E2FF\">' + "忘记密码?" + '</font>')
        # self.label_fg.linkActivated.connect(self.forget_password)
        

        # 登录按钮
        self.login_btn = QPushButton("登录")
        self.login_btn.clicked[bool].connect(self.login_req)

        # 纵向布局
        layout = QVBoxLayout()
        # 占位
        layout.addStretch(1)
        layout.addWidget(self.label_u)
        layout.addWidget(self.lineedit_u)
        layout.addWidget(self.label_p)
        layout.addWidget(self.lineedit_p)
        layout.addWidget(self.label_fg)
        layout.addStretch(1)
        layout.addWidget(self.login_btn)
        layout.addStretch(1)

        # 横向布局
        hlayout = QHBoxLayout()
        hlayout.addStretch(1)
        hlayout.addLayout(layout)
        hlayout.addStretch(1)
        
        # 设置布局
        self.setLayout(hlayout)

        self.show()

    
    def login_req(self):
        '''
        登录请求
        '''
        # 获取输入数据
        user_name = self.lineedit_u.text()
        password = self.lineedit_p.text()
        # 设置数据格式
        login_data = {"args":{"user_name": user_name, "password": password}}
        # 数据
        login_data = json.dumps(login_data).encode()
        # 数据大小
        login_data_len = "{:<15}".format(len(login_data)).encode()
        # 发送数据
        sock.send(login_data_len + login_data)
        # 接收数据
        self.login_resp()

    def login_resp(self):
        '''
        登录响应
        '''
        header_data = sock.recv(15).decode().rstrip()
        if len(header_data) > 0:
            header_data = int(header_data)

            recv_data = 0
            json_data = b''
            while recv_data < header_data:
                temp = sock.recv(header_data - recv_data)
                if not temp:
                    break

                json_data += temp
                recv_data += len(temp)

            json_data = json_data.decode()
            req = json.loads(json_data)
            
            if req["status"] == 0:
                # 验证通过
                # 关闭本页面
                self.close()
                # 跳转到另一页面，这里前面要加 self 不然页面会闪退！！
                self.skip = SelectInterface()
                

    def forget_password(self):
        '''
        忘记密码
        '''
        print(1)


class SelectInterface(QWidget):
    '''
    选择聊天
    '''
    def __init__(self):
        super().__init__()

        self.select_chat()
    
    def select_chat(self):
        '''
        登录后选择聊天界面
        '''
        self.setGeometry(1300, 200, 300, 600)
        self.setWindowTitle("AzChat")
        self.setWindowIcon(QIcon(r'Python的Socket网络编程\AzChat聊天工具\chat.png'))
        # 群聊
        self.MtoM_btn = QPushButton("加入群聊")
        self.MtoM_btn.setFont(QFont('Arial', 15))

        self.MtoM_btn.clicked[bool].connect(self.MtoM_redirect)

        layout = QVBoxLayout()
        layout.addWidget(self.MtoM_btn)

        self.setLayout(layout)

        # 设置样式颜色
        qssStyle = '''
           QWidget{background-color: #2F4F4F}
           
           '''
        #加载设置好的样式
        self.setStyleSheet(qssStyle)

        self.show()

    
    def MtoM_redirect(self):
        '''
        群聊跳转
        '''
        self.close()
        self.chat = ChatInterface()



class ChatInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.chat()

    def chat(self):
        '''
        聊天
        '''
        # 创建线程 接收数据
        Thread(target=self.recv_finfor).start()

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
    Inter = LoginInterface()
    # 保证程序干净的退出
    sys.exit(app.exec_())