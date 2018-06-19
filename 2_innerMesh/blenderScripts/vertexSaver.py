import bpy
import pickle

dataPath = '../dsplab/Desktop/Middle_Meta_Carpal_V2/2_innerMesh/scripts/python_data/'

vertices = bpy.context.active_object.data.vertices

vL = []
for v in vertices:
    x = v.co[0], v.co[1], v.co[2]
    vL.append(x)
    
f = open(dataPath+'Vertices.data','wb')
pickle.dump(vL, f)
f.close()