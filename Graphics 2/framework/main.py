#this one *must* be first
from ast import Pass
from Blurrer import Blurrer
import etgg2801

import pysdl2.sdl2 as sdl2
import pysdl2.sdl2.keycode as keycode
from gl import *
from glconstants import *
import time
from Globals import GlobalVars
import ctypes
import BufferManager
import math
from Program import Program
from Sampler import ClampSampler, MipSampler,NearestSampler
from ImageTexture2DArray import ImageTexture2DArray
from math2801 import *
from Camera import Camera
from FullScreenQuad import FullScreenQuad
from GLTFMesh import GLTFMesh
import Text
import Lights
from Framebuffer import *
from Blurrer import *
from ImageTextureCube import *
from Water import *
import random

WIDTH = 512
HEIGHT = 512
def main():
    win = etgg2801.createWindow(width=512, height=512)
    print( glGetString(GL_RENDERER), glGetString(GL_VENDOR), glGetString(GL_VERSION), glGetString(GL_SHADING_LANGUAGE_VERSION))  
    globs = GlobalVars()
    setup(globs)
    last = time.time_ns()/1000000000
    DESIRED_FRAMES_PER_SEC = 60
    DESIRED_SEC_PER_FRAME = 1/DESIRED_FRAMES_PER_SEC
    QUANTUM = 0.005
    accumulated=0
    while True:
        now = time.time_ns()/1000000000
        elapsed = now-last
        last=now
        accumulated += elapsed
        while accumulated >= QUANTUM:
            update(QUANTUM,globs)
            accumulated -= QUANTUM
        draw(globs)
        sdl2.SDL_GL_SwapWindow(win)
        end = time.time_ns()/1000000000
        frameTime=end-now
        leftover = DESIRED_SEC_PER_FRAME - frameTime
        if leftover > 0:
            time.sleep(leftover)
        
        
def setup(globs):
    glEnable(GL_STENCIL_TEST)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    
    globs.keys=set()
    globs.mouseLook=True
    sdl2.SDL_SetRelativeMouseMode(1)
    
    globs.prog = Program(vs="vs.txt",
                    fs="fs.txt")  
    
    globs.camera = Camera(vec3(0,1,2), vec3(0,1,0), vec3(0,1,0) )
    
    globs.water = Water()
    
    globs.meshes=[]
    
    globs.envMap = ImageTextureCube(
    "px.jpg", "nx.jpg",
    "py.jpg", "ny.jpg",
    "pz.jpg", "nz.jpg"
    )

    globs.skyboxTexture = ImageTextureCube(
    "space.jpg", "space1.jpg",
    "space2.jpg", "space3.jpg",
    "space4.jpg", "space5.jpg"
    )

    

    
    fname = os.path.join(
        os.path.dirname(__file__),
        "bigassets",
        "kitchen.gltf")
    

    globs.meshes.append(GLTFMesh(fname))
    for m in globs.meshes:
        globs.nonTransItems = m.getItemsNotMatchingName("bookshelfglass")
        globs.transItems = m.getItemsMatchingName("bookshelfglass")
    
    
    globs.cubemesh = GLTFMesh("assets/cube.gltf")
    
    lightdata = Lights.parseLights(fname)
    
    lightPositionsAndDirectionalFlag=[None]*len(lightdata)
    spotDirectionsAndCosineSpotEdgeStarts=[None]*len(lightdata)
    lightColorsAndCosineSpotAngleCutoffs=[None]*len(lightdata)

    
    for i in range(len(lightdata)):
        lightPositionsAndDirectionalFlag[i] = vec4( lightdata[i].position,1.0 )
        spotDirectionsAndCosineSpotEdgeStarts[i] = vec4(0,-1,0, math.cos(math.radians(lightdata[i].spotCutoffStart) ) )
        lightColorsAndCosineSpotAngleCutoffs[i] = vec4( lightdata[i].energy* vec3(*lightdata[i].color), math.cos(math.radians(lightdata[i].spotCutoffEnd) ) ) 
    
    Program.setUniform( "lightPositionsAndDirectionalFlag[0]", lightPositionsAndDirectionalFlag )
    Program.setUniform( "spotDirectionsAndCosineSpotEdgeStarts[0]", spotDirectionsAndCosineSpotEdgeStarts)
    Program.setUniform( "lightColorsAndCosineSpotAngleCutoffs[0]", lightColorsAndCosineSpotAngleCutoffs)
    Program.setUniform( "attenuation", vec3(450,0,3.5) )
    Program.setUniform("blurSlice",0)

    globs.fbo = Framebuffer(512,512,[(GL_RGBA8,2)])
    
    globs.fsq = FullScreenQuad()
    globs.fboprog = Program(vs="fbovs.txt",fs="fbofs.txt")
   
    globs.glowprog = Program(vs ="glowvs.txt",fs = "glowfs.txt")

    globs.skyboxprog = Program(vs = "skyboxvs.txt",fs = "skyboxfs.txt")

    mipSampler = MipSampler()
    mipSampler.bind(0)          #color texture
    mipSampler.bind(1)          #emission texture
    mipSampler.bind(2)
    mipSampler.bind(3)          #MR texture

    clampSamp = ClampSampler()
    clampSamp.bind(14)

    glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS)
    mipSampler.bind(7)

    globs.blurrer = Blurrer(globs.fbo,11)
    
    globs.fbo1 = Framebuffer(512,512,GL_RGBA8,withStencilBuffer=False)
    globs.fbo2 = Framebuffer(512,512,GL_RGBA8)
    globs.blurrer1 = Blurrer(globs.fbo2,21)

    nearestSampler = NearestSampler()
    nearestSampler.bind(15)     #for text
    
    glClearColor(0,0,0,1)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    globs.timeToNextRipple=0
    globs.R = random.Random(321)
    Text.initialize()
    updateText(globs)
    BufferManager.pushToGPU()


def updateText(globs):
    if globs.mouseLook:
        state="off"
    else:
        state="on "
        
    Text.print(0,f"Tab=Mouselook {state}")
    Text.print(1, "WASD=walk/strafe  QE=turn RF=up/down")


def update(elapsed,globs):
    #if not globs.paused:
    globs.water.update(elapsed)
    globs.timeToNextRipple -= elapsed
    if globs.timeToNextRipple < 0:
        globs.timeToNextRipple = 1.0
        #x=globs.R.uniform(-5.6,5.6)
        x = -4.65
    
        #z=globs.R.uniform(-7.6,7.6)
        z = -7.1
        r=globs.R.uniform(0.001,0.05)
        a=globs.R.uniform(-0.025,-0.05)
        globs.water.addRipple(x,z,r,a)
    
    pumpEvents(globs)

    if keycode.SDLK_w in globs.keys:
        globs.camera.strafeNoUpOrDown(0,0,2.0*elapsed)
    if keycode.SDLK_s in globs.keys:
        globs.camera.strafeNoUpOrDown(0,0,-2.0*elapsed)
    if keycode.SDLK_a in globs.keys:
        globs.camera.strafeNoUpOrDown(-2.0*elapsed,0,0)
    if keycode.SDLK_d in globs.keys:
        globs.camera.strafeNoUpOrDown(2.0*elapsed,0,0)
    if keycode.SDLK_q in globs.keys:
        globs.camera.turn(elapsed)
    if keycode.SDLK_e in globs.keys:
        globs.camera.turn(-elapsed)
    if keycode.SDLK_r in globs.keys:
        globs.camera.strafeXYZ(0,elapsed,0)
    if keycode.SDLK_f in globs.keys:
        globs.camera.strafeXYZ(0,-elapsed,0)
        


def pumpEvents(globs):
    ev = sdl2.SDL_Event()
    while True:
        eventOccurred = sdl2.SDL_PollEvent(ctypes.byref(ev))
        if not eventOccurred:
            return
        if ev.type == sdl2.SDL_QUIT:
            sdl2.SDL_Quit()
            sys.exit(0)
        if ev.type == sdl2.SDL_KEYDOWN:
            if ev.key.keysym.sym == keycode.SDLK_F1:
                etgg2801.screenshot("screenshot.png")
                print("Wrote screenshot.png")
            elif ev.key.keysym.sym == keycode.SDLK_TAB:
                globs.mouseLook = not globs.mouseLook
                if globs.mouseLook:
                    sdl2.SDL_SetRelativeMouseMode(1)
                else:
                    sdl2.SDL_SetRelativeMouseMode(0)
                updateText(globs)
            elif ev.key.keysym.sym == keycode.SDLK_ESCAPE:
                sdl2.SDL_Quit()
                sys.exit(0)
            globs.keys.add( ev.key.keysym.sym )
        if ev.type == sdl2.SDL_KEYUP:
            globs.keys.discard( ev.key.keysym.sym )
        if ev.type == sdl2.SDL_MOUSEMOTION:
            if globs.mouseLook:
                globs.camera.turnAroundAxis(vec3(0,1,0),  -0.01*ev.motion.xrel,  )
                globs.camera.pitch( -0.01*ev.motion.yrel)


def drawTranslucentThings(globs):
    for m in globs.meshes:
        m.draw(toDraw=globs.transItems)
        
def drawOpaqueThings(globs):
    for m in globs.meshes:
        m.draw(toDraw=globs.nonTransItems)

def drawEverything(globs):
    for m in globs.meshes:
        m.draw()
def draw_water(globs):
    pass


def draw_trans(globs):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

    glStencilFunc(GL_ALWAYS,0,0xff)
    glStencilOp(GL_KEEP,GL_KEEP,GL_KEEP)

    globs.fbo1.depthtexture.unbind(15)
    globs.fbo1.setAsRenderTarget(True)
    drawTranslucentThings(globs)
    #globs.fbo1.dump("fbo1contents")
    globs.fbo1.unsetAsRenderTarget()
    globs.fbo1.depthtexture.bind(15)
    
    
    globs.fbo2.setAsRenderTarget(True)
    glColorMask(0,0,0,0)
    glDepthMask(0)
    
    glStencilFunc(GL_ALWAYS,1,0xff)
    glStencilOp(GL_KEEP,GL_KEEP,GL_REPLACE)

    drawTranslucentThings(globs)
    glColorMask(1,1,1,1)
    glDepthMask(1)

    glStencilFunc(GL_EQUAL,1,0xff)
    glStencilOp(GL_KEEP,GL_KEEP,GL_KEEP)
    
    
    Program.setUniform("testDepth",1.0)
    drawOpaqueThings(globs)
    Program.setUniform("testDepth",0.0)
    
    #globs.fbo2.dump("fbo2contents")
    globs.fbo2.unsetAsRenderTarget()
    Program.setUniform("testDepth",0.0)
    glStencilFunc(GL_ALWAYS,0,0xff)
    glStencilOp(GL_KEEP,GL_KEEP,GL_KEEP)
    globs.blurrer1.blur(0)

    glStencilFunc(GL_ALWAYS,1,0xff)
    glStencilOp(GL_KEEP,GL_KEEP,GL_REPLACE)
    glColorMask(0,0,0,0)
    drawTranslucentThings(globs)
    glColorMask(1,1,1,1)

    glStencilFunc(GL_ALWAYS,0,0xff)
    glStencilOp(GL_KEEP,GL_KEEP,GL_REPLACE)
    drawOpaqueThings(globs)

    glStencilFunc(GL_EQUAL,1,0xff)
    glStencilOp(GL_KEEP,GL_KEEP,GL_KEEP)
    glDisable(GL_DEPTH_TEST)
    globs.fboprog.use()
    globs.fbo2.texture.bind(0)
    globs.fsq.draw()

    glEnable(GL_DEPTH_TEST)
    globs.prog.use()
    drawTranslucentThings(globs)


def draw(globs):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
    globs.envMap.bind(7)
    #globs.fbo.setAsRenderTarget(True)
    
    BufferManager.bind()
    globs.prog.use()
    globs.camera.setUniforms()
    Program.setUniform("alphaFactor",1.0)
    Program.setUniform("animationFrame",1.0)
    Program.setUniform("worldMatrix",mat4.identity())
    Program.setUniform("testDepth",0.0)
    Program.setUniform("waterScreenSize",vec2(WIDTH,HEIGHT))
    
    #draw_trans(globs)
    globs.fbo.setAsRenderTarget(True)
    drawEverything(globs)
    globs.fbo.unsetAsRenderTarget()
    drawEverything(globs)
    #drawEverything(globs)
    globs.fbo.texture.bind(0)
    globs.water.draw()


    #glDisable(GL_CULL_FACE)
    #globs.skyboxprog.use()
    #globs.skyboxTexture.bind(7)
    
    #globs.cubemesh.draw()
    

    #globs.fbo.unsetAsRenderTarget()

    #globs.blurrer.blur(1)           #changed!
    #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    #globs.glowprog.use()            #changed!
    #globs.fbo.texture.bind(0)
    #globs.fsq.draw()
    Text.draw()

    #Draw the skybox

 

  
main()
