import threading
from Model import *
from Codes import *
from collections import deque
from torch import tensor
from Lobby import *
#from numba import jit
#@jit(nopython=True)
#sython
class Client:    
    def __init__(self, connection, adress):
        self.gameState = "START" #"LOBBY" #"GAME"
        self.connection = connection
        self.adress = adress    
        self.inputs = deque()
        self.username = "Guest"
        self.brawler = 1
        self.lobby = None #prevention from uninitalised access

    def delete_client(self):
        print(str(self.adress[0]) + ':' + str(self.adress[1]) + " disconnected forcefully\n", end="")
        self.connection.close()
        if self.gameState == "LOBBY" or self.gameState == "GAME":
            self.lobby.removePlayer(self)
        exit(0)
    
    def recv_user(self):
        lobby_name = str(self.s_recv(10), "utf-8")
        self.username = str(self.s_recv(10), "utf-8")
        self.brawler = int(self.s_recv(1)[0])
        return lobby_name

    def s_recv(self, l):
        try:
            data = self.connection.recv(l)
            if data:
                return data
            else:
                self.delete_client()
        except Exception as inst:
            print("Exception in recv:", inst)
            self.delete_client()
    def s_send(self, msg):
        self.connection.send(msg)

    def recv_more(self, l):
        data = self.s_recv(l)
        while(len(data) < l):
            data+=self.s_recv(l-len(data))
        return data

    def handler(self):
        while True:
            code = int(self.s_recv(1)[0])        
            #crate lobby
            if code == S_CREATE_LOBBY:
                lobby_name = self.recv_user()
                lobby = findLobbyByName(lobby_name)
                if lobby == None:
                    #create new lobby
                    newLobby = Lobby(lobby_name)
                    newLobby.addPlayer(self)
                    
                    #new thread   
                    cThread = threading.Thread(target = newLobby.handler)
                    cThread.setDaemon(True)
                    cThread.start()
                else:
                    self.connection.send(bytes([C_LOBBY_ALREADY_EXISTS]))#lobby already exists
                
            #join lobby
            if code == S_JOIN_LOBBBY:
                lobby_name = self.recv_user()
                lobby = findLobbyByName(lobby_name)
                if lobby == None:
                    self.connection.send(bytes([C_LOBBY_DOESNT_EXISTS]))#lobby doesn't exist
                else:
                    lobby.addPlayer(self)

            #screenshot
            if code == S_SCREENSHOT_TAKEN:
                data = self.s_recv(4)
                w = int(data[0] * 2**8) + int(data[1])
                h = int(data[2] * 2**8) + int(data[3])
                start = time.time()
                t = tensor(list(self.recv_more(w*h))).view(h, w) * 1.
                print("First length", time.time()-start)
                print(model.predict(t))

            if code == S_START_GAME:
                self.lobby.startGame()
            
            if code == S_LEAVE_LOBBY:
                self.lobby.removePlayer(self)
                self.connection.send(bytes([C_LEAVE_LOBBY]))

            if code == S_PLAYER_INPUT:
                inputData = self.s_recv(12)
                k_x = int(inputData[0]) + int(inputData[1] * 2**8)
                k_y = int(inputData[2])+ int(inputData[3] * 2**8)
                k_SHIFT = int(inputData[4])
                k_CTRL = int(inputData[5])
                k_CAPS_LOCK = int(inputData[6])
                k_w = int(inputData[7])
                k_a = int(inputData[8])
                k_s = int(inputData[9])
                k_d = int(inputData[10])
                k_jump = int(inputData[11])
                if self.gameState == "GAME":
                    self.inputs.append([k_x, k_y, k_SHIFT, k_CTRL, k_CAPS_LOCK, k_w, k_a, k_s, k_d, k_jump])            

