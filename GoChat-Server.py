import socket
import threading
import sys
import time
import sqlite3
import mutex
import stopThreading


class GoChat_Server:
    def __init__(self):
        super().__init__()
        self.tcp_socket = None
        self.sever_th = None
        self.client_th = None
        self.client_socket_list = list()
        self.client_online_dict = dict()
        self.client_info_dict = dict()

        self.link = False  # 用于标记是否开启了连接

        #开启ID-Key数据库
        self.conn = sqlite3.connect("user.db")

        self.tcp_server_start()

    def tcp_server_start(self):
        """
        功能函数，TCP服务端开启的方法
        :return: None
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设定套接字为非阻塞式
        self.tcp_socket.setblocking(False)
        try:
            port = 9999
            self.tcp_socket.bind(('', port))
        except Exception as ret:
            msg = '请检查端口号\n'
            print(msg)
        else:
            self.tcp_socket.listen()
            self.sever_th = threading.Thread(target=self.tcp_server_concurrency)
            self.sever_th.start()
            msg = 'TCP服务端正在监听端口:%s\n' % str(port)
            print(msg)

    def tcp_server_concurrency(self):
        """
        功能函数，供创建线程的方法；
        使用子线程用于监听并创建连接，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客户端消息，减少系统资源浪费，使软件轻量化
        :return:None
        """
        while True:
            try:
                client_socket, client_address = self.tcp_socket.accept()
            except Exception as ret:
                time.sleep(0.001)
            else:
                client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表,client_address为ip和端口的元组
                self.client_socket_list.append((client_socket, client_address))
                msg = 'TCP服务端已连接IP:%s端口:%s\n' % client_address
                print(msg)

            # 轮询客户端套接字列表，接收数据
            for client, address in self.client_socket_list:
                try:
                    recv_msg = client.recv(1024)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        msg = recv_msg.decode('ascii')
                        print(msg)
                        self.server_recv_manage(recv_msg, client)
                        msg = '来自IP:{}端口:{}:\n{}\n'.format(address[0], address[1], msg)
                        print(msg)
                    else:
                        client.close()
                        self.client_socket_list.remove((client, address))

    def tcp_send(self):
        """
        功能函数，用于TCP服务端和TCP客户端发送消息
        :return: None
        """
        if self.link is False:
            msg = '请选择服务，并点击连接网络\n'
            self.signal_write_msg.emit(msg)
        else:
            try:
                send_msg = (str(self.textEdit_send.toPlainText())).encode('utf-8')
                # 向所有连接的客户端发送消息
                for client, address in self.client_socket_list:
                    client.send(send_msg)
                msg = 'TCP服务端已发送\n'
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

    #以下是服务端处理客户端发来的消息的函数

    def signup_manage(self, message, client):
        if len(message) < 9:
            print("packed message might be damaged")
            return
        Id = message[1:9]
        password = message[9:]
        mutex.lock.acquire()
        if Id in self.client_info_dict.keys():
            retmsg = '0'.encode('ascii')
            try:
                client.sendall(retmsg)
            except Exception:
                pass
            mutex.lock.release()
            return
        self.client_info_dict[Id].append(password)
        retmsg = ('1' + Id).encode('ascii')
        try:
            client.sendall(retmsg)
        except Exception:
            pass
        mutex.lock.release()

    def login_manage(self, message, client):
        if len(message) < 9:
            print("packed message might be damaged")
            return
        Id = message[1:9]
        password = message[9:]
        mutex.lock.acquire()
        if Id not in self.client_info_dict.keys():
            retmsg = '0'.encode('ascii')
            try:
                client.sendall(retmsg)
            except Exception:
                pass
            mutex.lock.release()
            return
        elif password != self.client_info_dict[Id][0]:
            retmsg = '0'.encode('ascii')
            try:
                client.sendall(retmsg)
            except Exception:
                pass
            mutex.lock.release()
            return
        self.client_online_dict[Id] = client
        retmsg = ('1' + Id).encode('ascii')
        try:
            client.sendall(retmsg)
        except Exception:
            pass
        mutex.lock.release()

    def msg_manage(self, message):
        if len(message) < 17:
            print("packed message might be damaged")
            return
        from_id = message[1:9]
        to_id = message[9:17]
        mutex.lock.acquire()
        if to_id not in self.client_online_dict.keys():
            retmsg = '0'.encode('ascii')
            try:
                self.client_online_dict[from_id].sendall(retmsg)
            except Exception:
                pass
            mutex.lock.release()
            return
        try:
            binmsg = message.encode('ascii')
            self.client_online_dict[to_id].sendall(binmsg)
        except Exception:
            pass
        mutex.lock.release()

    def reqfriendlist_manage(self, message):
        if len(message) < 9:
            print("packed message might be damaged")
            return
        Id = message[1:9]
        ret = str()
        i = 0
        mutex.lock.acquire()
        num = len(self.client_info_dict[Id]) - 1
        for item in self.client_info_dict[Id]:
            if i == 0:
                i += 1
                ret = ret + str(num)
                continue
            ret = ret + item
        try:
            binmsg = ret.encode('ascii')
            self.client_online_dict[Id].sendall(binmsg)
        except Exception:
            pass
        mutex.lock.release()

    def addfriend_manage(self, message):
        if len(message) < 17:
            print("packed message might be damaged")
            return
        from_id = message[1:9]
        to_id = message[9:17]
        mutex.lock.acquire()
        if to_id not in self.client_online_dict.keys():
            try:
                retmsg = '0'.encode('ascii')
                self.client_online_dict[from_id].sendall(retmsg)
            except Exception:
                pass
            mutex.lock.release()
            return
        try:
            self.client_online_dict[to_id].sendall(message.encode('ascii'))
        except Exception:
            pass
        try:
            retmsg = '1'.encode('ascii')
            self.client_online_dict[from_id].sendall(retmsg)
        except Exception:
            pass
        mutex.lock.release()

    def logout_manage(self, message):
        if len(message) < 9:
            print("packed message might be damaged")
            return
        Id = message[1:9]
        mutex.lock.acquire()
        if Id in self.client_online_dict.keys():
            self.client_online_dict[Id] = None
        mutex.lock.release()

    def server_recv_manage(self, message, client):
        instr = message.decode('ascii')
        if instr[0] == '1':                    #sign up to server
            self.signup_manage(instr, client)
        elif instr[0] == '2':                  #log in to server
            self.login_manage(instr, client)
        elif instr[0] == '3':                  #send message to server
            self.msg_manage(instr)
        elif instr[0] == '4':                  #require for friend list to server
            self.reqfriendlist_manage(instr)
        elif instr[0] == '5':                  #add friend
            self.addfriend_manage(instr)
        elif instr[0] == '6':                  #log out to server
            self.logout_manage(instr)
        else:
            print('unknown instruction')

if __name__ == '__main__':
    GoChat_Server()