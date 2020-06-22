from socket import *
import time
serverPort = 8803
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
#t=time.clock()
print('The server is ready to receive')
connectionSocket, addr = serverSocket.accept()
while True:
     sentence = connectionSocket.recv(1024).decode()
     capitalizedSentence = sentence.upper()
     connectionSocket.send(capitalizedSentence.encode())
connectionSocket.close()
                    