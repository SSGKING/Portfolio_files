import json
import os.path
import struct
import collections
from gl import *
from glconstants import *
from ImageTexture2DArray import ImageTexture2DArray
import BufferManager

"""
Key assumptions:
    * Input file is "gltf separate" format
    * All transforms were applied before export
    * No child objects
"""


Material = collections.namedtuple("Material", "baseTextureIndex normalTextureIndex baseTexture emissiveTexture normalTexture mrtexture name")
Item = collections.namedtuple("Item", "vertexOffset indexStart material numIndices name")

class GLTFMesh:
    textureCache={}
    
    def __init__(self,fname):
        folder = os.path.dirname(fname)
        with open(fname) as fp:
            data = fp.read()
        J = json.loads(data)
        scenes = J["scenes"]
        scene = scenes[0]
        bufferDatas = self.loadBuffers(folder,J["buffers"])
        self.items=[]
        for nodeIndex in scene["nodes"]:
            node = J["nodes"][nodeIndex]
            if "mesh" in node:
                meshIndex = node["mesh"]
                mesh = J["meshes"][meshIndex]
                self.getMeshData(bufferDatas, J, mesh)
                
    def loadBuffers( self, folder, buffers ):
        bufferDatas = []
        for buff in buffers:
            path = os.path.join(folder,buff["uri"])
            with open(path,"rb") as fp:
                bufferDatas.append(fp.read())
        return bufferDatas    

    def getItemsMatchingName(self,name):
        L=list( filter( lambda item: item.name == name, self.items ) )
        return L

    def getItemsNotMatchingName(self,name):
        L=list( filter( lambda item: item.name != name, self.items ) )
        return L

    def getMeshData(self,bufferDatas,J,mesh):
        name = mesh["name"]
        for prim in mesh["primitives"]:
            indices = self.extractData(bufferDatas,J,prim["indices"])
            positions = self.extractData(bufferDatas,J,
                prim["attributes"]["POSITION"])
            normals = self.extractData(bufferDatas,J,
                prim["attributes"]["NORMAL"])
            alltexcoords = []
            alltexcoords.append(
                self.extractData(bufferDatas,J,
                    prim["attributes"]["TEXCOORD_0"])
            )
            if "TEXCOORD_1" in prim["attributes"]:
                alltexcoords.append(
                    self.extractData(bufferDatas,J,
                        prim["attributes"]["TEXCOORD_1"])
                )
            mtl = self.getMaterial(J,prim)
            if "TANGENT" in prim["attributes"]:
                tangents = self.extractData(bufferDatas,J,
                    prim["attributes"]["TANGENT"])
            else:
                tangents = [0,0,0,0] * int(len(positions)/3)
            tex = self.getMaterial(J,prim)
            basetexcoords = alltexcoords[mtl.baseTextureIndex]
            bumptexcoords = alltexcoords[mtl.normalTextureIndex]
            vstart,istart = BufferManager.addIndexedData(
                positiondata = positions, texturedata=basetexcoords, 
                normaldata=normals, indexdata=indices,tangentdata=tangents,bumpmapdata=bumptexcoords)
            self.items.append( Item(
                vertexOffset=vstart, 
                indexStart=istart, 
                material=tex, 
                numIndices=len(indices),name=name))

    def getMaterial(self,J,prim):
        mtlIndex = prim["material"]
        mtl = J["materials"][mtlIndex]
        
        index = mtl["pbrMetallicRoughness"]["baseColorTexture"]["index"]
        basetextureFile = self.getTextureFilename(J,index)
        basetexture = self.getTexture(basetextureFile)

        index = mtl["pbrMetallicRoughness"]["metallicRoughnessTexture"]["index"]
        mrtextureFile = self.getTextureFilename(J,index)
        mrtexture = self.getTexture(mrtextureFile)

        if "emissiveTexture" in mtl:
            index = mtl["emissiveTexture"]["index"]
            emissiveTextureFile = self.getTextureFilename(J,index)
            emissivetexture = self.getTexture(emissiveTextureFile)
        else:
            emissivetexture = self.getTexture("black.jpg")
        if "normalTexture" in mtl:
            index = mtl["normalTexture"]["index"]
            normalTextureFile = self.getTextureFilename(J,index)
            normaltexture = self.getTexture(normalTextureFile)
            normalTextureIndex = mtl["normalTexture"].get("texCoord",0)
        else:
            normaltexture = self.getTexture("periwinkle.png")
            normalTextureIndex = 0

        return Material( baseTexture = basetexture,
                        baseTextureIndex = mtl["pbrMetallicRoughness"]["baseColorTexture"].get("texCoord",0),
                        emissiveTexture = emissivetexture,
                        normalTexture = normaltexture,
                        normalTextureIndex = normalTextureIndex,
                        mrtexture = mrtexture,
                        name=mtl["name"])
            

    def getTextureFilename(self,J,index):
        texture = J["textures"][index]
        imageIndex = texture["source"]
        return J["images"][imageIndex]["uri"]

    def getTexture(self,filename):
        if filename not in GLTFMesh.textureCache:
            GLTFMesh.textureCache[filename] = ImageTexture2DArray(filename)
        return GLTFMesh.textureCache[filename]
        
    def draw(self,toDraw=None):
        if toDraw == None:
            toDraw=self.items

        for item in toDraw:
            item.material.baseTexture.bind(0)
            item.material.emissiveTexture.bind(1)
            item.material.normalTexture.bind(2)
            item.material.mrtexture.bind(3)
            glDrawElementsBaseVertex( GL_TRIANGLES, item.numIndices,
                GL_UNSIGNED_INT, item.indexStart, item.vertexOffset )

    def extractData(self,buffers,J,index):
        accessor = J["accessors"][index]
        bufferViewIndex = accessor["bufferView"]
        bufferView = J["bufferViews"][bufferViewIndex]
        buffIndex = bufferView["buffer"]
        data = buffers[buffIndex]
        S = self.makeExtractor(accessor,bufferView)
        count = accessor["count"]
        offset = accessor.get("byteOffset",0) + bufferView.get("byteOffset",0)
        L=[]
        sz = S.size
        for i in range(count):
            L += S.unpack_from(data, offset )
            offset += sz
        return L

    def makeExtractor(self,accessor,bufferView):
        UBYTE=5121; USHORT=5123; UINT=5125; FLOAT=5126  
        typ = accessor["type"]  #SCALAR, VEC2, or VEC3
        comptype = accessor["componentType"]   #UBYTE, USHORT, UINT
        if typ == "VEC2" and comptype == FLOAT:
            fmtcode = "<2f"
        elif typ == "VEC3" and comptype == FLOAT:
            fmtcode = "<3f"
        elif typ == "VEC4" and comptype == FLOAT:
            fmtcode = "<4f"
        elif typ == "SCALAR" and comptype == UBYTE:
            fmtcode = "<B"
        elif typ == "SCALAR" and comptype == USHORT:
            fmtcode = "<H"
        elif typ == "SCALAR" and comptype == UINT:
            fmtcode = "<I"
        else:
            assert 0
        extrabytes = bufferView.get("byteStride",0) - struct.calcsize(fmtcode)
        if extrabytes > 0:
            fmtcode += f"{extrabytes}x"
        return struct.Struct(fmtcode)
        
