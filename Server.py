import socket
import threading
from Lobby import *
from Player import *

ADDR = ("0.0.0.0", 27015) #server, port

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def __init__(self):
        self.sock.bind(ADDR)
        self.sock.listen(1)        
        print(f"[SERVER] Server is starting at adress {get_ip(), ADDR[1]}")

    def run(self):
        while True:
            connection, adress = self.sock.accept()
            client = Client(connection, adress)
            print(str(adress[0]) + ':' + str(adress[1]) + " connected\n", end="")
            
            cThread = threading.Thread(target=client.handler)
            cThread.setDaemon(True)
            cThread.start()


server = Server()
server.run()
