import array
from Buffer import *

vao=0
pdata=[]
pbuff=None
tdata=[]
tbuff=None
ndata=[]
nbuff=None
idata=[]
ibuff=None
tandata =[]
tanbuff = None
bumpdata = []
bumpbuff = None


def addData( newpdata ):
    global vao, pdata
    if vao != 0:
        raise RuntimeError("Cannot add data after pushToGPU() has been called")
    assert type(newpdata) == list
    oldSize = len(pdata)//3        #get number of points in list
    pdata += newpdata
    return oldSize
 
def addIndexedData(*, positiondata, texturedata, normaldata, indexdata, tangentdata,bumpmapdata):
    global vao, pdata, tdata, idata, ndata,tandata,bumpdata
    if vao != 0:
        raise RuntimeError("Cannot add data after pushToGPU() has been called")
    assert type(positiondata) == list
    assert type(texturedata) == list       
    assert type(normaldata) == list       
    assert type(indexdata) == list
    assert type(tangentdata) == list
    assert type(bumpmapdata) == list
    assert len(positiondata)//3 == len(texturedata)//2    
    assert len(positiondata)//3 == len(normaldata)//3    
    startingVertexNumber = len(pdata)//3
    indexStart = len(idata)
    pdata += positiondata
    tdata += texturedata          
    ndata += normaldata
    idata += indexdata
    tandata += tangentdata
    bumpdata += bumpmapdata
    return startingVertexNumber,indexStart*4
    
def pushToGPU():
    global vao
    global pbuff,tbuff,ibuff,tanbuff,bumpbuff
    global pdata,tdata,idata,tandata,bumpdata
    pbuff = Buffer( array.array( "f", pdata ) )
    tbuff = Buffer( array.array( "f", tdata ) )    
    nbuff = Buffer( array.array( "f", ndata ) )    
    ibuff = Buffer( array.array( "I", idata ) )
    tanbuff = Buffer(array.array("f",tandata))
    bumpbuff = Buffer(array.array("f",bumpdata))
    tmp = array.array("I",[0])
    glGenVertexArrays(1,tmp)
    vao = tmp[0]
    glBindVertexArray(vao)
    ibuff.bind(GL_ELEMENT_ARRAY_BUFFER)
    pbuff.bind(GL_ARRAY_BUFFER)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer( 0, 3, GL_FLOAT, False, 3*4, 0 )
    tbuff.bind(GL_ARRAY_BUFFER)         
    glEnableVertexAttribArray(1)            
    glVertexAttribPointer( 1, 2, GL_FLOAT, False, 2*4, 0 )  
    nbuff.bind(GL_ARRAY_BUFFER)        
    glEnableVertexAttribArray(2)            
    glVertexAttribPointer( 2, 3, GL_FLOAT, False, 3*4, 0 )  
    tanbuff.bind(GL_ARRAY_BUFFER)
    glEnableVertexAttribArray(3)            
    glVertexAttribPointer( 3, 3, GL_FLOAT, False, 3*4, 0 )  
    bumpbuff.bind(GL_ARRAY_BUFFER)
    glEnableVertexAttribArray(4)            
    glVertexAttribPointer( 4, 2, GL_FLOAT, False, 2*4, 0 )  


def bind():
    if not vao:
        raise RuntimeError("Data hasn't been pushed to GPU")
    glBindVertexArray(vao)
