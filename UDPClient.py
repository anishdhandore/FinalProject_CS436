from socket import *
import time

serverName = 'localhost'
serverPort = 18000
clientSocket = socket(AF_INET, SOCK_DGRAM)

def send_message(clientSocket, msg):
    clientSocket.sendto(msg.encode(),(serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())

def start():
    print("Choose one of the options from the menu:")
    print("1. Get a file from the server")
    print("2. Quit")

    message = input("Enter your selection: ")

    if message == "1":
        print("1. Use HTTP version 1.0 (non-persistent)")
        print("2. Use HTTP version 1.1 (persistent)")
        http_ver = input("Enter your selection: ").lower()
        send_message(clientSocket, http_ver)

    else:
        return

start()

    

    
