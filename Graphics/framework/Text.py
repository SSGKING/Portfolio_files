from typing import Text
from FullScreenQuad import FullScreenQuad
from gl import *
from glconstants import *
from Texture import *
from Program import *
from dataTexture2DArray import *
def initialize():
    global fsq
    fsq = FullScreenQuad()
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    global tex
    tex = ImageTexture2DArray("consolefont14.ora")
    global prog
    prog = Program(vs="textvs.txt",fs="textfs.txt")
    global rows
    rows=512//20
    global cols
    cols=512//10
    global chars
    chars = bytearray( rows*cols )
    global charTex
    charTex = DataTexture2DArray( cols,rows,1,GL_R8I, GL_RED_INTEGER, GL_BYTE )
    global dirty
    dirty = True
def putChar(row,col,c):
    global chars,dirty
    idx = row * cols + col
    
    chars[idx] = ord(c)
    dirty = True
def print(row, string):
    
    res = row
    textarray=list(string)
    curCol = 0
    for i in range(len(textarray)):
        while curCol >= cols:
            res -= 1
            curCol -= cols
        putChar(res,curCol,textarray[i])
        curCol += 1

def clear():
    global chars,dirty
    for r in range(rows):
        for c in range(cols):
            putChar(r,c," ")
def draw():
    global dirty, charTex, chars, prog
    if dirty:
        dirty=False
        charTex.setData(chars,
            GL_RED_INTEGER, GL_BYTE,False)
    oldprog = Program.current
    prog.use()
    tex.bind(0)
    charTex.bind(15)
    fsq.draw()
    if oldprog:
        oldprog.use()