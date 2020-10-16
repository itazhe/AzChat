#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
服务器
'''

import socket
import threading
import json


def server(sock_conn, client_addr):
    '''
    聊天处理函数
    '''
    try:
        while True:
            # 接收报头
            msg_data_len = sock_conn.recv(15)
            print(msg_data_len.decode())
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
                temp_data = sock_conn.recv(msg_len - recv_size)
                # 如果没接受到，代表接收完毕，退出
                if not temp_data:
                    break
                # 每次接收到的数据添加到msg_data里
                msg_data += temp_data
                # 每次接收到的数据长度加到rece_size上
                recv_size += len(temp_data)
            # while循环执行完毕就会执行else
            else:
                # 转发消息
                for sock_temp, temp_addr in client_socks:
                    # 排除自己
                    if sock_temp is not sock_conn:
                        try:
                            # 发送报头，数据长度
                            sock_temp.send(msg_data_len)
                            # 发送数据
                            sock_temp.send(msg_data)
                        except:
                            # 发送不到就移除
                            client_socks.remove((sock_temp, temp_addr))
                            sock_temp.close()
                continue
            break
    finally:
        client_socks.remove((sock_conn, client_addr))
        sock_conn.close()
                    

def check_login(sock_conn, client_addr):
    '''
    登录校验
    '''
    try:
        data_len = sock_conn.recv(15).decode().rstrip()
        if len(data_len) > 0:
            data_len = int(data_len)

            recv_size = 0
            recv_data = b''
            while recv_size < data_len:
                temp = sock_conn.recv(data_len - recv_size)

                if not temp:
                    break

                recv_data += temp
                recv_size += len(temp)
            
            json_data = json.loads(recv_data.decode())

            print(json_data)
            
            '''
            数据库名 azchat
            用户 azchat_u
            密码 1234567890
            '''
            


    finally:
        pass
            


def main():
    '''
    主函数
    '''
    global client_socks

    # 设置套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置重用 ip 和 端口号
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定端口
    sock.bind(("127.0.0.1", 9999))
    # 设置最大连接数
    sock.listen(5)
    
    # 连接的人
    client_socks = []

    while True:
        # 阻塞，等待连接
        sock_conn, client_addr = sock.accept()
        # 添加连接的人进去
        client_socks.append((sock_conn, client_addr))
        # 创建线程处理聊天
        threading.Thread(target=check_login, args=(sock_conn, client_addr)).start()


if __name__ == '__main__':
    main()
