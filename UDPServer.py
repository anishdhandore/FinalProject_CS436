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
    b += firstmessage
    d = json.loads(b.decode('utf-8'))

    #Use HTTP version desired by client
    http_ver = d["HTTP_CLIENT_VERSION"]

    #Initiate TCP connection with client
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

        # get the http get request from the client 
        # check if the file exists in our directory
        http_message, clientAddress = serverSocket.recvfrom(2048)
        e += http_message
        d = json.loads(e.decode('utf-8'))

        link_to_file = d["HTTP_REQUEST_PATH"]
        cwd = os.getcwd()
        link_to_file_new = cwd + "/" + link_to_file

        # file does not exists
        if os.path.exists(link_to_file_new) == False:
            # status code 404 page not found
            # server sends message to client with 404 error

            error_message = {"PAYLOAD LENGTH": 0, 
            "TCP_SYN_FLAG": 0, 
            "TCP_ACK_FLAG": 0,
            "TCP_FIN_FLAG": 0,
            "HTTP_GET_REQUEST": 0,
            "HTTP_RESPONSE_STATUS_CODE": 404,
            "HTTP_CLIENT_VERSION": http_ver,
            "HTTP_REQUEST_PATH": link_to_file,
            "HTTP_INCLUDED_OBJECT_PATH": 0}

            error_msg = json.dumps(error_message).encode('utf-8')
            serverSocket.sendto(error_msg, clientAddress) 

            # receive the TCP FIN message from the client
            tcp_fin_message, clientAddress = serverSocket.recvfrom(2048)

            # send the tcp fin ack message to the server
            tcp_fin_ack = {"PAYLOAD LENGTH": 0, 
            "TCP_SYN_FLAG": 0, 
            "TCP_ACK_FLAG": 0,
            "TCP_FIN_FLAG": 0,
            "HTTP_GET_REQUEST": 0,
            "HTTP_RESPONSE_STATUS_CODE": 404,
            "HTTP_CLIENT_VERSION": http_ver,
            "HTTP_REQUEST_PATH": link_to_file,
            "HTTP_INCLUDED_OBJECT_PATH": 0}
            tcp_fin_ack_msg = json.dumps(tcp_fin_ack).encode('utf-8')
            serverSocket.sendto(tcp_fin_ack_msg, clientAddress) 

            break

        else:
            # status code 200 OK
            file = open(link_to_file_new, mode='r')
            file_contents = file.read()
            file.close()

            # set the status code to 200
            # include the link to the html file 
            # include link to any object path
            # include the contents of the file
            # send the file to the client

            object_path = ""

            # first file has no objects
            if link_to_file == "attachments/file1.html":
                pass
            # second file has link to third file
            elif link_to_file == "attachments/file2.html":
                object_path += "attachments/file3.html"
            # third file has link to second file
            elif link_to_file == "attachments/file1.html":
                object_path += "attachments/file2.html"
            else:
                pass

            final_message = {"PAYLOAD LENGTH": 0, 
            "TCP_SYN_FLAG": 0, 
            "TCP_ACK_FLAG": 0,
            "TCP_FIN_FLAG": 0,
            "HTTP_GET_REQUEST": 0,
            "HTTP_RESPONSE_STATUS_CODE": 200,
            "HTTP_CLIENT_VERSION": http_ver,
            "HTTP_REQUEST_PATH": link_to_file,
            "HTTP_INCLUDED_OBJECT_PATH": object_path,
            "CONTENTS": file_contents}

            final_msg = json.dumps(final_message).encode()
            serverSocket.sendto(final_msg, clientAddress)
            print("[Server] sent a message to the client with file information")
            break
            
    # serverSocket.close()