from socket import *
import json
# from UDPClient import http_ver

serverPort = 18000
serverName = 'localhost'
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))

print('The server is ready to receive')

b = b''
while True:
    message, clientAddress = serverSocket.recvfrom(2048)

    f = open('test.txt', mode='w')
    f.write(str(message))
    f.close()

    # http version 1.0
    # if str(message) == "b'1'":
    #     print(f"Client [{clientAddress}] chose HTTP 1.0")

    # # http version 1.1
    # elif str(message) == "b'2'":
    #     print(f"Client [{clientAddress}] chose HTTP 1.1")
    
    # else:
    #     break

    # modifiedMessage = f'''PAYLOAD LENGTH: {0}\nTCP_SYN_FLAG: {1}\nTCP_ACK_FLAG: {0}\n
    #     TCP_FIN_FLAG: {0}\nHTTP_GET_REQUEST: {1}\nHTTP_RESPONSE_STATUS_CODE: {0}\n
    #     HTTP_CLIENT_VERSION: {str(http_ver)}\nHTTP_REQUEST_PATH: {0}\nHTTP_INCLUDED_OBJECT_PATH: {0}'''

    b += message
    d = json.loads(b.decode('utf-8'))
    print(d)

    http_ver = d["HTTP_CLIENT_VERSION"]
    if message:
        tcp_syn_msg = {"PAYLOAD LENGTH": 0, 
        "TCP_SYN_FLAG": 1, 
        "TCP_ACK_FLAG": 1,
        "TCP_FIN_FLAG": 0,
        "HTTP_GET_REQUEST": 1,
        "HTTP_RESPONSE_STATUS_CODE": 0,
        "HTTP_CLIENT_VERSION": http_ver,
        "HTTP_REQUEST_PATH": 0,
        "HTTP_INCLUDED_OBJECT_PATH": 0}

        # modifiedMessage = message.decode().upper()
        msg = json.dumps(tcp_syn_msg).encode('utf-8')
        serverSocket.sendto(msg, clientAddress)

    # serverSocket.close()