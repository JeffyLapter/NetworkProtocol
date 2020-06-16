from socket import *
import json
from hashlib import *
import time
class Proxy:
    def __init__(self,*args):
        if len(args)==0:
            self.id = '0'
            self.type = ''
            self.client_ip = 'X.X.X.X'
            self.client_port = 0
            self.des_ip = 'X.X.X.X'
            self.des_port = 0
        else:
            self.id = args[0]
            self.type = args[1]
            self.client_ip = args[2]
            self.client_port = args[3]
            self.des_ip = args[4]
            self.des_port = args[5]
    
    def connect(self):
        #TCP connection
         if self.type=='000':    
             try:
                self.clientSocket = socket(AF_INET, SOCK_STREAM)
                self.clientSocket.connect((self.des_ip,self.des_port))
             except Exception:
                self.req_message = '0b001'
                print(time.asctime('[',time.localtime(time.time())),'] ','id: ',self.id,'   ','Connection Error.')
             else:
                self.req_message = '0b000'
                print(time.asctime('[',time.localtime(time.time())),'] ','id: ',self.id,'   ','Connection OK!')
        #UDP connection
         elif self.type=='001':  
             try:
                self.clientSocket = socket(AF_INET, SOCK_DGRAM)
             except Exception:
                self.req_message = '0b001'
                print(time.asctime('[',time.localtime(time.time())),'] ','id: ',self.id,'   ','Connection Error.')
             else:
                self.req_message = '0b000'
                print(time.asctime('[',time.localtime(time.time())),'] ','id: ',self.id,'   ','Connection OK!')
    def disconncet(self):
        try:
            self.clientSocket.close()
        except Exception:
            self.req_message = '0b101'
            print(time.asctime('[',time.localtime(time.time())),'] ','id: ',self.id,'   ','Disconnection Error.')
        else:
            self.req_message = '0b100'
            print(time.asctime('[',time.localtime(time.time())),'] ','id: ',self.id,'   ','Disconnection OK!')

    def send_information(self,request):
        self.clientSocket.send(request)
        print('The message from ',self.id,' sends to destination...')
        response=self.clientSocket.recv(1024)
        print('The message has been responsed, it will be transmited.')
        return response

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
    str_ip=''
    f='0b'
    for i in range(32):
        f=f+b_ip[i]
        if i%8==7:
            str_ip=str_ip+str(int(f,2))
            if i!=31:
                str_ip=str_ip+'.'
            f='0b'
    return str_ip

def bin_to_str_port(b_port):
    str_port='0b'+b_port
    return int(str_port,2)

def str_to_bin_ip(str_ip):
    f=''
    b_ip=''
    for i in str_ip:
        if i!='.':
            f=f+i
        else:
            b_ip=b_ip+'{:08b}'.format(int(f))
            f=''
    return b_ip

def str_to_bin_port(str_port):
    b_port='{:016b}'.format(int(str_port))
    return b_port

# ****************config server********************
Config_ini_path="./Server/config.json"
with open('Config_ini_path', 'r') as f:
    conf = json.load(f)    
serverport=int(conf['Port'])
# *************************************************

client_socket=[]    #record the opening socket

#receive message from client
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverport))
serverSocket.listen(5)

#analysis message and send response to client
while True:
     message = ''
     connectionSocket,addr = serverSocket.accept()     
     message = connectionSocket.recv(1024) 

     if message[0:2]=='00':        #connect
        req = Proxy_Request(message)

        con = Proxy(md5(message[5:101]), req.type, req.client_ip, req.client_port, req.des_ip, req.des_port)
        client_socket.append(con)
        con.connect()
            
        res = Proxy_Response('00',con.req_message[2:],con.des_ip,con.des_port)
        connectionSocket.send(res.number+res.message+res.des_ip+res.des_port)

        del req
        del res

     if message[0:2]=='01':        #disconnect
        for i in client_socket:
            if i.id == md5(message[5:101]):
                i.disconncet()
                if i.req_message=='0b100':
                    res = Proxy_Response('01',i.req_message[2:],i.des_ip,i.des_port)
                    connectionSocket.send(res.number+res.message+res.des_ip+res.des_port)
                    del i
                    del client_socket[client_socket.index(i)]
                    del res
                else:
                    res = Proxy_Response('01',i.req_message[2:],i.des_ip,i.des_port)
                    connectionSocket.send(res.number+res.message+res.des_ip+res.des_port)
                    del res

     if message[0:2]=='10':     #send message
        for i in client_socket:
            if i.id == md5(message[5:101]):
                res_message = i.send_information(message[101:])
                res = Proxy_Response('10',con.req_message[2:],con.des_ip,con.des_port)
                connectionSocket.send(res.number+res.message+res.des_ip+res.des_port+res_message)


