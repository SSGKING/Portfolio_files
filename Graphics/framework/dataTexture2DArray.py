
from gl import *
from glconstants import *
from Texture import *

class DataTexture2DArray(Texture2DArray):
    def __init__(self, w,h,slices, iformat, eformat, etype):
        super().__init__(w,h,slices)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        tmp = array.array("I",[0])
        glGenTextures(1,tmp)
        self.tex = tmp[0]
        self.bind(0)
        glTexImage3D( GL_TEXTURE_2D_ARRAY, 0, iformat,
            self.w, self.h, self.slices, 0, eformat, etype, None )
        self.unbind(0)

    def setData(self, data, eformat, etype, generateMips):
        self.bind(0)
        glTexSubImage3D(GL_TEXTURE_2D_ARRAY, #target
            0, #mip level
            0, 0, 0, #x,y,z
            self.w, self.h, self.slices,
            eformat, etype, data )
            
        if generateMips:
            glGenerateMipmaps(GL_TEXTURE_2D_ARRAY)
        self.unbind(0)