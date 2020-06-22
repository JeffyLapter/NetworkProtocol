
from socket import *
from time import ctime


HOST = '0.0.0.0'
PORT = 8877
BUFSIZE = 1024
ADDR = (HOST, PORT)
udpSerSock = socket(AF_INET, SOCK_DGRAM)
udpSerSock.bind(ADDR)
while True:
    print('waiting for message...')
    data, addr = udpSerSock.recvfrom(BUFSIZE)
    rpldata=bytes('ACCEPT [%s] %s' % (ctime(), data),encoding='utf-8')
    udpSerSock.sendto(rpldata, addr)
    print('received from %s >> %s' % (addr, data))
udpSerSock.close()

