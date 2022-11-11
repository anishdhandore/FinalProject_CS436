import socket
import threading

# CONSTANTS
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 18000
# ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('', PORT))

def clientActivity(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg = conn.recv(1024).decode('utf-8')
        if msg:
            print(f"[{addr}] {msg}")
    conn.close()

def start():
    # server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=clientActivity, args=(conn, addr))
        thread.start()

print("[LISTENING] GOAT's server started...")
start()