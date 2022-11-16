from socket import *
import time
import json
import os
import shutil

serverName = 'localhost'
serverPort = 18000
clientSocket = socket(AF_INET, SOCK_DGRAM)

def send_message(clientSocket, msg):
    if type(msg) == dict:
        msg = json.dumps(msg).encode('utf-8')
        clientSocket.sendto(msg,(serverName, serverPort))

    else:
        clientSocket.sendto(str(msg).encode('base64','strict'),(serverName, serverPort))

#Show initial menu option
def start():
    print("Choose one of the options from the menu:")
    print("1. Get a file from the server")
    print("2. Quit")

    message = input("Enter your selection: ")

    b = b''
    c = b''
    e = b''
    
    #Select HTTP Version to use
    if message == "1":
        filename = input("Enter the location of your file: ")
        print("1. Use HTTP version 1.0 (non-persistent)")
        print("2. Use HTTP version 1.1 (persistent)")

        http_ver = input("Enter your selection: ").lower()

        if http_ver == 1:
            http_ver = 1.0
        else:
            http_ver = 1.1
        
        #Initiate TCP Connection with Server
        tcp_syn_msg = {"PAYLOAD LENGTH": 0, 
        "TCP_SYN_FLAG": 1, 
        "TCP_ACK_FLAG": 0,
        "TCP_FIN_FLAG": 0,
        "HTTP_GET_REQUEST": 0,
        "HTTP_RESPONSE_STATUS_CODE": 0,
        "HTTP_CLIENT_VERSION": http_ver,
        "HTTP_REQUEST_PATH": 0,
        "HTTP_INCLUDED_OBJECT_PATH": 0}

        send_message(clientSocket, tcp_syn_msg)

        print("[Client] Sent a TCP SYN message to the server!!!")

        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

        b += modifiedMessage
        d = json.loads(b.decode('utf-8'))

        # respond with a TCP ACK message here, now the client and server are in a TCP connection
        tcp_ack_msg = {"PAYLOAD LENGTH": 0, 
        "TCP_SYN_FLAG": 0, 
        "TCP_ACK_FLAG": 1,
        "TCP_FIN_FLAG": 0,
        "HTTP_GET_REQUEST": 0,
        "HTTP_RESPONSE_STATUS_CODE": 0,
        "HTTP_CLIENT_VERSION": http_ver,
        "HTTP_REQUEST_PATH": 0,
        "HTTP_INCLUDED_OBJECT_PATH": 0}

        send_message(clientSocket, tcp_ack_msg) 
        print("[Client] Sent a TCP ACK message to the server...")
        print("[Client] Client and Server are in a TCP connection now!!!")

        # send a http get request
        http_get = {"PAYLOAD LENGTH": 0, 
        "TCP_SYN_FLAG": 0, 
        "TCP_ACK_FLAG": 0,
        "TCP_FIN_FLAG": 0,
        "HTTP_GET_REQUEST": 1,
        "HTTP_RESPONSE_STATUS_CODE": 0,
        "HTTP_CLIENT_VERSION": http_ver,
        "HTTP_REQUEST_PATH": filename,
        "HTTP_INCLUDED_OBJECT_PATH": 0}

        send_message(clientSocket, http_get) 

        # get the http response message now 
        statusMessage, serverAddress = clientSocket.recvfrom(2048)
        c += statusMessage
        d = json.loads(c.decode('utf-8'))
        
        # if status code is 404, display page not found
        if d["HTTP_RESPONSE_STATUS_CODE"] == 404:
            print("[Client] Error 404...the page you are looking for is not found!!!")

            # send a TCP FIN message to the server to close the connection 
            tcp_fin_msg = {"PAYLOAD LENGTH": 0, 
            "TCP_SYN_FLAG": 0, 
            "TCP_ACK_FLAG": 0,
            "TCP_FIN_FLAG": 1,
            "HTTP_GET_REQUEST": 1,
            "HTTP_RESPONSE_STATUS_CODE": 404,
            "HTTP_CLIENT_VERSION": http_ver,
            "HTTP_REQUEST_PATH": filename,
            "HTTP_INCLUDED_OBJECT_PATH": 0}
        
            send_message(clientSocket, tcp_fin_msg)
            print("[Client] Sent a TCP FIN message to the server...")

            # receive a TCP FIN ACK message from the server 
            tcpfinackMessage, serverAddress = clientSocket.recvfrom(2048)

            # send a TCP ACK message again, and display menu again
            tcp_ack_msg = {"PAYLOAD LENGTH": 0, 
            "TCP_SYN_FLAG": 0, 
            "TCP_ACK_FLAG": 1,
            "TCP_FIN_FLAG": 0,
            "HTTP_GET_REQUEST": 0,
            "HTTP_RESPONSE_STATUS_CODE": 404,
            "HTTP_CLIENT_VERSION": http_ver,
            "HTTP_REQUEST_PATH": filename,
            "HTTP_INCLUDED_OBJECT_PATH": 0}
            send_message(clientSocket, tcp_ack_msg)
            print("[Client] Closing the TCP connection!!!")
            # show the first menu now
            return False

        # if status code is 200, display page is found
        else:
            print("[Client] Success 200 OK...the page you are looking for is found!!!")

            print("[Client] Contents of your file are as follows:")
            print(d["CONTENTS"])
            
            #file contains a link to another object so, open path to other object
            if d["HTTP_INCLUDED_OBJECT_PATH"] != "":
                file = open(d["HTTP_INCLUDED_OBJECT_PATH"], mode='r')
                file_contents = file.read()
                file.close()

                print("[Client] Contents of attached file:")
                print(file_contents)

            # storing the file in client machine 
            original = os.getcwd() + "/" + d["HTTP_REQUEST_PATH"]
            print(original)
            target = "/Users/anishdhandore/Documents/CSUSM/Courses /7 Fall 2022/CS 436/FinalProject_Networking/Client"
            shutil.copy(original, target)

            return True
    else:
        return True

if __name__ == '__main__':
    while True:
<<<<<<< HEAD
        if not start():
            break



    

    
=======
        start()
>>>>>>> 75fa59e1cd5113d76843dbf9640f04562f744e46
