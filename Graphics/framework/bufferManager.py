import array
from Buffer import Buffer
from gl import *
from glconstants import *

vao = 0
pdata = []
pbuff = None       #vertex buffer

idata = []     #new
ibuff = None   #new

tbuff = None
tdata = []

ndata = []
nbuff = None



def addData(newpdata):
    global vao, pdata
    if vao != 0:
        raise RuntimeError("Cannot add data after pushToGPU() has been called")
    assert type(newpdata) == list
    oldSize = len(pdata)//3        #get number of points in list
    pdata += newpdata
    return oldSize
def pushToGPU():
    global pbuff,tbuff, ibuff,nbuff, vao
    if pbuff:
        raise RuntimeError("Cannot call pushToGPU twice!")
    A = array.array( "f", pdata )
    pbuff = Buffer( A )
    A = array.array("f",tdata)
    tbuff = Buffer(A)
    
    A = array.array("f",ndata)
    nbuff = Buffer(A)

    A = array.array( "I", idata )      #new
    ibuff = Buffer( A )                #new
    tmp = array.array("I",[0])



    glGenVertexArrays(1,tmp)
    vao = tmp[0]
    glBindVertexArray(vao)
    ibuff.bind(GL_ELEMENT_ARRAY_BUFFER)    #new
    pbuff.bind(GL_ARRAY_BUFFER)


    

    glEnableVertexAttribArray(0)
    glVertexAttribPointer( 0, 3, GL_FLOAT, False, 3*4, 0 )


    tbuff.bind(GL_ARRAY_BUFFER)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1,2,GL_FLOAT,False,2*4,0)

    nbuff.bind(GL_ARRAY_BUFFER)
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2,3,GL_FLOAT,False,3*4,0)
def bind():
    global vao
    if not vao:
        raise RuntimeError("Data hasn't been pushed to GPU")
    glBindVertexArray(vao)
def addIndexedData(*,positiondata,texturedata,normaldata,indexdata):
    global vao, pdata, idata, tdata,ndata
    if vao != 0:
        raise RuntimeError("Cannot add data after pushToGPU() has been called")
    assert type(positiondata) == list
    assert type(indexdata) == list
    startingVertexNumber = len(pdata)//3    #divide by 3 because x,y,z
    indexOffset = len(idata)
    pdata += positiondata
    idata += indexdata
    tdata += texturedata
    ndata += normaldata
    return startingVertexNumber,indexOffset*4

    