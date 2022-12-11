import etgg2801
from time import process_time
import Globals as globs
import random
import Mesh
from gl import *
from glconstants import *
from Program import *
import math2801
import Texture

class BouncingSquare:
    mesh = None
    texture = None
    

    def __init__(self,win_w,win_h):
        self.x = random.random()
        self.y = random.random()
        
        self.xdir = random.randint(-1, 1)
        while self.xdir == 0:
            self.xdir = random.randint(-1, 1)
        
        self.xspeed = 0.01 * self.xdir
        
        self.ydir = random.randint(-1, 1)
        while self.ydir == 0:
            self.ydir = random.randint(-1, 1)
        self.yspeed = 0.01 * self.ydir
        self.win_w = 1
        self.win_h = 1
        self.width = 0
        self.hight = 0
        self.xScale = 1
        self.yScale = 1
        self.alpha = 1
        self.dead = False
        self.angle = 0
        if BouncingSquare.texture == None:
            BouncingSquare.texture = Texture.ImageTexture2DArray("biohazard.ora")
        if BouncingSquare.mesh == None:

            BouncingSquare.mesh = Mesh.Mesh("virus.obj")
        self.numFrames = 30
        frames_per_second = 15      
        self.secPerFrame = 1/10
        self.timeLeft = self.secPerFrame    
        self.frameNum = 0   

    def killthis(self):
        self.dead = True
    
    def update(self,elapsed):
        self.timeLeft -= elapsed
        while self.timeLeft <= 0 :
            self.timeLeft += self.secPerFrame
            self.frameNum += 1
            
            if self.frameNum >= self.numFrames:
                self.frameNum = 0
        self.x += (self.xspeed*self.xdir)
        
        self.y += (self.yspeed * self.ydir)

        self.angle += 0.01
        if self.angle >= 360:
            self.angle = 0


        if self.x <= -1:
            self.xdir *= -1
        if self.y <= -1:
            self.ydir *= -1
        if self.x + self.width >= self.win_w:
            self.xdir *= -1
        if self.y + self.hight >= self.win_h:
            self.ydir *= -1

        if self.dead:
            self.alpha -= 0.01
        
        self.xScale -= 0.00005
        self.yScale -= 0.00005
        
        if self.xScale <= 0 or self.yScale <= 0:
            self.timeLeft = 0
        

        
        

    def draw(self):
        #Draws the square at current position
        Program.setUniform("frame",self.frameNum)
        Program.setUniform("worldMatrix", math2801.scaling(self.xScale,self.yScale,1)*((math2801.axisRotation(math2801.vec3(0,0,1),self.angle))*math2801.translation(self.x,self.y,1)))
        Program.setUniform("alpha",self.alpha)
        BouncingSquare.mesh.draw()
    


        
