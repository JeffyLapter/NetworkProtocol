from socket import *
import time




HOST='39.106.97.149'
PORT=8777
BUFSIZE=1024
Totaltime=0.0
Packet=10
ADDR=(HOST,PORT)
udpClientSock=socket(AF_INET,SOCK_DGRAM)
for i in range(10):
    data = bytes('aaaaaaaaaaaaaaaaa',encoding='utf-8')

    start_time=time.time()

    udpClientSock.sendto(data, ADDR)    
    data, ADDR = udpClientSock.recvfrom(BUFSIZE)
    
    end_time=time.time()
    use_time_single=(end_time-start_time)*1000
    Totaltime+=use_time_single

AVG_TIME=Totaltime/10.0/2.0

print('AVG RTT:',AVG_TIME,'ms')
    
    #print(data,'\t',later-now)

udpClientSock.close()