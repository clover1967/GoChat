import socket
import threading
import sys
import time
import sqlite3
import mutex
import stopThreading
import struct


class GoChat_Server:
    def __init__(self):
        super().__init__()
        self.tcp_socket = None
        self.sever_th = None
        self.client_th = None
        self.client_socket_list = list()                    #用于轮询的客户端socket列表
        self.client_online_dict = dict()                    #在线客户端socket字典,key为账号(8byte字符串),value为socket对象
        self.client_info_dict = dict()                      #用户个人信息字典,key为账号(8byte字符串),value为list,第0个元素为密码,之后的元素为好友账号
                                                            #以上两个字典应从文件读入
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

    def signup_manage(self, message, client, length):           #服务端收到客户端的注册消息
        if len(message) < length:                               #message格式为:'1'+账号(8byte)+密码
            print("packed message might be broken")
            return
        Id = message[1:9]
        password = message[9:]
        mutex.lock.acquire()                                    #加锁
        if Id in self.client_info_dict.keys():                  #账号重复
            retmsg = '0'.encode('ascii')                        #服务端发送'0',表示注册失败
            try:                                                #使用try except语句,避免运行时爆炸
                client.sendall(retmsg)
            except Exception:
                print('client crashed')
            mutex.lock.release()                                #释放锁
            return
        self.client_info_dict[Id].append(password)              #该字典为用户个人信息,key为账号,value为列表,第0个元素为密码,之后的元素为好友账号
        retmsg = ('1' + Id).encode('ascii')                     #服务端发送'1'+账号表示注册成功
        try:
            client.sendall(retmsg)
        except Exception:
            print('client crashed')
        mutex.lock.release()

    def login_manage(self, message, client, length):            #服务端收到客户端的登陆消息
        if len(message) < length:                               #message格式为:'2'+账号(8byte)+密码
            print("packed message might be broken")
            return
        Id = message[1:9]
        password = message[9:]
        mutex.lock.acquire()
        if Id not in self.client_info_dict.keys():              #账号不存在
            retmsg = '0'.encode('ascii')                        #服务端发送'0',表示登陆失败
            try:
                client.sendall(retmsg)
            except Exception:
                print('client crashed')
            mutex.lock.release()
            return
        elif password != self.client_info_dict[Id][0]:          #密码不正确
            retmsg = '0'.encode('ascii')                        #服务端发送'0',表示登陆失败
            try:
                client.sendall(retmsg)
            except Exception:
                print('client crashed')
            mutex.lock.release()
            return
        self.client_online_dict[Id] = client                    #登陆成功,将client加入在线字典(该变量注释见init函数)
        retmsg = ('1' + Id).encode('ascii')                     #服务端发送'1'+账号表示登陆成功
        try:
            client.sendall(retmsg)
        except Exception:
            print('client crashed')
        mutex.lock.release()

    def msg_manage(self, message, length):                      #服务端收到客户端发来的一般消息
        if len(message) < length:                               #message格式为:'3'+发送者账号(8byte)+接收者账号(8byte)+消息(ascii)
            print("packed message might be broken")
            return
        from_id = message[1:9]
        to_id = message[9:17]
        mutex.lock.acquire()
        if to_id not in self.client_online_dict.keys():         #对方不在线
            retmsg = '0'.encode('ascii')
            try:
                self.client_online_dict[from_id].sendall(retmsg)
            except Exception:
                print('client crashed')
            mutex.lock.release()
            return
        try:
            binmsg = message[:length].encode('ascii')           #为了避免两条消息黏在一起,只发送符合长度的部分
            self.client_online_dict[to_id].sendall(binmsg)
        except Exception:
            print('client crashed')
        mutex.lock.release()

    def reqfriendlist_manage(self, message, length):            #服务器收到客户端发送的好友列表请求
        if len(message) < length:                               #message格式为:'4'+账号
            print("packed message might be broken")
            return
        Id = message[1:9]
        ret = str()
        i = 0
        mutex.lock.acquire()
        if Id not in self.client_info_dict.keys():              #账号对应的个人信息(密码、好友列表)不存在(不应该走到这里)
            retmsg = '0'.encode('ascii')
            try:
                self.client_online_dict[Id].sendall(retmsg)
            except Exception:
                print('client crashed')
            mutex.lock.release()
            return
        num = 0 
        for item in self.client_info_dict[Id]:                  #个人信息是一个列表,第0个元素是密码,之后的元素是好友账号(每个8byte)
            if i == 0:
                i += 1
                continue
            if item in self.client_online_dict.keys():          #只返回在线好友列表
                num += 1
                ret = ret + item
        try:
            binmsg = ret.encode('ascii')
            binmsg = '4'.encode('ascii') + struct.pack('>L', num) + binmsg
            self.client_online_dict[Id].sendall(binmsg)         #服务端发回的字节串格式是:'4'+在线好友个数(4byte整数)+在线好友账号(每个8byte)
        except Exception:
            print('client crashed')
        mutex.lock.release()

    def addfriend_manage(self, message, length):                #服务端收到客户端的加好友申请
        if len(message) < length:                               #message格式为:'5'+发送者账号(8byte)+接收者账号(8byte)
            print("packed message might be broken")
            return
        from_id = message[1:9]
        to_id = message[9:17]
        mutex.lock.acquire()
        if to_id not in self.client_online_dict.keys():         #要添加的好友不在线
            try:
                retmsg = '0'.encode('ascii')
                self.client_online_dict[from_id].sendall(retmsg)
            except Exception:
                print('client crashed')
            mutex.lock.release()
            return
        try:
            self.client_online_dict[to_id].sendall(message[:length].encode('ascii'))
        except Exception:                                       #将好友申请消息原样发送
            print('client crashed')
            mutex.lock.release()
            return
        try:
            retmsg = '1'.encode('ascii')                        #给发送方返回发送成功消息
            self.client_online_dict[from_id].sendall(retmsg)
        except Exception:
            print('client crashed')
        mutex.lock.release()

    def logout_manage(self, message, length):                   #服务端收到客户端的登出消息
        if len(message) < length:                               #message格式为:'6'+发送者账号(8byte)
            print("packed message might be broken")
            return
        Id = message[1:9]
        mutex.lock.acquire()
        if Id in self.client_online_dict.keys():                #将发送者从在线列表中移除
            self.client_online_dict[Id] = None
        mutex.lock.release()
    
    def agree_manage(self, message, length):                    #服务端收到客户端的同意添加好友消息
        if len(message) < length:                               #message格式为:'7'+同意者账号(8byte)+请求者账号(8byte)
            print("packed message might be broken")
            return
        agr_id = message[1:9]
        req_id = message[9:17]
        mutex.lock.acquire()
        if agr_id not in self.client_info_dict.keys():          #若同意者个人信息不存在(不应该走到这里)
            mutex.lock.release()
            return
        if req_id not in self.client_info_dict.keys():          #若发送者个人信息不存在
            retmsg = '0'.encode('ascii')
            try:
                self.client_online_dict[agr_id].sendall(retmsg)
            except Exception:
                print('client crashed')
            mutex.lock.release()
            return
        self.client_info_dict[agr_id].append(req_id)            #互加好友
        self.client_info_dict[req_id].append(agr_id)
        try:
            retmsg = '7'.encode('ascii')                        #向请求者发送好友申请已通过的消息('7')
            self.client_online_dict[req_id].sendall(retmsg)
        except Exception:
            print('client crashed or is not online')            #申请者可能不在线
        mutex.lock.release()

    def server_recv_manage(self, message, client):
        length = struct.unpack('>L',message[0:4])[0]        #字节串message的前4字节表示消息长度
        instr = message[4:].decode('ascii')
        if instr[0] == '1':                                 #sign up to server
            self.signup_manage(instr, client, length)
        elif instr[0] == '2':                               #log in to server
            self.login_manage(instr, client, length)
        elif instr[0] == '3':                               #send message to server
            self.msg_manage(instr, length)
        elif instr[0] == '4':                               #require for friend list to server
            self.reqfriendlist_manage(instr, length)
        elif instr[0] == '5':                               #add friend
            self.addfriend_manage(instr, length)
        elif instr[0] == '6':                               #log out to server
            self.logout_manage(instr, length)
        elif instr[0] == '7':                               #agree to add friend to server
            self.agree_manage(instr, length)
        else:
            print('unknown instruction')

if __name__ == '__main__':
    GoChat_Server()