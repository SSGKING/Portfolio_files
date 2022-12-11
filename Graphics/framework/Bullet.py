import math2801
import Mesh
import Texture
from Program import *

class Bullet:
    mesh = None
    texture = None
    
    def __init__(self,x,y,speedx,dir):
        
        self.x = x
        self.y = y
        self.angle = 0
        self.timeLeft = 1/2
        self.speedx = speedx
        self.alpha = 1
        self.dir = dir
        self.dead = False
        
        if Bullet.texture == None:
            Bullet.texture = Texture.ImageTexture2DArray("circlet.png")
        if Bullet.mesh == None:

            Bullet.mesh = Mesh.Mesh("plane.obj")

        
    def killthis(self):
        self.dead = True
        

    def update(self,elapsed):
        #time and position update
        self.timeLeft -= elapsed
        self.x += 1*self.speedx
        


        if self.dead:
            
            self.alpha -= 0.01

    def draw(self):

        Program.setUniform("worldMatrix", math2801.scaling(0.2,0.2,1)*math2801.translation(self.x,self.y,1))
        Program.setUniform("alpha",self.alpha)
        Bullet.mesh.draw()
