
import array
from gl import *
from glconstants import *
from DataTexture2DArray import *


class FramebufferBase:
    saved_viewport = array.array("I",[0,0,0,0])
    current=None
    @staticmethod
    def unsetAsRenderTarget():
        FramebufferBase.current = None
        glBindFramebuffer(GL_FRAMEBUFFER,0);
        A = array.array("I",[GL_BACK_LEFT])
        # ~ glDrawBuffer(GL_BACK)
        glViewport(
            FramebufferBase.saved_viewport[0],FramebufferBase.saved_viewport[1],
            FramebufferBase.saved_viewport[2],FramebufferBase.saved_viewport[3]);

class Framebuffer(FramebufferBase):
    
    def __init__(self,width,height,sliceformat,*,withStencilBuffer=True):
        """ width is the FBO width;
            height is the FBO height;
            sliceformat can be a single GL format code (ex: GL_RGBA8) or a list
            of format codes (to make separate textures with one slice each) 
            or a list of (format,slicecount) tuples.
            """
            
        self.w=width
        self.h=height
        self.textures=[]
        self.texture=None
        
        slices = sliceformat
        
        if type(slices) == int:
            slices = [slices]
        
        if FramebufferBase.current:
            FramebufferBase.current.unsetAsRenderTarget()
            
        tmp = array.array("I",[0])
        glGenFramebuffers(1,tmp)
        self.fbo = tmp[0]
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo )
    
    
        #only permit formats that GL requires support for. Any combination
        #of these must be OK in an FBO according to the standard.
        #https:#www.khronos.org/opengl/wiki/Image_Format#Required_formats
        #https:#www.khronos.org/opengl/wiki/Framebuffer_Object
        #page 197 (218) of OpenGL Core profile:
        #mandatory color renderable formats
        allowedFormats = {
            GL_R8: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_R16: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RG8: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RG16: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RGBA8: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RGBA16: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RGB10_A2: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RGB10_A2UI: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_R16F: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RG16F: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RGBA16F: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_R32F: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RG32F: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RGBA32F: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_R8I: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_R16I: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_R32I: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_R8UI: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_R16UI: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_R32UI: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RG8I: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RG8UI: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RG16I: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RG16UI: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RG32I: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RG32UI: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RGBA8I: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RGBA8UI: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RGBA16I: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RGBA16UI: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RGBA32I: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_RGBA32UI: (GL_RGBA,GL_UNSIGNED_BYTE),
            GL_DEPTH24_STENCIL8: (GL_DEPTH_STENCIL, GL_UNSIGNED_INT_24_8),
            GL_DEPTH32F_STENCIL8: (GL_DEPTH_STENCIL, GL_UNSIGNED_INT_24_8)
        }
            
        attachmentCount=0
        drawbuffers=[]
        for i in range(len(slices)):
            si = slices[i]
            
            if type(si) == int:
                si = (si,1)
                
            fmt,slicecount = si
            
            if fmt not in allowedFormats:
                raise RuntimeError("Invalid texture format for FBO")
            else:
                efmt,etype = allowedFormats[fmt]
            self.textures.append( DataTexture2DArray(
                width,height,slicecount,fmt,efmt,etype))
            for j in range(slicecount):
                if attachmentCount < 8:
                    #target, attachment, texture, mip level, layer
                    glFramebufferTextureLayer(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0+attachmentCount,
                        self.textures[-1].tex, 0, j )
                    drawbuffers.append(GL_COLOR_ATTACHMENT0+attachmentCount);
                    attachmentCount+=1
          
        if len(self.textures) > 0:
            self.texture = self.textures[0]
        else:
            self.texture = None
        
        if withStencilBuffer:
            self.depthtexture = DataTexture2DArray(width,height,1,
                GL_DEPTH24_STENCIL8,GL_DEPTH_STENCIL,GL_UNSIGNED_INT_24_8)
            glFramebufferTextureLayer(GL_FRAMEBUFFER,GL_DEPTH_STENCIL_ATTACHMENT,
                self.depthtexture.tex, 0, 0 )
            self.withStencil=True
        else:
            self.depthtexture = DataTexture2DArray(width,height,1,
                GL_DEPTH_COMPONENT24,GL_DEPTH_COMPONENT,GL_UNSIGNED_INT)
            glFramebufferTextureLayer(GL_FRAMEBUFFER,GL_DEPTH_ATTACHMENT,
                self.depthtexture.tex, 0, 0 )
            self.withStencil=False
                
            
        complete = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        
        if complete != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("Framebuffer is not complete")
        
        glBindFramebuffer(GL_FRAMEBUFFER,0)
        FramebufferBase.current = 0
        self.drawbuffers = array.array("I",drawbuffers)
        
        self.allLayers=[]
        for i in range(len(self.textures)):
            t = self.textures[i]
            for s in range(t.slices):
                self.allLayers.append( (i,s) )
        
        
        
    def setAsRenderTarget(self,clear,layers=None):
        """If clear is true, clear the FBO after binding it. 
            layers is one of:
                None: Enable rendering to all framebuffer layers
                int: Render only to the given layer
                List of ints: Render to the given layers
            Note that layers are numbered starting from self.textures[0].
                Each slice of this texture is a subsequent layer number.
                Then the rest of the textures are used, with each
                slice being the next layer in turn.
        """
        if FramebufferBase.current:
            FramebufferBase.current.unsetAsRenderTarget()
        glGetIntegerv(GL_VIEWPORT,FramebufferBase.saved_viewport)
        FramebufferBase.current = self
        
        glBindFramebuffer(GL_FRAMEBUFFER,self.fbo);
        
        if layers == None:
            layers = range(len(self.allLayers))
        elif type(layers) == int:
            layers = [self.allLayers[layers]]
            
        i=0
        for li in layers:
            assert type(li) == int
            texnum,slicenum = self.allLayers[li]
            glFramebufferTextureLayer(
                GL_FRAMEBUFFER,
                GL_COLOR_ATTACHMENT0+i,                 #which FS output slot
                self.textures[texnum].tex,              #which texture
                0,                                      #mip level
                slicenum )                              #texture slice (layer)
            i+=1
        A = array.array("I",[GL_COLOR_ATTACHMENT0+q for q in range(i)])
        glDrawBuffers(len(A),A)
        glViewport(0,0,self.w,self.h)
        if clear :
            if self.withStencil:
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT )
            else:
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

    def unsetAsRenderTarget(self):
        super().unsetAsRenderTarget()
        for t in self.textures:
            t.bind(0)
            glGenerateMipmap(GL_TEXTURE_2D_ARRAY)
      

    def dump(self,filename,multiplier=1.0):
        for j in range(len(self.textures)):
            t = self.textures[j]
            F = array.array("f",[0]*(t.w*t.h*4*t.slices))
            t.bind(0)
            glGetTexImage(GL_TEXTURE_2D_ARRAY, 0, GL_RGBA, GL_FLOAT, F);
            t.unbind(0)
            B = bytearray(len(F))
            for i in range(len(F)):
                tmp = F[i] * multiplier
                if tmp < 0:
                    tmp = 0.0
                if tmp > 1.0:
                    tmp = 1.0
                B[i] = int(tmp*255)
                
            bytesPerRow = t.w*4
            bytesPerSlice = bytesPerRow*t.h
            si=0  
            for i in range(t.slices):
                dest = bytearray(t.w*t.h*4)
                di=len(dest)-t.w*4    #destination index
                for y in range(t.h):
                    dest[di:di+bytesPerRow] = B[si:si+bytesPerRow]
                    di -= bytesPerRow
                    si += bytesPerRow
                
                fn = "{}-texture-{}-{}.png".format(
                    filename,j,i)
                png = image.encodePNG( t.w,t.h,"RGBA8",dest )
                with open(fn,"wb") as fp:
                    fp.write(png)
                print("Wrote",fn)
  

