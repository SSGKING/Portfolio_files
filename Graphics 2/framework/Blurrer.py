import math
from glconstants import *
from gl import *
from Program import Program
from FullScreenQuad import FullScreenQuad
from Framebuffer import Framebuffer
from math2801 import *

class Blurrer:
    
    fboCache = {}
    prog=None
    fsq=None
    
    def __init__(self,fbo,kernelSize):
        
        key = (fbo.w,fbo.h,fbo.texture.ifmt)
        if key not in self.fboCache:
            Blurrer.fboCache[key] = Framebuffer( fbo.w,fbo.h, GL_RGBA8 )
            
        self.fbo2 = Blurrer.fboCache[key]
        self.fbo = fbo
        
        if Blurrer.prog == None:
            Blurrer.prog = Program(vs="blurvs.txt",fs="blurfs.txt")
            Blurrer.fsq = FullScreenQuad()
        
        F=[0] * 32      #32 = max blur kernelSize
        sigma = kernelSize / 3.0
        sum = 0.0
        for i in range(0,kernelSize+1):
            Q = (i * i) / (-2.0 * sigma * sigma);
            F[i] = math.exp(Q) / (sigma * math.sqrt(2.0 * math.pi))
            if i == 0:
                sum += F[i]
            else:
                sum += 2*F[i]
        for i in range(len(F)):
            F[i] /= sum
        
        self.weights = F
        
        self.kernelSize = kernelSize
        
        #dummy init, to prevent spurious errors
        Program.setUniform("blurDeltas", vec2(0,0))
        Program.setUniform("blurRadius",0)
        Program.setUniform("blurWeights[0]",self.weights)
        #Program.setUniform("blurSlice",0)

    def blur(self,slicenum):
        fbo = self.fbo
        fbo2 = self.fbo2
        oldprog = Program.current
        Blurrer.prog.use()
        fbo2.setAsRenderTarget(True)
        glDisable(GL_STENCIL_TEST)
        glStencilMask(0)

        fbo.texture.bind(14)
        Program.setUniform("blurDeltas", vec2(1/fbo.w,0) )
        Program.setUniform("blurRadius",self.kernelSize)
        Program.setUniform("blurWeights[0]",self.weights)
        Program.setUniform("blurSlice",slicenum)
        self.fsq.draw()
        fbo.setAsRenderTarget(True,[slicenum])
        fbo2.texture.bind(14)
        Program.setUniform("blurDeltas", vec2(0,1/fbo.h) )
        Program.setUniform("blurSlice",0)
        glEnable(GL_STENCIL_TEST)
        glStencilMask(0xff)
        
        Blurrer.fsq.draw()
        fbo.unsetAsRenderTarget()
        if oldprog:
            oldprog.use()
            
