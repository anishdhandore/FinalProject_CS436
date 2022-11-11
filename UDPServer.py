from socket import *

serverPort = 18000
serverName = 'localhost'
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))

print('The server is ready to receive')

while True:
    message, clientAddress = serverSocket.recvfrom(2048)

    # f = open('test.txt', mode='w')
    # f.write(str(message))
    # f.close()

    # http version 1.0
    if str(message) == "b'1'":
        print(f"Client [{clientAddress}] chose HTTP 1.0")

    # http version 1.1
    elif str(message) == "b'2'":
        print(f"Client [{clientAddress}] chose HTTP 1.1")
    
    else:
        break

    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode('utf-8'), clientAddress)