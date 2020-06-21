from socket import *
import time
from Main import Recording_Insertion
class Client_Request:
    def __init__(self,f,con_type,client_ip,client_port,des_ip,des_port):
        self.f = f
        self.con_type = con_type
        self.client_ip = str_to_bin_ip(client_ip)
        self.client_port = str_to_bin_port(client_port)
        self.des_ip = str_to_bin_ip(des_ip)
        self.des_port = str_to_bin_port(des_port)
    def set_f(self,F):
        self.f = F

class Proxy_Response:
    def __init__(self,message):
        self.number = message[0:2]
        self.type = message[2:5]
        self.des_ip = bin_to_str_ip(message[5:37])
        self.des_port = bin_to_str_port(message[37:53])

class Basic_information:
    def __init__(self,con_type,client_ip,client_port,proxy_server,proxy_port,des_ip,des_port):
        self.con_type = con_type
        self.client_ip = str_to_bin_ip(client_ip)
        self.client_port = str_to_bin_port(client_port)
        self.proxy_server = str_to_bin_ip(proxy_server)
        self.proxy_port = str_to_bin_port(proxy_port)
        self.des_ip = str_to_bin_ip(des_ip)
        self.des_port = str_to_bin_port(des_port)
    
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


#请求代理连接
def connect(clientSocket,information):
    #from Main import Recording_Insertion
    try:
        clientSocket.bind((information.client_ip,information.client_port))
        clientSocket.connect((information.proxy_server,information.proxy_port))
    except Exception:
        Recording_Insertion('['+time.asctime(time.localtime(time.time()))+'] '+'Connect to Proxy '+' status: Connect Error.\n','error')
        return -1
    else:
        Recording_Insertion('['+time.asctime(time.localtime(time.time()))+'] '+'Connect to Proxy '+' status: Request for Proxy OK.\n','success')
        req = Client_Request('00',information.con_type,information.client_ip,information.client_port,information.des_ip,information.des_port)
        message = req.f+req.con_type+req.client_ip+req.client_port+req.des_ip+req.des_port
        clientSocket.send(message)

#接收代理响应信息
def receive(clientSocket):
    #from Main import Recording_Insertion
    res_message = clientSocket.recv(53)
    res = Proxy_Response(res_message)
    if res.type=='000':
        Recording_Insertion('['+time.asctime(time.localtime(time.time()))+'] '+'Response form Proxy '+'status: Connect Ok.\n','success')
    elif res.type=='001':
        Recording_Insertion('['+time.asctime(time.localtime(time.time()))+'] '+'Response form Proxy '+'status: No Response.\n','error')
    elif res.type=='100':
        Recording_Insertion('['+time.asctime(time.localtime(time.time()))+'] '+'Response form Proxy '+'status: Disconnect Ok.\n','success')
    elif res.type=='101':
        Recording_Insertion('['+time.asctime(time.localtime(time.time()))+'] '+'Response form Proxy '+'status: No Response, Disconnect Error.\n','error')
    return res.type
#send message
def send_message(clientSocket,information):
    #from Main import Recording_Insertion
    Recording_Insertion('Please enter the script input test statement, the target server will automatically convert to uppercase...\n','blue')
    req = Client_Request('10',information.con_type,information.client_ip,information.client_port,information.des_ip,information.des_port)
    message = req.f+req.con_type+req.client_ip+req.client_port+req.des_ip+req.des_port
    while True:
        sentence=input('Enter your test sentence, it will be modified (Enter #01 means disconnect proxy): ')
        if sentence=='#01':
            break
        else:
            clientSocket.send(message+sentence.encode())
            modifiedSentence = clientSocket.recv()

            print('From Server:', modifiedSentence[53:].decode())
#关闭代理
def disconnect(clientSocket,information):
    #from Main import Recording_Insertion
    req = Client_Request('01',information.con_type,information.client_ip,information.client_port,information.des_ip,information.des_port)
    message = req.f+req.con_type+req.client_ip+req.client_port+req.des_ip+req.des_port
    clientSocket.send(message)
    Recording_Insertion('['+time.asctime(time.localtime(time.time()))+'] '+'Disconnect to Proxy '+'status: Request for Proxy OK.\n','success')

    res_message = clientSocket.recv(53)
    res = Proxy_Response(res_message)

    if receive(clientSocket)=='100':
        clientSocket.close()
        return 1
    else:
        return -1

#
def work(proxy_server,proxy_port):
    #
    # proxy_server = ''
    # proxy_port = 1234
    client_name = getfqdn(gethostname())
    client_ip = gethostbyname(client_name)
    client_port = 8080
    Recording_Insertion('Please enter the script to input the configuration information...\n','blue')
    clientSocket = socket(AF_INET, SOCK_STREAM)
    while True:
            con_type = input('Enter your connect type (TCP/UDP): ')
            if con_type=='TCP' or con_type=='tcp':
                con_type = '000'
                break
            elif con_type=='UDP' or con_type=='udp':
                con_type = '001'
                break
            else:
                print('Error. Please enter again.')
    address = input('Enter your destination address (xx.xx.xx.xx:xx): ')
    des_ip = address.split(':')[0]
    des_port = int(address.split(':')[1])
    information=Basic_information(con_type,client_ip,client_port,proxy_server,proxy_port,des_ip,des_port)
    connect(clientSocket,information)
    if receive(clientSocket)=='000':
        send_message(clientSocket,information)
        f=disconnect(clientSocket,information)
        if f==-1:
            return -1
        else:
            return 1
    else:
        return -1