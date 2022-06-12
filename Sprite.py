screenWidth = 1920
screenHeight = 1040

import random

class BigStone:
    ID = 1
    def __init__(self, lobby):
        self.lobby = lobby            
        self.x = 300
        self.y = 700
        self.w = 1200
        self.h = 100
    def update(self):
        pass
    def shipIt(self):
        return bytes([self.ID]) + bytes([0])  + bytes([self.x%(2**8)]) + bytes([self.x//(2**8)]) + bytes([self.y%(2**8)]) + bytes([self.y//(2**8)]) + bytes([self.w%(2**8)]) + bytes([self.w//(2**8)]) + bytes([self.h%(2**8)]) + bytes([self.h//(2**8)])
        

class SmallStoneA:
    ID = 2
    
    def __init__(self, lobby):
        self.lobby = lobby    
        self.x = 1100
        self.y = 500
        self.w = 300
        self.h = 50
    def update(self):
        pass
    def shipIt(self):
        return bytes([self.ID]) + bytes([0])  + bytes([self.x%(2**8)]) + bytes([self.x//(2**8)]) + bytes([self.y%(2**8)]) + bytes([self.y//(2**8)]) + bytes([self.w%(2**8)]) + bytes([self.w//(2**8)]) + bytes([self.h%(2**8)]) + bytes([self.h//(2**8)])
    
class SmallStoneB:
    ID = 2
    def __init__(self, lobby):
        self.lobby = lobby
        self.x = 400
        self.y = 500
        self.w = 300
        self.h = 50
    def update(self):
        pass
    def shipIt(self):
        return bytes([self.ID]) + bytes([0])  + bytes([self.x%(2**8)]) + bytes([self.x//(2**8)]) + bytes([self.y%(2**8)]) + bytes([self.y//(2**8)]) + bytes([self.w%(2**8)]) + bytes([self.w//(2**8)]) + bytes([self.h%(2**8)]) + bytes([self.h//(2**8)])
    
class HealthSprite:
    def __init__(self, lobby, playerNum):
        lobby.sprites.append(self)
        self.HP = 100
        self.x = 50+playerNum*250
        self.y = 100
        self.ID = 2
        self.w = 200
        self.h = 40
    def update(self):
        self.w = self.HP*2
    
    def shipIt(self):
        return bytes([self.ID]) + bytes([0])  + bytes([self.x%(2**8)]) + bytes([self.x//(2**8)]) + bytes([self.y%(2**8)]) + bytes([self.y//(2**8)]) + bytes([self.w%(2**8)]) + bytes([self.w//(2**8)]) + bytes([self.h%(2**8)]) + bytes([self.h//(2**8)])
    
class PlayerSprite:
    def __init__(self, lobby, playerNum):
        self.drop = False
        self.lobby = lobby
        self.ID = 4
        self.x = 100
        self.y = 5
        self.w = int(32*1.6)
        self.h = int(64*1.6)
        self.x_vel = 0
        self.y_vel = 0
        self.standing = False
        self.jumped = 1
        self.healthSprite = HealthSprite(lobby, playerNum)

    def update(self):
        if self.x_vel > 5:
            self.x_vel = 5
        if self.x_vel < -5:
            self.x_vel = -5
        if self.y_vel > 10:
            self.y_vel = 10
        if self.y_vel < -20:
            self.y_vel = -20

        if random.randint(0, 200) == 69:
            self.healthSprite.HP -= 5
            if self.healthSprite.HP < 0:
                self.healthSprite.HP = 0

        self.y_vel += 1
        newx = self.x + self.x_vel
        newy = self.y + self.y_vel
        self.standing = False
        for sprite in self.lobby.sprites:
            if sprite.ID == 2:
                if newx >= sprite.x and newx <= sprite.x + sprite.w:
                    if self.y+self.h <= sprite.y and newy+self.h >= sprite.y and not self.drop:
                        newy = sprite.y-self.h
                        self.standing = True
                        self.jumped = 0
                
            elif sprite.ID == 1:
                if newx >= sprite.x and newx <= sprite.x + sprite.w:
                    if self.y+self.h <= sprite.y and newy+self.h >= sprite.y:
                        newy = sprite.y-self.h
                        self.standing = True
                        self.jumped = 0

        if newx < 0:
            newx = 0
        if newy < 0:
            newy = 0
        if newx > screenWidth:
            newx = screenWidth
        if newy > screenHeight:
            newy = screenHeight

        self.x = newx
        self.y = newy
        
        self.drop = False

    def handleInput(self, a):
        k_x, k_y, k_SHIFT, k_CTRL, k_CAPS_LOCK, k_w, k_a, k_s, k_d, k_jump = tuple(a)
        if k_a:
            self.x_vel-=1
        else:
            if self.x_vel < 0:
                self.x_vel +=1
        if k_d:
            self.x_vel+=1
        else:    
            if self.x_vel > 0:
                self.x_vel -=1    
        if k_w and self.jumped < 2:
            self.y_vel = -20
            self.jumped +=1
        if k_s:
            self.drop = True
        #if k_jump:
        #    self.y_vel = -20
        

    def shipIt(self):
        return bytes([self.ID]) + bytes([0])  + bytes([self.x%(2**8)]) + bytes([self.x//(2**8)]) + bytes([self.y%(2**8)]) + bytes([self.y//(2**8)]) + bytes([self.w%(2**8)]) + bytes([self.w//(2**8)]) + bytes([self.h%(2**8)]) + bytes([self.h//(2**8)])
    


