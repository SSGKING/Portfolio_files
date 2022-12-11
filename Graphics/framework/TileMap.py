import xml.dom.minidom
import FullScreenQuad
import Program
from math2801 import *
from Texture import *
from dataTexture2DArray import *
from os import *
class TileMap:
    def __init__(self,mapfname,setfname):
        #the parsed document
        X = xml.dom.minidom.parse(os.path.join("assets",mapfname))

        mapelem = X.documentElement
        self.numHorizontalTiles = mapelem.getAttribute("width")
        self.numHorizontalTiles = int(self.numHorizontalTiles)
        self.numVerticalTiles = mapelem.getAttribute("height")
        self.numVerticalTiles = int(self.numVerticalTiles)
        datanode = mapelem.getElementsByTagName("data")[0]
        textnode = datanode.childNodes[0]
        maptext = textnode.data
        maplist = maptext.split(",")
        mapvalues = [int(q)-1 for q in maplist]
        for i in range(0,self.numVerticalTiles//2):
            row1 = i * self.numHorizontalTiles
            row2 = (self.numVerticalTiles-i-1) * self.numHorizontalTiles
            tmp = mapvalues[row1:row1+self.numHorizontalTiles]
            mapvalues[row1:row1+self.numHorizontalTiles] = mapvalues[row2:row2+self.numHorizontalTiles]
            mapvalues[row2:row2+self.numHorizontalTiles] = tmp
        self.fsq = FullScreenQuad()
        self.prog = Program(vs="tilevs.txt",
                            fs="tilefs.txt")
        self.tileW = int(mapelem.getAttribute("tilewidth"))
        self.tileH = int(mapelem.getAttribute("tileheight"))
        self.tileSize = vec2(self.tileW,self.tileH)
        self.tileimages = ImageTexture2DArray("tileset.ora")
        self.whichtiles = DataTexture2DArray(
            self.numHorizontalTiles,
            self.numVerticalTiles,
            1,
            GL_R32F, GL_RED, GL_FLOAT)
        self.whichtiles.setData(
            array.array("f",mapvalues),
            GL_RED,
            GL_FLOAT,
            True)
    def draw(self):
        self.tileimages.bind(0)
        self.whichtiles.bind(1); 
        curr = Program.current
        self.prog.use()
        Program.setUniform("worldMatrix",mat4.identity())
        
        Program.setUniform("tileSize",self.tileSize)
        self.fsq.draw()
        if curr:
            curr.use()
        