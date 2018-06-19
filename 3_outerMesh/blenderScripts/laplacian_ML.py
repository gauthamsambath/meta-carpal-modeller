import pickle
import bpy
import numpy as np
import bmesh
#utility function to select vertices
#arggs if 'list' is given indexList should be given as first argument
#else only the index of vertex to be selected is to be given
def selectVertices(index, *args):
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

#define hook adder for vertices
def addHooks_and_deform(vertexIndices, source_3d, target_3d, correspondence, meshName):
    #add hooks
    for i in vertexIndices:
        selectVertices(i, 'num')
        bpy.ops.object.hook_add_newob()
        
    selectVertices(vertexIndices, 'list')
    
    bpy.ops.object.vertex_group_add()
    bpy.ops.object.vertex_group_assign()

    #apply hook modifier and delete it from stack
    bpy.ops.object.mode_set(mode='OBJECT')

    modifierLen = len(bpy.data.objects[meshName].modifiers)
    for i in range(modifierLen):
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier = bpy.data.objects[meshName].modifiers[0].name)

    bpy.ops.object.mode_set(mode='EDIT')

    #do laplacian deform
    bpy.ops.object.modifier_add(type='LAPLACIANDEFORM')

    bpy.data.objects[meshName].modifiers["LaplacianDeform"].vertex_group = bpy.data.objects[meshName].vertex_groups[bpy.data.objects[meshName].vertex_groups.active_index].name

    bpy.ops.object.laplaciandeform_bind(modifier = "LaplacianDeform")
    bpy.data.objects[meshName].modifiers["LaplacianDeform"].show_in_editmode = True

    bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
    for v in bm.verts:
        v.select = False

    bm.verts.ensure_lookup_table()

    for i in range(len(source_3d)):
        diff = target_3d[i] - source_3d[i]
        diff = diff[0], diff[1], diff[2], 0

        bm.verts[correspondence[i]].select = True
        bpy.ops.transform.transform(mode = 'TRANSLATION', value = diff, proportional = 'DISABLED')
        bm.verts[correspondence[i]].select = False
    
    #Use the below 2 lines of code to delete any object in scene
    #objs = bpy.data.objects
    #objs.remove(objs["Cube"], True)
    #Delete all the objects that do not have the name as 'outer_mesh_new'
    #Essentially delete all the new hook objects created to keep it clean
    objs = bpy.data.objects
    for obj in objs:
        if (obj.name != 'outer_mesh_new'):
            objs.remove(objs[obj.name], True)
            print(obj.name+' deleted')
            
    #apply laplacian modifier in object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="LaplacianDeform")
    bpy.ops.object.mode_set(mode='EDIT')
    #also remove the created vertex group
    #bpy.ops.object.vertex_group_remove(all=True)

def get3D_target(camPos, plane, source_2d, target_2d, source_3d):
    target_3d = []
    for i in range(len(source_2d)):
        #define the 2d source point and 3d point in a plane
        #currently defining only for AP plane
        S2_x = plane
        S2_y = source_2d[i][0]
        S2_z = source_2d[i][1]
        #define parameters of plane a, b, c, d
        #this plane has normal as source line
        #source line is line joining cameraPos and 2d 
        a = camPos[0] - S2_x
        b = camPos[1] - S2_y
        c = camPos[2] - S2_z
        d = -(a*source_3d[i][0]+b*source_3d[i][1]+c*source_3d[i][2])
        
        #define 2d target point as 3d point in a plane 
        #currently defining only for AP plane
        T2_x = plane
        T2_y = target_2d[i][0]
        T2_z = target_2d[i][1]
        #get parameter lamda by finding intersection of plane and target line
        lamda = -(a*camPos[0]+b*camPos[1]+c*camPos[2]+d)/(a*(camPos[0]-T2_x)+b*(camPos[1]-T2_y)+c*(camPos[2]-T2_z))
        
        #put value of lamda in parametric equation of target line and get the 3d target points
        T3_x = camPos[0] + lamda*(camPos[0] - T2_x)
        T3_y = camPos[1] + lamda*(camPos[1] - T2_y)
        T3_z = camPos[2] + lamda*(camPos[2] - T2_z)
        
        T3 = [T3_x,T3_y,T3_z]
        target_3d.append(T3)
        
    target_3d = np.array(target_3d)
    return target_3d
                
AP_camPos = [1000, -0.22289990027644974, -0.23709555329397242]
AP_plane = -6.9628801345825195


#Load AP_contourPoints after SOM deformation
dataPath = 'scripts/python_data/'
f = open(dataPath+'SOM_ML_contourPoints.data', 'rb')
SOM_AP_contourPoints = pickle.load(f)
f.close()
#load also the correspondence map for laplacian deformation
f = open(dataPath+'ML_correspondenceMap.data', 'rb')
AP_correspondenceMap = pickle.load(f)
f.close()
#load AP contourPoints just after ICP
f = open(dataPath+'ICP_ML_contourPoints.data', 'rb')
ICP_AP_contourPoints = pickle.load(f)
f.close()

print (len(SOM_AP_contourPoints), len(ICP_AP_contourPoints))

#get the 3D point cloud using the correspondence map
#mistake:vertices = bpy.context.active_object.data.vertices
#first set mode to edit
bpy.ops.object.mode_set(mode='EDIT')
#get the bmesh
bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
vertices = bm.verts
print(len(vertices))
source_3d = []
for elem in AP_correspondenceMap:
    x = vertices[AP_correspondenceMap[elem]]
    x = x.co[0], x.co[1], x.co[2]
    source_3d.append(x)
    
source_3d = np.array(source_3d)
#print(source_3d)

source_2d = ICP_AP_contourPoints
target_2d = SOM_AP_contourPoints

#get 3d target 
target_3d = get3D_target(AP_camPos, AP_plane, source_2d, target_2d, source_3d)
    
#contains indices of AP silhouette
AP_indexList = []
for elem in AP_correspondenceMap:
    AP_indexList.append(AP_correspondenceMap[elem])
    
addHooks_and_deform(AP_indexList, source_3d, target_3d, AP_correspondenceMap, 'outer_mesh_new')