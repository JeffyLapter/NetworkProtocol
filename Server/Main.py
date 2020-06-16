from socket import *
import json
from hashlib import *
class Proxy_Connect:
    def __init__(self,*args):
        if len(args)==0:
            self.id = '0'
            self.type = ''
            self.client_ip = 'X.X.X.X'
            self.client_port= 0
            self.des_ip = 'X.X.X.X'
            self.des_port = 0
        else:
            self.id = args[0]
            self.type = args[1]
            self.client_ip = args[2]
            self.client_port= args[3]
            self.des_ip = args[4]
            self.des_port = args[5]
    
    def connect(self):
        #TCP connection
         if self.type=='0000':    
             try:
                self.clientSocket = socket(AF_INET, SOCK_STREAM)
                self.clientSocket.connect((des_ip,des_port))
             except Exception:
                self.req_message = '0b0001'
             else:
                self.req_message = '0b0000'
        #UDP connection
         elif self.type=='0001':  
             try:
                self.clientSocket = socket(AF_INET, SOCK_DGRAM)
             except Exception:
                self.req_message = '0b0001'
             else:
                self.req_message = '0b0000'
    def disconncet(self):
        try:
            self.clientSocket.close()
        except Exception:
            self.req_message = '0b1001'
        else:
            self.req_message = '0b1000'

        
class Proxy_Response:
    def __init__(self,num,message,des_ip,des_port):
        self.number=num
        self.message=message
        self.des_ip=des_ip
        self.des_port=des_port

def bin_to_str_ip(b_ip):
    str_ip=''
    f='0b'
    for i in range(32):
        f=f+b_ip[i]
        if i%8==7:
            str_ip=str_ip+str(int(f,2))
            if i!=31:
                str_ip=str_ip+':'
            f='0b'
    return str_ip

def bin_to_str_port(b_port):
    str_port='0b'+b_port
    return int(str_port,2)

# ****************config server********************
Config_ini_path="./Server/config.json"
with open(Config_ini_path, 'r') as f:
    conf = json.load(f)    
serverport=int(conf['Port'])
# *************************************************
client_socket=[]

#receive message from client
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverport))
serverSocket.listen(1)

#analysis message and send response to client
while True:
     message=''
     connectionSocket,addr = serverSocket.accept()     
     message = connectionSocket.recv(102)
     if message[0]=='0':
         des_ip = bin_to_str_ip(message[53:85])
         des_port = bin_to_str_port(message[86:101])

         con = Proxy_Connect(md5(message[5:101]),message[1:5],bin_to_str_ip(message[5:37]),bin_to_str_port(message[37,53]),bin_to_str_ip(message[53:85]),bin_to_str_port(message[86:101]))
         client_socket.append(con)
         x=client_socket.index(con)
         client_socket[x].connect()
        
         request_C = Proxy_Response('0',client_socket[x].req_message[2:],client_socket[x].des_ip,client_socket[x].des_port)
         connectionSocket.send(request_C.number+request_C.message+request_C.des_ip+request_C.des_port)

     if message[0]=='1':
         for i in client_socket:
             if i.id == md5(message[5:101]):
                 i.disconncet()
                 if i.req_message=='0b1000':
                     del i
                     del client_socket[client_socket.index(i)]

