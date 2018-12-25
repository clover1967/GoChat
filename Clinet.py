import socket
import threading
import sys
import time
import sqlite3
import struct
import hashlib


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
            address = ('127.0.0.1', int(9999))
        except Exception as ret:
            msg = '请检查目标IP，目标端口\n'
            print(msg)
        else:
            try:
                msg = '正在连接目标服务器\n'
                print(msg)
                print(address)
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
                print(msg)
            else:
                self.tcp_socket.close()
                self.reset()
                msg = '从服务器断开连接\n'
                print(msg)
                break

    def tcp_send(self, message):
        """
        功能函数，用于TCP服务端和TCP客户端发送消息
        :return: None
        """
        print(message)
        length = len(message)
        message = struct.pack('>L', length) + message
        print(message)

        if self.link is False:
            msg = '请选择服务，并点击连接网络\n'
            print(msg)
        else:
            try:
                self.tcp_socket.send(message)
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

    '''
    消息处理
    '''

    def server_recv_manage(self, message, client):
        print("server_recv_manage")
        print(message)
        length = struct.unpack('>L',message[0:4])[0]        #字节串message的前4字节表示消息长度
        instr = message[4:].decode('ascii')
        print(length, instr)
        if instr[0] == '1':                                 #sign up to server
            self.signup_manage(instr, client, length)
        elif instr[0] == '2':                               #log in to server
            self.login_manage(instr, client, length)
        elif instr[0] == '4':                               #send message to server
            self.msg_manage(instr, length)
        elif instr[0] == '5':                               #require for friend list to server
            self.recfriendlist_manage(instr, length)
        elif instr[0] == '6':                               #add friend
            self.addfriend_manage(instr, length)
        elif instr[0] == '':                               #log out to server
            self.logout_manage(instr, length)
        elif instr[0] == '7':                               #agree to add friend to server
            self.agree_manage(instr, length)
        else:
            print('unknown instruction')

    '''
    一些函数
    '''
    def get_ip_port(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            my_addr = s.getsockname()
        except Exception as ret:
            # 若无法连接互联网使用，会调用以下方法
            try:
                my_addr = socket.gethostbyname(socket.gethostname())
            except Exception as ret_e:
                print("无法获取ip，请连接网络！\n")
        finally:
            s.close()

        return my_addr

    def hash(src):
        src = (src + "qewrqefasafsdafa").encode('ascii')
        m = hashlib.md5()
        m.update(src)
        return m.hexdigest()
