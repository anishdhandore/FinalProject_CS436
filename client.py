import socket
import time

# CONSTANTS
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 18000
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect(ADDR)

def send_message(client, msg):
    message = msg.encode('utf-8')
    client.send(message)

def start():
    print("Choose one of the options from the menu:")
    print("1. Get a file from the server")
    print("2. Quit")

    choice = input("Enter your selection: ").lower()
    # if inp == "yes":
    #     name = input("Please tell us your name: ")
    #     while True:
    #         msg = input(f"[{name}] Message (q to quit) ")
    #         if msg == "q":
    #             time.sleep(1)
    #             send_message(client, "!DISCONNECTED")
    #             break
    #         send_message(client, msg)
    # else:
    #     return

    if choice == "1":
        print("1. Use HTTP version 1.0 (non-persistent)")
        print("2. Use HTTP version 1.1 (persistent)")
        http_ver = input("Enter your selection: ").lower()
    
    else:
        return

start()