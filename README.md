#### 消息格式：

消息类型(1byte) + 源ip（4byte）+端口（2byte）

客服端到服务端

1、注册

​	用户名（8byte）+ key

2、登录

​	用户名（8byte）+ key

3、登出

​	用户名（8byte）

4、发送消息

​	发送用户（8byte）+ 接受用户（8byte）+消息内容

5、请求好友列表

​	发送用户（8byte）

6、添加好友（好友必须在线）

​	发起：发送用户（8byte）+ 接受用户（8byte）

​	回复：发送用户（8byte）+ 接受用户（8byte）+  0(拒绝)/1（通过）（1byte）

客服端到服务端

1、回复注册

- 成功：1（1byte）+用户（8byte）
- 用户名重复：0（1byte）

2、回复登录​

- 成功：1（1byte）+ 用户（8byte）
- 用户名或密码错误：0

4、发送消息

​	发送用户（8byte）+ 接受用户（8byte）+消息内容

5、发送好友列表

​	接受用户（8byte）+  在线好友个数（1byte）+在线好友账号 8（byte）+ 离线好友个数（1byte）+离线好友账号 8（byte）

6、添加好友（好友必须在线）

​	发送用户（8byte）+ 接受用户（8byte）

s