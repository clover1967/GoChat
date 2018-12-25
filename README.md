# 消息格式：

消息长度(4byte)+消息类型(1byte) + 不同类型的消息说明

例如：

客服端到服务端的注册消息`b'\x00\x00\x00)18765432177d70a48e73f8d29953bf4cdde119619'`其中`b'\x00\x00\x00)`为消息长度，消息类型为`1`,用户名为`87654321`,key为`77d70a48e73f8d29953bf4cdde119619`。

## 客服端到服务端

1、注册

​	用户名（8byte）+ key（40byte）

2、登录

​	用户名（8byte）+ key（40byte）

3、登出

​	用户名（8byte）

4、发送消息

​	发送用户（8byte）+ 接受用户（8byte）+消息内容

5、请求好友列表

​	发送用户（8byte）

6、添加好友（好友必须在线）

​	发起：发送用户（8byte）+ 接受用户（8byte）

​	回复：发送用户（8byte）+ 接受用户（8byte）+  0(拒绝)/1（通过）（1byte）

7、删除好友

## 服务端到客服端

1、回复注册

- 成功：1（1byte）+用户（8byte）
- 用户名重复：0（1byte）

2、回复登录

- 成功：1（1byte）+ 用户（8byte）
- 用户名或密码错误：0

4、发送消息

​	发送用户（8byte）+ 接受用户（8byte）+消息内容

5、发送好友列表

​	接受用户（8byte）+  在线好友个数（1byte）+在线好友账号 8（byte）+ 离线好友个数（1byte）+离线好友账号 8（byte）

6、添加好友（好友必须在线）

​	发送用户（8byte）+ 接受用户（8byte）

7、删除好友