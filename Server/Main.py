from socket import *
import json
from hashlib import *
import time
import re
class Proxy:
    def __init__(self,*args):
        self.id = args[0]
        self.type = args[1]
        self.client_ip = args[2]
        self.client_port = args[3]
        self.des_ip = args[4]
        self.des_port = args[5]            
        self.flag = -1


class Proxy_Response:
    def __init__(self,num,message,des_ip,des_port):
        self.number = num
        self.message = message
        self.des_ip = str_to_bin_ip(des_ip)
        self.des_port = str_to_bin_port(des_port)

class Proxy_Request:
    def __init__(self,message):
        self.number = message[0:2]
        self.type = message[2:5]
        self.client_ip = bin_to_str_ip(message[5:37])
        self.client_port = bin_to_str_port(message[37:53])
        self.des_ip = bin_to_str_ip(message[53:85])
        self.des_port = bin_to_str_port(message[85:101])

def bin_to_str_ip(b_ip):
    e=re.findall('........',b_ip)
    ipstrlist=[]
    for i in e:
        ipstrlist.append(str(int(i,2)))
    ipstr='.'.join(ipstrlist)
    return ipstr

def bin_to_str_port(b_port):
    str_port='0b'+b_port
    x=int(str_port,2)
    return x

def str_to_bin_ip(str_ip):
    f=''
    b_ip=''
    for i in str_ip:
        if i!='.':
            f=f+i
        else:
            b_ip=b_ip+bin(int(f))[2:].zfill(8)
            f=''
    b_ip=b_ip+bin(int(f))[2:].zfill(8)
    return b_ip

def str_to_bin_port(str_port):
    b_port='{:016b}'.format(int(str_port))
    return b_port

def send_information(i,message):
    if i.flag==1:
            tcpSocket.send(message.encode())
            print('The message from ',i.id,' sends to destination...')
            response=tcpSocket.recv(1024).decode()
            print('The message from ',i.id,' has been responsed, it will be transmited.')
            return response
    elif i.flag==0:
            udpSocket.send(message.encode())
            print('The message from ',i.id,' sends to destination...')
            response=udpSocket.recv(1024).decode()
            print('The message from ',i.id,' has been responsed, it will be transmited.')
            return response
# ****************config server********************
Config_ini_path="./config.json"
#with open(Config_ini_path, 'r') as f:
    #conf = json.load(f)    
#serverport=int(conf['Port'])
serverport=8877
# *************************************************

client_socket=[]    #record the opening socket
##########################UDP Delay_Response##########################################

'''HOST = '0.0.0.0'
PORT = serverport
BUFSIZE = 1024
ADDR = (HOST, PORT)
udpSerSock = socket(AF_INET, SOCK_DGRAM)
udpSerSock.bind(ADDR)
while True:
    print('waiting for message...')
    data, addr = udpSerSock.recvfrom(BUFSIZE)
    if data:
        rpldata=bytes('AAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        udpSerSock.sendto(rpldata, addr)
        print('received from %s >> %s' % (addr, data))
        break
udpSerSock.close()
'''

############################Connection Contribute####################################

#receive message from client 
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverport))
serverSocket.listen(5)
tcpSocket = socket(AF_INET,SOCK_STREAM)
udpSocket = socket(AF_INET, SOCK_DGRAM)
connectionSocket,addr = serverSocket.accept()

#analysis message and send response to client
while True:
    message = ''     
    message = connectionSocket.recv(1024).decode()
   # tcpSocket = socket(AF_INET, SOCK_STREAM)
    #udpSocket = socket(AF_INET, SOCK_DGRAM)

    if message[0:2]=='00':        #connect
        req = Proxy_Request(message)
       
        con = Proxy(md5(message[5:101].encode()), req.type, req.client_ip, req.client_port, req.des_ip, req.des_port)
        client_socket.append(con)
        #print(client_socket[0].id)
        if con.type=='000':    
             try:
                print(con.des_ip,con.des_port,type(con.des_port)) 
                tcpSocket.connect((con.des_ip,con.des_port))
             except Exception:
                con.req_message = '001'
                print('[',time.asctime(time.localtime(time.time())),'] ','id: ',con.id,'   ','Connection Error.')
             else:
                con.req_message = '000'
                con.flag = 1
                print('[',time.asctime(time.localtime(time.time())),'] ','id: ',con.id,'   ','Connection OK!')
        #UDP connection
        elif con.type=='001':  
            con.req_message = '000'
            con.flag = 0
            print('[',time.asctime(time.localtime(time.time())),'] ','id: ',con.id,'   ','Working...')
            
        res = Proxy_Response('00',con.req_message,con.des_ip,con.des_port)
        res_mes = res.number+res.message+res.des_ip+res.des_port
        connectionSocket.send(res_mes.encode())

        del req
        del res

    if message[0:2]=='01':        #disconnect
       # for i in client_socket:
          #  print(i.id,'\n',md5(message[5:101].encode()))
           # if i.id == md5(message[5:101].encode()):
                try:
                    if con.flag==1:
                        tcpSocket.close()
                    else:    
                        udpSocket.close()
                except Exception:
                    con.req_message = '101'
                    print('[',time.asctime(time.localtime(time.time())),'] ','id: ',con.id,'   ','Disconnection Error.')
                else:
                    con.req_message = '100'
                    print('[',time.asctime(time.localtime(time.time())),'] ','id: ',con.id,'   ','Disconnection OK!')
                if con.req_message=='100':
                    res = Proxy_Response('01',con.req_message,con.des_ip,con.des_port)
                    res_mes = res.number+res.message+res.des_ip+res.des_port
                    connectionSocket.send(res_mes.encode())
                    connectionSocket.close()
                    del con
                   # del client_socket[client_socket.index(i)]
                    del res
                    break
                else:
                    res = Proxy_Response('01',con.req_message[2:],con.des_ip,con.des_port)
                    res_mes = res.number+res.message+res.des_ip+res.des_port
                    connectionSocket.send(res_mes.encode())
                    del res

    if message[0:2]=='10':     #send response to C
      #  for i in client_socket:
           
          #  if i.id == md5(message[5:101].encode()):
                #print(message[101:])
                res_message = send_information(con,message[101:])
                res = Proxy_Response('10','010',con.des_ip,con.des_port)
                res_mes = res.number+res.message+res.des_ip+res.des_port+res_message
                connectionSocket.send(res_mes.encode())



