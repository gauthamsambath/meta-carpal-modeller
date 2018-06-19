import bpy
import pickle

def selectVertices(index, *args):
    print(args)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    if args[0]=='list':
        for ind in index:
            obj.data.vertices[ind].select = True        
    else:
        obj.data.vertices[index].select = True
    bpy.ops.object.mode_set(mode = 'EDIT') 

path='../dsplab/Desktop/Middle_Meta_Carpal_V2/3_outerMesh/python_data'

f = open(path+'/contour2D-3DMap_AP.data', 'rb')
contourMap = pickle.load(f)
f.close()

indices= []
for elem in contourMap:
    indices.append(contourMap[elem])
    
for i in indices:
    selectVertices(i, 'num')
    bpy.ops.object.hook_add_newob()
    
    
selectVertices(indices, 'list')

bpy.ops.object.vertex_group_add()
bpy.ops.object.vertex_group_assign()

bpy.ops.object.modifier_add(type='LAPLACIANDEFORM')

bpy.data.objects["plyModel"].modifiers["LaplacianDeform"].vertex_group = "Group"

