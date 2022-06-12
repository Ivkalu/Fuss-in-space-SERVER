import time
from Codes import *
from Sprite import *

FPS = 60
frameDelay = 1/FPS

class Lobby:
    def __init__(self, name):
        self.name = name
        self.sprites = []
        self.clients = []
        self.gameStarted = False
        global lobbies
        lobbies.append(self)

    def startGame(self):
        print("[LOBBY] Lobby " + self.name + " started!")
        self.sprites = [BigStone(self), SmallStoneA(self), SmallStoneB(self)]
        
        for i in range(len(self.clients)):
            client = self.clients[i]
            client.playerSprite = PlayerSprite(self, i)
            self.sprites.append(client.playerSprite)
            client.connection.send(bytes([C_GAME_STARTED]))
            client.gameState = "GAME"
            
        self.gameStarted = True

    def addPlayer(self, client):
        if len(self.clients) == 4:
            client.connection.send(bytes([C_NOT_JOIN]))
            return False
        #succesfull join
        self.clients.append(client)
        client.gameState = "LOBBY"
        client.lobby = self
        client.connection.send(bytes([C_JOINED_LOBBY]))
        return True

    def removePlayer(self, client):
        if client in self.clients:
            self.clients.remove(client)
            client.lobby = None

    def sendBuffer(self):
        if not self.gameStarted:
            return bytes([C_LOBBY_DATA]) + b''.join([bytes(client.username, 'utf-8') for client in self.clients]+[bytes(10) for i in range(4-len(self.clients))])
        else:
            return bytes([C_GAME_DATA]) + bytes([len(self.sprites)]) +b''.join([sprite.shipIt() for sprite in self.sprites])
            
    def handler(self):
        #this runs while in LOBBY state and in GAME state
        while(len(self.clients)):
            #framerate
            frameStart = time.time()
            
            #handle events
            for client in self.clients:
                if len(client.inputs):
                    client.playerSprite.handleInput(client.inputs.popleft())

            #update the game
            if self.gameStarted:
                for sprite in self.sprites:
                    sprite.update()
            
            #sending informations to players
            buff = self.sendBuffer()
            for client in self.clients:
                client.connection.send(buff)                

            #framerate limiter
            frameLength = time.time()-frameStart
            if(frameLength < frameDelay):
                time.sleep(frameDelay - frameLength)    

        #lobby is empty, delete lobby from list of lobbies
        global lobbies
        lobbies.remove(self)

lobbies = []

def findLobbyByName(lobby_name):
    for lobby in lobbies:
        if lobby.name == lobby_name:
            return lobby
    return None