from Bullet import Bullet
import etgg2801
import math2801
from Program import * 
import Globals
import pysdl2.sdl2 as sdl2
import pysdl2.sdl2.keycode as keycode
from gl import *
from glconstants import *
import ctypes
import time
import BouncingSquares 
from ChargeState import ChargeStateMachine, ChargeStater
import bufferManager as BufferManager
import hexagon
import Mesh
from Sampler import *
import Text
import Camera
import math


def main() -> None:
    win = etgg2801.createWindow()
    globs = Globals.GlobalVariables()
    globs.stateMachine = ChargeStateMachine()
    setup(globs)
    #print( glGetString(GL_RENDERER), glGetString(GL_VENDOR), glGetString(GL_VERSION), glGetString(GL_SHADING_LANGUAGE_VERSION))

    samp = MipSampler()
    samp.bind(0)

    nsamp = NearestSampler()
    nsamp.bind(15)



    DESIRED_FRAMES_PER_SEC = 60
    DESIRED_SEC_PER_FRAME = 1/DESIRED_FRAMES_PER_SEC
    last = time.time_ns() / 1000000000
    QUANTUM = 0.005
    accumulated = 0
    while True:
        now = time.time_ns() / 1000000000
        elapsed = now-last
        last = now
        accumulated += elapsed
        while accumulated >= QUANTUM:
            update(QUANTUM,globs)
            accumulated -= QUANTUM
        draw(globs)
        sdl2.SDL_GL_SwapWindow(win)
        end = time.time_ns() / 1000000000
        frameTime = end-now
        leftover = DESIRED_SEC_PER_FRAME - frameTime
        if leftover > 0:
            time.sleep(leftover)


        
    
def setup(globs):
    mipSampler = MipSampler()
    mipSampler.bind(0)
    mipSampler.bind(1)
    globs.stateMachine = ChargeStateMachine()
    samp = NearestSampler()
    samp.bind(0)
    
    globs.prog = Program(vs="vs.txt",fs="fs.txt")
    
    Program.setUniform("viewMatrix", math2801.mat4.identity())
    Program.setUniform("cosineSpotAngleCutoff",math.cos(60))
    Program.setUniform("cosineSpotEdgeStart",math.cos(45))
    Program.setUniform("attenuation",math2801.vec3(0,0,0.10))
    Program.setUniform("spotDirection",math2801.vec3(0,-1,0))
    Program.setUniform("projMatrix", math2801.mat4.identity())

    #SETTING UP LIGHTS
    tmp = [math2801.vec4(-2.3135,1.4679,-7.0324,1.0),math2801.vec4(-6.9185,1.4679,-7.0324,1.0),math2801.vec4(-9.5572,1.4679, -7.0324,1.0),
    math2801.vec4(  -9.3824   , 1.4679    , -4.6223,1.0),math2801.vec4(  -9.3824   , 2.1061    , -2.0401,1.0),math2801.vec4(  4.5921    , 2.2343    , -2.1713,1.0),
    math2801.vec4(  4.5921    , 2.2343    , -0.2322,1.0),math2801.vec4(  -1.2879   , 3.6474    , -5.0965,1.0),math2801.vec4(  -6.7676   , 3.6474    , 1.3062,1.0),
    math2801.vec4(-1.2879   , 3.6474    , 3.8710,1.0),math2801.vec4(  -4.6568   , 3.6474    , -6.8181,1.0),math2801.vec4(  -1.2879   , 3.6474    , 1.2312,1.0),
    math2801.vec4(  -6.7676   , 3.6474    , -5.0965,1.0),math2801.vec4(  -3.9931   , 3.6474    , -1.9893,1.0),math2801.vec4(  27.5629   , 6.3964    , 2.8408,1.0),
    math2801.vec4(  12.1400   , 2.0948    , -1.2897,1.0),math2801.vec4(  12.6444   , 2.0948    , -0.7935,1.0),math2801.vec4(  13.1510   , 2.0948    , -1.2897,1.0),
    math2801.vec4(  12.6444   , 2.0948    , -1.7916,1.0),math2801.vec4(  -6.9202   , 0.5760    , -7.0359,1.0),math2801.vec4(  -2.2903   , 0.5760    , -7.0359,1.0),
    math2801.vec4(  -9.3903   , 1.4543    , -2.0183,1.0),math2801.vec4(  -9.5539   , 0.5760    , -7.0359,1.0),math2801.vec4(  -9.3903   , 0.5760    , -4.6102,1.0)]
    Program.setUniform("lightPositionsAndDirectionalFlag[0]",tmp)

    tmp2 = [math2801.vec4(0,-1,0,math.cos(math.radians(21.3429))),math2801.vec4(0,-1,0,math.cos(math.radians(21.3429))),math2801.vec4(0,-1,0,math.cos(math.radians(21.3429))),math2801.vec4(0,-1,0,math.cos(math.radians(21.3429))),math2801.vec4(0,-1,0,math.cos(math.radians(21.3429))),
    math2801.vec4(0,-1,0,math.cos(math.radians(13.5000))),math2801.vec4(0,-1,0,math.cos(math.radians(13.5000))),math2801.vec4(0,-1,0, math.cos(math.radians(22.5000))),math2801.vec4(0,-1,0, math.cos(math.radians(22.5000))),math2801.vec4(0,-1,0, math.cos(math.radians(22.5000))),math2801.vec4(0,-1,0, math.cos(math.radians(22.5000))),
    math2801.vec4(0,-1,0, math.cos(math.radians(22.5000))),math2801.vec4(0,-1,0, math.cos(math.radians(22.5000))),math2801.vec4(0,-1,0, math.cos(math.radians(22.5000))),math2801.vec4(0,-1,0,math.cos(math.radians(6.5029))),math2801.vec4(0,-1,0,math.cos(math.radians(180.0000))),math2801.vec4(0,-1,0,math.cos(math.radians(180.0000))),
    math2801.vec4(0,-1,0,math.cos(math.radians(180.0000))),math2801.vec4(0,-1,0,math.cos(math.radians(180.0000))),math2801.vec4(0,-1,0,math.cos(math.radians(180.0000))),math2801.vec4(0,-1,0,math.cos(math.radians(180.0000))),math2801.vec4(0,-1,0,math.cos(math.radians(180.0000))),
    math2801.vec4(0,-1,0,math.cos(math.radians(180.0000))),math2801.vec4(0,-1,0,math.cos(math.radians(180.0000)))]
    Program.setUniform("spotDirectionsAndCosineSpotEdgeStarts[0]",tmp2)
    
    tmp3 = [math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),
    math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),
    math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),
    math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(45.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(180.0000))),
    math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(180.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(180.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(180.0000))),math2801.vec4(0.5,0.5,0.5,math.cos(math.radians(180.0000))),
    math2801.vec4(0.1,0.1,0.1,math.cos(math.radians(180.0000))),math2801.vec4(0.1,0.1,0.1,math.cos(math.radians(180.0000))),math2801.vec4(0.1,0.1,0.1,math.cos(math.radians(180.0000))),math2801.vec4(0.1,0.1,0.1,math.cos(math.radians(180.0000)))]
    Program.setUniform("lightColorsAndcosineSpotAngleCutoffs[0]",tmp3)



    #globs.hex_shape = hexagon.Hexagon()
    globs.biolist = []
    globs.bulletlist = []
    #globs.bulletlist.append((Bullet(0,0,(10*globs.stateMachine.chargeTime),1)))
    #del globs.bulletlist[0]

    globs.Camera = Camera.Camera(math2801.vec3(1,1,1),math2801.vec3(0,1,1))



    
    globs.kitchenMeshes = []
    asset_path = os.path.join(os.path.dirname(__file__),"bigassets")

    filelist = os.listdir(asset_path)

    for f in filelist:
        if f.endswith(".obj"):
            print("Now loading",f)
            globs.kitchenMeshes.append(Mesh.Mesh(f))



    globs.numFrames = 15
    frames_per_second = 15      
    globs.secPerFrame = 1/frames_per_second
    globs.timeLeft = globs.secPerFrame    
    globs.frameNum=0    
    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA,GL_ONE)
    
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    BufferManager.pushToGPU()
def checkLife(globs):
    i=0
    while i < len(globs.bulletlist):
        if globs.bulletlist[i].timeLeft <= 0:
            
            globs.bulletlist[i].dead = True
            
        i += 1
    while i < len(globs.biolist):
        if globs.biolist[i].timeLeft <= 0:
            
            globs.biolist[i].dead = True
        i += 1
def kill(list):
    i=0
    while i < len(list):
        if list[i].alpha <= 0:
            del list[i]
        else:
            i += 1
def update(elapsed,globs):

    
    keysBefore = set(globs.keys)
    pumpEvents(globs)
    #globs.Camera.lookAt(math2801.vec2(globs.playerX,globs.playerY),math2801.vec2(0,1))
    globs.Camera.setUniforms()
    #for i in globs.bulletlist:
    #    i.update(elapsed)
        
    
    charge = globs.stateMachine.update(keysBefore,globs.keys,elapsed)
    change = 1
    globs.timeLeft -= elapsed
    while globs.timeLeft <= 0 :
        globs.timeLeft += globs.secPerFrame
        globs.frameNum += 1 
        
        if globs.frameNum >= 32:
            globs.frameNum = 0
    #
    #for b in globs.biolist:
    #    b.update(elapsed)
    #    for i in globs.bulletlist:
    #        if i.x > b.x and i.x < b.x + 0.4 and i.dead is False:
    #            if i.y > b.y and i.y < b.y + 0.2 and i.dead is False:
    #                print(kill)
   #                i.timeLeft = 0
    #                b.timeLeft = 0
    checkLife(globs)
    #kill(globs.biolist)
    #kill(globs.bulletlist)
    

    if charge is not None:
        
        globs.bulletlist.append(Bullet(globs.playerY,globs.playerX+0.2,((1/50)*charge),1))
    if keycode.SDLK_d in globs.keys:
        #....do something
        #globs.playerY += 0.01
        #globs.Camera.pan(0.01,0)
        globs.Camera.strafe(0.1,0,0)

        
    if keycode.SDLK_w in globs.keys:
        #....do something
        #globs.playerX += 0.01
        #globs.Camera.pan(0,0.01)
        globs.Camera.strafe(0,0,0.1)
        
        
    if keycode.SDLK_a in globs.keys:
        #....do something
        #globs.playerY -= 0.01
        #globs.Camera.pan(-0.01,0)
        globs.Camera.strafe(-0.1,0,0)
        
        
    if keycode.SDLK_s in globs.keys:
        #....do something
        #globs.playerX -= 0.01
        #globs.Camera.pan(0,-0.01)
        globs.Camera.strafe(0,0,-0.1)
    if keycode.SDLK_e in globs.keys:
        globs.Camera.yaw(-0.01)
    if keycode.SDLK_q in globs.keys:
        globs.Camera.yaw(0.01)
    if keycode.SDLK_c in globs.keys:
        #Clear the text
        #Text.clear()
        pass
    pass
def pumpEvents(globs):
    ev = sdl2.SDL_Event()
    while True:
        eventOccured = sdl2.SDL_PollEvent(ctypes.byref(ev))
        if not eventOccured:
            break
        if ev.type == sdl2.SDL_QUIT:
            sdl2.SDL_Quit()
            sys.exit(0)
        if ev.type == sdl2.SDL_KEYDOWN:
            
            globs.keys.add(ev.key.keysym.sym)
            pass
        if ev.type == sdl2.SDL_KEYUP:
            globs.keys.discard(ev.key.keysym.sym)
            pass
def draw(globs):
    
    #glClear( GL_COLOR_BUFFER_BIT)
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    
    globs.prog.use()
    BufferManager.bind()
    
    Program.setUniform("tileSize",math2801.vec2(0.2,0.1))
    Program.setUniform("positional",1.0)
    
    Program.setUniform("frame",globs.frameNum)

    Program.setUniform("objcolor", math2801.vec3(1,1,1))
    Program.setUniform("worldMatrix", math2801.mat4.identity())
    
    

    Program.setUniform("alpha",1)
    #globs.backMesh.draw()
    
    #Program.setUniform("viewMatrix", math2801.mat4.identity())
    #Program.setUniform("worldMatrix", math2801.translation(globs.playerX,globs.playerY,1))
    #globs.playerMesh.draw()
    
    #Text.draw()
    
    for m in globs.kitchenMeshes:
        m.draw()

    #for b in globs.biolist:
    #    b.draw()

    #for i in globs.bulletlist:
    #    i.draw()
    
    
    
    #globs.hex_shape.draw()
    



        
main()
