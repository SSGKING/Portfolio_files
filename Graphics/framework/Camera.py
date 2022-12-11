from math2801 import *
from Program import *
class Camera:
    #coi is center of interest
    def __init__(self,coi,eye):
        self.h = 0.001
        self.y = 1000

        dh = 1
        dv = 1

        self.projMatrix = mat4(dh,0,0,0,
                            0,dv,0,0,
                            0,0, (((2*self.y)/(self.h-self.y))+1),-1,
                            0,0,((2*self.h*self.y)/(self.h-self.y)),0)

        self.lookAt( coi, eye,vec3(0,1,0)  )


    def lookAt(self,eye, coi, up ):
        self.eye = vec4(eye.x, eye.y, eye.z,1)
        self.coi = vec4(coi.x, coi.y, coi.z,1)
        self.look = normalize(self.coi-self.eye)
        self.right = normalize(cross(self.look,vec4(up.x,up.y,up.z,0) ))
        self.up = cross(self.right,self.look)
        self.updateViewMatrix()
        
    def updateViewMatrix(self):
        cr = -dot(self.eye,self.right)
        cu = -dot(self.eye,self.up)
        cl = dot(self.eye,self.look)
        self.viewMatrix = mat4(
            self.right.x, self.up.x, -self.look.x, 0,
            self.right.y, self.up.y, -self.look.y, 0,
            self.right.z, self.up.z, -self.look.z, 0,
            cr,           cu,        cl, 1 )
        self.setUniforms()
    def setUniforms(self):
        Program.setUniform("viewMatrix",self.viewMatrix)
        Program.setUniform("eyePos",vec3(self.eye.x,self.eye.y,self.eye.z))
        Program.setUniform("projMatrix",self.projMatrix)
        #Program.setUniform("projMatrix",mat4.identity())
    def pan(self,dx,dy):
        self.coi.x += dx
        self.coi.y += dy
        self.updateViewMatrix()
    def tilt(self,amt):
        M = axisRotation( vec3(0,0,1), amt )
        self.right = self.right * M
        self.up = self.up * M
        self.updateViewMatrix()
    def strafe(self,deltaRight, deltaUp, deltaLook):
        self.eye += deltaRight * self.right
        self.eye += deltaUp * self.up
        self.eye += deltaLook * self.look
        self.updateViewMatrix()

    def yaw(self,amt):
        #turns left/right
        M = axisRotation( self.up, amt )
        self.look = self.look * M
        self.right = self.right * M
        self.updateViewMatrix()
    def roll(self, amt):
        #do a barrel roll!
        M = axisRotation( self.look, amt )
        self.right = self.right * M
        self.up = self.up * M
        self.updateViewMatrix()
    def pitch(self,amt):
        #looks up/down
        M = axisRotation( self.right, amt )
        self.look = self.look * M
        self.up = self.up * M
        self.updateViewMatrix()
