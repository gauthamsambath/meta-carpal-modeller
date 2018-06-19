import bpy
import pickle

vertices = bpy.context.active_object.data.vertices

vl = []
for v in vertices:
    x=v.co[0], v.co[1], v.co[2]
    vl.append(x)
    
f = open('2_innerMesh/python_data/innerVertices.data', 'wb')
pickle.dump(vl, f)
f.close()
