from socket import *
import json
import os
# from UDPClient import http_ver

serverPort = 18000
serverName = 'localhost'
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))

print('[Server] The server is ready to receive')

b = b''
c = b''
e = b''
while True:
    firstmessage, clientAddress = serverSocket.recvfrom(2048)

    # f = open('test.txt', mode='w')
    # f.write(str(message))
    # f.close()

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

    b += firstmessage
    d = json.loads(b.decode('utf-8'))
    print(d)

    http_ver = d["HTTP_CLIENT_VERSION"]
    if firstmessage:
        tcp_syn_msg = {"PAYLOAD LENGTH": 0, 
        "TCP_SYN_FLAG": 1, 
        "TCP_ACK_FLAG": 1,
        "TCP_FIN_FLAG": 0,
        "HTTP_GET_REQUEST": 0,
        "HTTP_RESPONSE_STATUS_CODE": 0,
        "HTTP_CLIENT_VERSION": http_ver,
        "HTTP_REQUEST_PATH": 0,
        "HTTP_INCLUDED_OBJECT_PATH": 0}

        # modifiedMessage = message.decode().upper()
        msg = json.dumps(tcp_syn_msg).encode('utf-8')
        serverSocket.sendto(msg, clientAddress)
        
        print("[Server] received the tcp syn message from the client")
        print("[Server] replying back...setting TCP_SYN_FLAG and TCP_ACK_FLAG to 1")

        # served received a tcp ack message from client 
        # server and client are in a tcp connection now
        tcp_message, clientAddress = serverSocket.recvfrom(2048)
        print("[Server] Received a TCP ACK message from the client...")
        print("[Server] Client and Server are in a TCP connection now!!!")

        c += tcp_message
        d = json.loads(c.decode('utf-8'))
        print(d)

        # get the http get request from the client 
        # check if the file exists in our directory
        http_message, clientAddress = serverSocket.recvfrom(2048)
        e += http_message
        d = json.loads(e.decode('utf-8'))
        print(d)

        link_to_file = e["HTTP_REQUEST_PATH"]
        cwd = os.getcwd()
        link_to_file_new = cwd + link_to_file

        # file exists
        if os.path.exists(link_to_file_new) == True:
            # status code 200 OK
            pass 
        else:
            # status code 404 page not found
            pass

    # serverSocket.close()