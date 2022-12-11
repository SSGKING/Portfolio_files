
from gl import *
from glconstants import *
import bufferManager as BufferManager
import Program
import Globals as globs


class Hexagon:
    def __init__(self):

        
        glClearColor(0.0, 0.0, 0.0, 1 )
       
        triverts = [
            -.25,   0.5 , 0.0,  
            -0.5,   0.0, 0.0,    
            0.0,   0.0, 0.0,

           # -0.25,   0.5 , 0.0,   
            0.25,   0.5, 0.0,    
            #0.0,   0.0, 0.0,

           # 0.25,   0.5 , 0.0,   
            0.5,   0.0, 0.0,    
           # 0.0,   0.0, 0.0,


            -.25,   -0.5 , 0.0,  
           # -0.5,   0.0, 0.0,    
          # 0.0,   0.0, 0.0,


           # -0.25,   -0.5 , 0.0,   
            0.25,   -0.5, 0.0,    
           # 0.0,   0.0, 0.0,

          #  0.25,   -0.5 , 0.0,   
           # 0.5,   0.0, 0.0,    
          #  0.0,   0.0, 0.0,
            ]
        idata = [0,1,2, 0,2,3, 2,3,4, 1,2,5, 2,5,6, 2,4,6]
        
        self.startVert,self.indexoffset = BufferManager.addIndexedData(positiondata = triverts,indexdata =idata)

        
    def draw(self):
        
        glDrawElementsBaseVertex(GL_TRIANGLES,18,GL_UNSIGNED_INT,self.indexoffset,self.startVert)

        #glDrawArrays(GL_TRIANGLES, 0, 54 )