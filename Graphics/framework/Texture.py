#Texture.py
from gl import *
from glconstants import *

import io
import os.path
import image
import zipfile

class Texture:
    def __init__(self, typ):
        self.type = typ
        self.tex = None
    def bind(self,unit):
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(self.type,self.tex)
    def unbind(self,unit):
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(self.type,0)

class Texture2DArray(Texture):
    def __init__(self,w,h,slices):
        Texture.__init__(self,GL_TEXTURE_2D_ARRAY)
        self.w=w
        self.h=h
        self.slices=slices

class ImageTexture2DArray(Texture2DArray):
    def __init__(self, *files):
        super().__init__(0,0,0)
        membuf = io.BytesIO()
        for fname in files:
            for folder in ["assets","bigassets"]:
                p = os.path.join(os.path.dirname(__file__),folder,fname)
                if os.path.exists(p):
                    break
            fname = p
            if fname.endswith(".png") or fname.endswith(".jpg"):
                self.loadImage(membuf,fname)
            elif fname.endswith(".ora") or fname.endswith(".zip"):
                self.loadZip(membuf,fname)
            else:
                raise RuntimeError("Cannot read file "+fname)

        self.pushToGPU( membuf )
    def loadImage(self,membuf,fname):
        with open(fname,"rb") as fp:
            tmp = fp.read()
    
        self.addImageDataToBuffer(membuf,tmp)
    def addImageDataToBuffer(self,membuf,img):
        pw,ph,fmt,pix = image.decode(img)
        pix = image.flipY(pw,ph,pix)
        if self.w == 0:
            self.w=pw
            self.h=ph
        else:
            if self.w != pw or self.h != ph:
                raise RuntimeError("Size mismatch")
        self.slices += 1
        membuf.write(pix)
    def loadZip(self,membuf,fname):
        z = zipfile.ZipFile(fname)
        for n in sorted(z.namelist()):
            if n.lower().endswith(".png") or n.lower().endswith(".jpg"):
                tmp = z.open(n).read()
                self.addImageDataToBuffer( membuf, tmp )
        z.close()

    def pushToGPU(self,membuf):
        tmp = array.array("I",[0])
        glGenTextures(1,tmp)
        self.tex = tmp[0]
        self.bind(0)
        glTexImage3D( GL_TEXTURE_2D_ARRAY, 0, GL_RGBA8, self.w,
                    self.h, self.slices, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                    membuf.getbuffer() )
        glGenerateMipmap(GL_TEXTURE_2D_ARRAY)
        self.unbind(0)