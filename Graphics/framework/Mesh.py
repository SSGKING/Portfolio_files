from gl import *
from glconstants import *
import os.path
import itertools
import bufferManager as BufferManager
import Texture
class Mesh:
    def __init__(self,fname):
        for folder in ["assets","bigassets"]:
            p = os.path.join(os.path.dirname(__file__),folder,fname)
            if os.path.exists(p):
                break

        positions = [] 
        indices = []
        texes=[]
        normals = []
        materials = {}      #new
        mtlname = None      #new
        with open(p) as fp:
            for line in fp:
                line = line.strip()
                if line.startswith("v "):
                    tmp3 = [float(q) for q in line.split()[1:] ]
                    positions.append(tmp3)

                elif line.startswith("f "):
                    lst = line.split()[1:]
                    if len(lst) != 3:
                        raise RuntimeError("Mesh {} has non-triangles".format(fname))
                    for s in lst:
                        tmp = s.split("/")
                        vi = int(tmp[0])-1
                        if len(tmp) < 3:
                            raise RuntimeError("Missing normals in {}".format(fname))
                        ti = int(tmp[1])-1
                        ni = int(tmp[2])-1
                        indices.append( (vi,ti,ni) )
                elif line.startswith("vn "):
                    normals.append([float(q)for q in line.split()[1:]])
                elif line.startswith("vt "):
                    texes.append( [float(q) for q in line.split()[1:]])
                elif line.startswith("mtllib "):
                    mtlfile = line.split(" ",1)[1]
                    self.parseMaterialFile( mtlfile, materials )
                elif line.startswith("usemtl "):
                    mtlname = line.split(" ",1)[1]


                else:
                    pass
        vertexMap = {}
        remappedPosData = []
        remappedTexData = []
        remappedIndices = []
        remappedNormalData = []

        #n = 0
        for vertexSpec in indices:
            if vertexSpec not in vertexMap:
                vi,ti,ni = vertexSpec
                n = len(remappedPosData)//3
                remappedPosData += positions[vi]
                remappedTexData += texes[ti]
                remappedNormalData += normals[ni]
                vertexMap[vertexSpec] = n
                #n += 1
            remappedIndices.append( vertexMap[vertexSpec] )
        self.vertexOffset, self.indexStart = BufferManager.addIndexedData(
        positiondata=remappedPosData,
        texturedata=remappedTexData,
        normaldata = remappedNormalData,
        indexdata=remappedIndices
        )
        self.numIndices = len(remappedIndices)

        if mtlname == None:
            raise RuntimeError("No texture on mesh {}".format(fname))
        elif mtlname not in materials:
            raise RuntimeError(
                "No texture for material {} on mesh {}".format(mtlname,
                fname))
        else:
            self.tex = Texture.ImageTexture2DArray( materials[mtlname] )


    def parseMaterialFile( self, fname, materials):
        for folder in ["assets","bigassets"]:
            p = os.path.join(os.path.dirname(__file__),folder,fname)
            if os.path.exists(p):
                break
        with open(p) as fp:
            for line in fp:
                line = line.strip()
                if line.startswith("newmtl"):
                    currmtl = line.split()[1]
                elif line.startswith("usemtl "):
                    mtlname = line.split(" ",1)[1]
                elif line.startswith("map_Kd"):
                    materials[currmtl] = line.split(" ",1)[1]

    def draw(self):
        self.tex.bind(0)
        glDrawElementsBaseVertex( GL_TRIANGLES, self.numIndices,
            GL_UNSIGNED_INT, self.indexStart, self.vertexOffset )