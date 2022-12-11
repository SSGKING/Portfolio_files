
import BufferManager
from Program import Program
from gl import *
from glconstants import *
from math2801 import *
from DataTexture2DArray import *

class Water:
    n=256
    vertexOffset=None
    indexStart=None
    drawprog=None
    updateprog = None

    def __init__(self):
        self.F=5.0        #force
        self.D=0.9        #density
        self.eta=0.1      #viscosity
        self.t=0.01       #time
        self.d=0.01       #distance
        self.accumulatedTime=0     #total elapsed time, sec.
        self.timeScale=30.5   #scale the elapsed time
        self.computeTau()

        if Water.vertexOffset == None:
            Water.makeGridMesh()
        if Water.drawprog == None:
            Water.drawprog = Program(
                vs="watervs.txt",
                fs="waterfs.txt")
        if Water.updateprog == None:
            Water.updateprog = Program(cs="watercs.txt")

        self.pendingRipples=[]

        #convert 0...n coords to world space
        self.worldMatrix = (
                scaling(1.7/Water.n,1.7/Water.n,1.6/Water.n) * 
                translation(-5.5,0,-7.6)
            )
            
        #convert world space to 0...n
        self.inverseWorldMatrix = (
            translation(5.5,0,7.6) *
            scaling(Water.n/1.7,Water.n/1.7,Water.n/1.6)  
        )
                
        self.waterHeight = DataTexture2DArray(
            self.n, self.n, 2, 
            GL_R32F, GL_RED, GL_FLOAT )
            
        tmp = vec4(0,0,0,1) * self.worldMatrix
        Program.setUniform("waterMin", tmp.xyz)
        tmp = vec4(self.n,0,self.n,1) * self.worldMatrix
        Program.setUniform("waterMax", tmp.xyz)
        
        #we have to create dummy data, even if we're not 
        #going to use it. Otherwise, GL tags the texture
        #as mipmap incomplete and we cannot use it.
        tmp = array.array("f",[0] * (self.n*self.n*2))
        self.waterHeight.setData(tmp,GL_RED,GL_FLOAT)
        self.waterHeight.bind(0)
        glGenerateMipmap(GL_TEXTURE_2D_ARRAY)
        self.waterHeight.unbind(0)
        self.currentSlice=0
        self.totalElapsed=0
        Program.setUniform("waterClear",0)
        Program.setUniform("waterRippleInfo",vec4(0,0,0,0))
        Program.setUniform("waterElapsed",0)
        self.computeTau()
        self.setUniforms()
    
    def addRipple(self, x,z,radius,amount):
        tmp = vec4(x,0,z,1) * self.inverseWorldMatrix
        tmp2 = vec4(radius,amount,0,0) * self.inverseWorldMatrix
        self.pendingRipples.append( (tmp.x,tmp.z,tmp2.x,tmp2.y) )
        
    def setUniforms(self):
        Program.setUniform("waterTau1",self.tau_1)
        Program.setUniform("waterTau2",self.tau_2)
        Program.setUniform("waterTau3",self.tau_3)
        Program.setUniform("waterTau4",self.tau_4)
        Program.setUniform("waterCurrentSlice",
                            self.currentSlice)

    def computeTau(self):
        self.tau_1 = (
            (2 * self.F * self.t*self.t) / 
            (self.D * self.d )
        )
        self.tau_2 = self.eta * self.d - 2
        self.tau_3 = 4 - (8 * self.F * self.t*self.t)/(self.D*self.d)
        self.tau_4 = self.eta * self.t + 2

            
    def clear(self):
        Program.setUniform("waterClear",1)
        self.currentSlice=0
        Water.updateprog.dispatch(int(self.n/64), 
                self.n, 1 )
        sync = glFenceSync(GL_SYNC_GPU_COMMANDS_COMPLETE, 0)
        glClientWaitSync(sync, GL_SYNC_FLUSH_COMMANDS_BIT, -1)
        glDeleteSync(sync)
        glMemoryBarrier(GL_ALL_BARRIER_BITS)
        Program.setUniform("waterClear",0)

        
    def update(self,elapsed):
        self.accumulatedTime += self.timeScale * elapsed
        self.totalElapsed += elapsed
        self.updateprog.use()
        self.waterHeight.bindImage(0)
        self.setUniforms()
        while self.accumulatedTime >= self.t:
            if len(self.pendingRipples) == 0:
                x,z,r,amt = (0,0,0,0)
            else:
                x,z,r,amt = self.pendingRipples.pop(0)
            Program.setUniform("waterRippleInfo", vec4(x,z,r,amt) )
            Water.updateprog.dispatch(int(self.n/64), 
                    self.n, 1 )
            sync = glFenceSync(GL_SYNC_GPU_COMMANDS_COMPLETE, 0)
            glClientWaitSync(sync, GL_SYNC_FLUSH_COMMANDS_BIT, -1)
            glDeleteSync(sync)
            glMemoryBarrier(GL_ALL_BARRIER_BITS)
            self.accumulatedTime -= self.t
            self.currentSlice ^= 1
                        
    def draw(self):
        self.setUniforms()
        oldprog = Program.current
        Water.drawprog.use()
        self.waterHeight.bind(1)
        Program.setUniform("waterElapsed",self.totalElapsed)
        Program.setUniform("worldMatrix",self.worldMatrix)
        glDrawElementsBaseVertex(GL_TRIANGLES, self.numIndices,
            GL_UNSIGNED_INT, self.indexStart, self.vertexOffset)
        if oldprog:
            oldprog.use()
            
    @staticmethod
    def makeGridMesh():
        pos=[]; norms=[]; texc=[]
        for i in range(Water.n):
            for j in range(Water.n):
                pos += [j,0,i]
                norms += [0,0,0]
                texc += [0,0]
        indices = []
        for i in range(Water.n-1):
            for j in range(Water.n-1):
                #   a +--+ b
                #     | /|
                #     |/ |
                #   c +--+ d
                a = i*Water.n + j; b = a+1
                c = a + Water.n; d = c+1
                indices += [a,c,b]
                indices += [b,c,d]                
        Water.numIndices=len(indices)
        data1 = [0,0,0]
        data2 = [0,0,0]
        Water.vertexOffset,Water.indexStart = (
            BufferManager.addIndexedData(
                positiondata=pos, texturedata=texc,
                normaldata=norms,indexdata=indices,tangentdata=data1,bumpmapdata=data2)
        )              
                
                
                
                
                
                
                
