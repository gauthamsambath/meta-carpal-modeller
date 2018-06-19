import bpy
import pickle
import numpy as np
import bmesh

path = '../dsplab/Desktop/Middle_Meta_Carpal_V2/3_outerMesh/python_data/newPos.data'

f = open(path, 'rb')
newPos = pickle.load(f)
f.close()


path = '../dsplab/Desktop/Middle_Meta_Carpal_V2/3_outerMesh/python_data/contour2D-3DMap_AP.data'
f = open(path, 'rb')
vDic = pickle.load(f)
f.close()

oldPos = []
vertices = bpy.context.active_object.data.vertices
for elem in vDic:
    x = vertices[vDic[elem]].co
    x = x[0], x[1], x[2]
    oldPos.append(x)
    
bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
for v in bm.verts:
    v.select = False
    
for i in range(len(oldPos)):
    diff = newPos[i][0]-oldPos[i][0], 0, newPos[i][1]-oldPos[i][2], 0
    
    bm.verts[vDic[i]].select=True
    bpy.ops.transform.transform(mode='TRANSLATION', value=diff, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=5)
    bm.verts[vDic[i]].select=False
