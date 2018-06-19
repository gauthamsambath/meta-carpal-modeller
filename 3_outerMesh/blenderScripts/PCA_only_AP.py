
import pickle
import bpy
import bmesh
import numpy as np
import math

def error(source, target):
	e = 0
	for i in range(len(source)):
		e = e + math.pow(distance(source[i], target[i]),2)
	e = e/source.shape[0]
	return math.sqrt(e)

def centroid(vertices):
	c = np.sum(vertices, 0)/vertices.shape[0]
	c = c.reshape(1, c.shape[0])
	return c

def distance(p1, p2):
	return (math.sqrt(math.pow(p1[0]-p2[0],2)+math.pow(p1[1]-p2[1],2)))
def PCA(source, target):
	#get centroid points
	source_centroid = centroid(source)
	
	target_centroid = centroid(target)

	M_source = np.dot((source.T - source_centroid.T), source - source_centroid)

	M_target = np.dot((target.T - target_centroid.T), target - target_centroid)

	eig_vec_source = (np.linalg.eig(M_source)[1])
	eig_vec_target = (np.linalg.eig(M_target)[1])

	rotationMatrix = np.dot(eig_vec_target, eig_vec_source.T)

	source_new = (target_centroid.T + np.dot(rotationMatrix, (source-source_centroid).T)).T

	return source_new,rotationMatrix, target_centroid, source_centroid

def get3D_target(camPos, plane, source_2d, target_2d, source_3d):
    target_3d = []
    for i in range(len(source_2d)):
        #define the 2d source point and 3d point in a plane
        #currently defining only for AP plane
        S2_x = source_2d[i][0]
        S2_y = plane
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
        T2_x = target_2d[i][0]
        T2_y = plane
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
                

AP_camPos = [0.05801076079343247,1000,-0.23709555329397242]
AP_plane = -13.831000328063965

dataPath = '../dsplab/Desktop/Middle_Meta_Carpal_V2/3_outerMesh/scripts/python_data/'

#get the old 2D contour
#these will be 2d source points
f = open(dataPath+'AP_contourPoints.data', 'rb')
AP_contourPoints = pickle.load(f)
f.close()



#load the new contour points
#these will be 2d target points
f = open(dataPath+'ICP_AP_contourPoints.data', 'rb')
ICP_AP_contourPoints = pickle.load(f)
f.close()

#get the correspondence map
f = open(dataPath+'AP_correspondenceMap.data', 'rb')
AP_correspondenceMap = pickle.load(f)
f.close()


vertices = bpy.context.active_object.data.vertices
source_3d = []

for elem in AP_correspondenceMap:
    x = vertices[AP_correspondenceMap[elem]]
    x = x.co[0], x.co[1], x.co[2]
    source_3d.append(x)
    
source_3d = np.array(source_3d)

target_3d = get3D_target(AP_camPos, AP_plane, AP_contourPoints, ICP_AP_contourPoints, source_3d)
print(error(source_3d, target_3d))

source, rotationMatrix, target_centroid, source_centroid = PCA(source_3d, target_3d)

#use the rotation matrix to change model to new points
#first set mode to edit
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)

#deselect all vertices
for v in bm.verts:
    v.select=False
#rotate all vertices
for v in bm.verts:
    v.select=True
    #define coordinate as 1
    oldPos = np.array([[v.co[0], v.co[1], v.co[2]]])
    #newPos = np.dot(oldPos, RotMatrix)
    newPos = (target_centroid.T + np.dot(rotationMatrix, (oldPos-source_centroid).T)).T    
    diff = oldPos-newPos
    diff = -diff[0]
    #print(diff)
    diffTup = diff[0], diff[1], diff[2], 0
    
    bpy.ops.transform.transform(mode='TRANSLATION', value=diffTup, proportional='DISABLED')
    
    v.select = False

print (error (source, target_3d))