#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
服务器
'''

import socket
import threading


def server(sock_conn, client_addr):
    '''
    聊天处理函数
    '''
    try:
        while True:
            # 设置接收套接字大小
            msg = sock_conn.recv(1024)
            # 防止发送空消息
            if not msg:
                break
            
            print(msg.decode())

            back = "收到"
            sock_conn.send(back.encode())
    finally:
        # 断开与客户端连接
        sock_conn.close()


def main():
    '''
    主函数
    '''
    # 设置套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置重用 ip 和 端口号
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定端口
    sock.bind(("127.0.0.1", 9999))
    # 设置最大连接数
    sock.listen(5)
    
    while True:
        # 阻塞，等待连接
        sock_conn, client_addr = sock.accept()
        # 创建线程处理聊天
        threading.Thread(target=server, args=(sock_conn, client_addr)).start()


if __name__ == '__main__':
    main()
