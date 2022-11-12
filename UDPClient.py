from socket import *
import time
import json

serverName = 'localhost'
serverPort = 18000
clientSocket = socket(AF_INET, SOCK_DGRAM)

b = b''

def send_message(clientSocket, msg):
    if type(msg) == dict:
        msg = json.dumps(msg).encode('utf-8')
        clientSocket.sendto(msg,(serverName, serverPort))
        # modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        # print(modifiedMessage.decode())

    else:
        clientSocket.sendto(str(msg).encode('base64','strict'),(serverName, serverPort))
        # modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        # print(modifiedMessage.decode())

def start():
    print("Choose one of the options from the menu:")
    print("1. Get a file from the server")
    print("2. Quit")

    message = input("Enter your selection: ")

    b = b''
    if message == "1":
        print("1. Use HTTP version 1.0 (non-persistent)")
        print("2. Use HTTP version 1.1 (persistent)")

        http_ver = input("Enter your selection: ").lower()

        if http_ver == 1:
            http_ver = 1.0
        else:
            http_ver = 1.1

        # tcp_syn_msg = f'''PAYLOAD LENGTH: {0}\nTCP_SYN_FLAG: {1}\nTCP_ACK_FLAG: {0}\n
        # TCP_FIN_FLAG: {0}\nHTTP_GET_REQUEST: {1}\nHTTP_RESPONSE_STATUS_CODE: {0}\n
        # HTTP_CLIENT_VERSION: {str(http_ver)}\nHTTP_REQUEST_PATH: {0}\nHTTP_INCLUDED_OBJECT_PATH: {0}'''

        tcp_syn_msg = {"PAYLOAD LENGTH": 0, 
        "TCP_SYN_FLAG": 1, 
        "TCP_ACK_FLAG": 0,
        "TCP_FIN_FLAG": 0,
        "HTTP_GET_REQUEST": 1,
        "HTTP_RESPONSE_STATUS_CODE": 0,
        "HTTP_CLIENT_VERSION": http_ver,
        "HTTP_REQUEST_PATH": 0,
        "HTTP_INCLUDED_OBJECT_PATH": 0}

        send_message(clientSocket, tcp_syn_msg)

        print("sent a tcp syn message to the server!!!")

        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        # print(modifiedMessage.decode())

        b += modifiedMessage
        d = json.loads(b.decode('utf-8'))
        print(d)

    else:
        return

start()

    

    
