import socket
import threading
import sys
import time
import sqlite3


class Clinet_S:
    link = False
    def __init__(self):
        self.tcp_client_start()

    def tcp_client_start(self):
        """
        功能函数，TCP客户端连接其他服务端的方法
        :return:
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            address = ('192.168.1.107', int(9999))
        except Exception as ret:
            msg = '请检查目标IP，目标端口\n'
            print(msg)
        else:
            try:
                msg = '正在连接目标服务器\n'
                print(msg)
                self.tcp_socket.connect(address)
            except Exception as ret:
                msg = '无法连接目标服务器\n'
                print(msg)
            else:
                self.client_th = threading.Thread(target=self.tcp_client_concurrency, args=(address,))
                self.client_th.start()
                self.link = 1;
                msg = 'TCP客户端已连接IP:%s端口:%s\n' % address
                print(msg)

    def tcp_client_concurrency(self, address):
        """
        功能函数，用于TCP客户端创建子线程的方法，阻塞式接收
        :return:
        """
        while True:
            recv_msg = self.tcp_socket.recv(1024)
            if recv_msg:
                msg = recv_msg.decode('ascii')
                msg = '来自IP:{}端口:{}:\n{}\n'.format(address[0], address[1], msg)
                self.signal_write_msg.emit(msg)
            else:
                self.tcp_socket.close()
                self.reset()
                msg = '从服务器断开连接\n'
                self.signal_write_msg.emit(msg)
                break

    def tcp_send(self, message):
        """
        功能函数，用于TCP服务端和TCP客户端发送消息
        :return: None
        """
        if self.link is False:
            msg = '请选择服务，并点击连接网络\n'
            print(msg)
        else:
            try:
                send_msg = (str(message)).encode('ascii')
                self.tcp_socket.send(send_msg)
                msg = 'TCP客户端已发送\n'
                print(msg)
            except Exception as ret:
                msg = '发送失败\n'
                print(msg)

    def tcp_close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        if self.comboBox_tcp.currentIndex() == 0:
            try:
                for client, address in self.client_socket_list:
                    client.close()
                self.tcp_socket.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                pass
        if self.comboBox_tcp.currentIndex() == 1:
            try:
                self.tcp_socket.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                pass
        try:
            stopThreading.stop_thread(self.sever_th)
        except Exception:
            pass
        try:
            stopThreading.stop_thread(self.client_th)
        except Exception:
            pass
