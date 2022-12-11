from Texture import *
import image

class ImageTextureCube(Texture):

    def __init__(self, px, nx, py, ny, pz, nz):
        
        super().__init__(GL_TEXTURE_CUBE_MAP)
        
        tmp = array.array("I",[0])
        glGenTextures(1,tmp)
        self.tex = tmp[0]
        self.bind(0)
        self.size=None
        
        sides = [
            GL_TEXTURE_CUBE_MAP_POSITIVE_X,
            GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
            GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
            GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
            GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
            GL_TEXTURE_CUBE_MAP_NEGATIVE_Z ]
        
        for side,fname in zip(sides,[px,nx,py,ny,pz,nz]):
            
            lst = ["assets","bigassets"]
            for folder in lst:
                p = os.path.join( os.path.dirname(__file__),folder,fname)
                if os.path.exists(p):
                    with open(p,"rb") as fp:
                        data = fp.read()
                    break
            else:
                raise RuntimeError(f'Could not find {fname} in any of these folders: {" ".join(lst)}')
                
            
            w,h,fmt,data = image.decode(data)
            if w != h:
                raise RuntimeError("Cubemap {} must be square".format(fname))
            if self.size == None:
                self.size = w
            else:
                if self.size != w:
                    raise RuntimeError("Cubemap sides must be the same size: {}".format(fname))
                    
            glTexImage2D(
                side, 0,
                GL_RGBA8, self.size, self.size, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, data )
                
                
        glGenerateMipmap(GL_TEXTURE_CUBE_MAP)
