# NetworkProtocol
Creat a new network protocol with Python-Sockets

## 项目开发文档

开发方向确定：具备代理功能的软件，分为模拟服务端、代理端、客户端，实现类socks协议。

服务端与代理端不使用GUI界面，客户端有GUI界面（选）。

类socks协议底层使用TCP作为主要协议，UDP协议可用于延迟测试和服务节点的自动选定。不设置身份认证。

#### 一、Requirements

Python 3.6.5 -3.7

GUI: tkinter

#### 二、通讯流程设计

1. 客户端向代理服务器发起请求（UDP），并与响应最快的代理相连（TCP）

2. 客户端向代理发送服务端ip和端口 

3. 代理与服务端建立连接（TCP）

4. 客户端选择协议，经代理向客户端发起请求

5. 服务端响应并经代理向客户端回复

   ##### 应用层协议的交换

6. 客户端向代理发送断开连接请求 

7. 代理向客户端发送收到请求，并断开与服务端连接 

8. 断开连接后向客户端发送已断开信号 

9. 客户端收到向代理发送信号 

10. 代理端收到客户端信号，结束通信 

#### 三、通讯协议设计

##### 1.延迟检测部分

###### 客户端：

采用UDP协议，主要在客户端完成检测。单次延迟测试在客户端生成一个随机整数，并取md5值作为标识位，发送至服务端。默认单次延迟测试，发送十个数据包，发送开始时记录一次时间，收到响应后记录一次时间，记录10次响应差值，取平均值，计算AVG RTT，作为服务器延迟。

代理默认采用自动选路模式，按照服务器列表中的顺序，对服务器进行逐个测速，选取RTT最小的服务器作为代理服务器，也可在设置-代理模式中更改为手动连接模式。手动模式中仅对选框中的服务器进行测速和连接操作。

测速超时时间默认为2。

###### 服务端：

监听本地udp端口，当服务端接收到客户端送来的标识位，响应一串随机信息。

##### 2. 通讯建立

##### 客户端：
时延模块测试完成后，将与代理服务端的时延返回到日志中，并自动选取时延最低服务端进行TCP连接。由用户指定目标服务器的ip、端口和连接类型，将数据封装为请求代理消息发送到代理服务端。并等待代理服务端的响应。

##### 服务端：
客户端经TCP连接将代理请求头发送到代理服务端，代理服务端接收并生成Proxy对象，并生成唯一的id记录。代理服务端解析请求头并与目标服务器发起指定类型连接，并将连接结果封装为响应报文返回客户端。

##### 3. 通讯转发

##### 客户端：
客户端提示输入字符串，输入完成后在消息前加上转发请求头并编码，经代理服务端解析请求头后，转发到目标服务端。目标服务端接收字符串并大写字符串，响应经代理服务端接收后加上代理响应头并编码，转发到客户端。客户端拆分响应头并解析。

##### 服务端：
客户端将请求转发数据发送至代理服务端，代理服务端根据消息头与Proxy对象匹配，并将请求头拆解，将数据转发到目标服务器。目标服务器响应数据到代理服务端接收，代理服务端在数据前封装代理响应头发送给客户端。完成转发。

##### 4. 通讯端开

##### 客户端：
客户端封装断连请求头并发送到代理服务端，代理服务端接收后与目标服务器断开连接，并将断开连接结果封装为代理响应头返回客户端。

##### 服务端：
客户端将断连请求发送至代理服务端，代理服务端根据消息头与Proxy对象匹配，并与指定目的服务器断开连接。若成功断开连接则销毁对象，并响应客户端，后断开与客户端的连接。反之则保留连接，响应客户端断连失败，不销毁对象。

#### 四、功能设计&GUI设计
代理连接
目标服务器对字符串大写处理


GUI设计包配置文件选项、延迟测试、连接按钮、连接状态显示、日志等

#### 五、模块化设计
1.UDP延迟检测模块
2.基于SOCKS协议的建立连接 断开连接模块
3.GUI
4.依应用层协议传输数据（选）

#### 六、接口开发规范

#####客户端：
GUI界面作为主程序，UDP时延模块与TCP连接模块提供接口
UDP时延模块为TCP连接模块提供代理服务器参数

#####服务端：
TCP连接作为主程序，UDP时延模块提供接口

#### 七、分工&项目时间表

##Nothing_H:
TCP建立代理连接模块---代理的构建、转发和删除
##LapterGrsd：
GUI界面设计 && UDP时延测试模块

开发周期：
6.8---6.11 设计思路讨论，协议构造，原理分析，消息头构造
6.12---6.18 项目设计并完成测试
