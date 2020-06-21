#用于客户端中用到的模块
from random import randint
from simhash import hashlib
from socket import *
import time


class Delay_Test_Module:
    def __init__(self,host,port):
        self.generate_int_seed=randint(2020,99999999999999999)
        self.rand_flag=hashlib.md5(str(self.generate_int_seed).encode('utf-8'))
        self.host=host
        self.port=port
        self.ADDR=(host,port)
        self.Buffer_Size=1024
        self.udpClientSock=socket(AF_INET,SOCK_DGRAM)
        self.udpClientSock.settimeout(1)
        self.RTT=0.0
    def Get_randstring(self):
        return self.rand_flag.hexdigest()
    
    def UDP_AVG_RTT(self):
        Total_time=0.0
        for i in range(1):
            data=bytes(self.Get_randstring(),encoding='utf-8')
            start_time=time.time()
            try:
                self.udpClientSock.sendto(data,self.ADDR)
                data,self.ADDR=self.udpClientSock.recvfrom(self.Buffer_Size)
            except:
                pass
            end_time=time.time()
            use_time_single=(end_time-start_time)*1000
            Total_time+=use_time_single
        self.RTT=Total_time/1/2.0
        return self.RTT
    
#TEST=Delay_Test_Module('39.106.97.149',8777)
#print(TEST.UDP_AVG_RTT())
            