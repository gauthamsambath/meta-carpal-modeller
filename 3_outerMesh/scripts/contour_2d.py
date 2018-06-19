'''
script to generate 2d vertices from 3d vertices

'''

import numpy as np
import triangulate2D as tr
import pickle
import matplotlib.pyplot as plt

def perspective_project(vertices, plane, cam_position):
	t = -(plane[0]*cam_position[0] + plane[1]*cam_position[1] + plane[2]*cam_position[2] + plane[3])
	projectedList = []	

	for v in vertices:
		lamda = t/(plane[0]*(cam_position[0]-v[0]) + plane[1]*(cam_position[1]-v[1]) + plane[2]*(cam_position[2]-v[2]))

		x = cam_position[0] + lamda*(cam_position[0]-v[0]) 
		y = cam_position[1] + lamda*(cam_position[1]-v[1])
		z = cam_position[2] + lamda*(cam_position[2]-v[2])

		projectedList.append([x,y,z])

	return np.array(projectedList)

def getCentroid(vertices):

	centroid = np.sum(vertices, 0)/vertices.shape[0]

	return centroid


#x, y arguments are to describe the plane
#0, 2 - XZ plane(AP)
#1, 2 - YZ plane(ML)
def getContour(vList, x, y):

	mesh, coordinates = tr.triangulate(vList[:,x], vList[:,y])

	mesh.simplices = tr.contrainMesh(mesh, coordinates, 2)

	mesh.simplices = tr.removeInnerTriangles(mesh)

	mesh.simplices, coordinates, coordinateMap = tr.removeInnerVertices(mesh, coordinates)

	return mesh, coordinates, coordinateMap

#update the 3d-2d dictionary also
def getContourVertices(mesh, coordinates, coordinateMap):
	connDic = {}
	triangles = mesh.simplices

	for tri in triangles:
		for v in tri:
			try:
				connDic[v] +=1
			except:
				connDic[v] = 1
	#remove vertices whose occurence is only one time
	newVInd = []

	for elem in connDic:
		if (connDic[elem] > 1):
			newVInd.append(elem)

	newVInd.sort()
	newVL = []
	newMap = {}
	i=0
	for elem in newVInd:
		newVL.append(coordinates[elem])
		newMap[i] = coordinateMap[elem]
		i=i+1
	return np.array(newVL), newMap


def getMinimumCoordinate(vertices, axis):
	mn = vertices[0][axis]

	for i in range(1, vertices.shape[0]):

		if mn>vertices[i][axis]:
			mn = vertices[i][axis]

	return mn



def project(vertices, *args):
	vertices = np.array(vertices)
	centroid = getCentroid(vertices)
	if (args==()):
		print ('Specify either ML or AP plane')
		return

	elif (args[0]=='ML'):
		#1. ML contour

		#get the lower bound of the shape in x direction
		#the Xray source will be placed on lower bound
	
		xLower = getMinimumCoordinate(vertices, 0)

		#define APplane i.e., XZ plane y=ymin -- 0x+1y+0z=yLower
		ML = [1,0,0,-xLower]


		#define position of the xray camera
		#the camera's axis will be on the centroid axis of the 3d shape
		cameraPos = [1000+xLower,centroid[1],centroid[2]]


		print ('ML plane equation - x='+str(xLower))
		print ('ML camera position = '+str(cameraPos))


		#take perspective projection in AP plane
		projectedVertices = perspective_project(vertices, ML, cameraPos)
		#after projection the dimensions of vertices are still the same

		#get the contour of projected vertices
		#arguments 0 and 2 mean in x-z plane
		mesh, coordinates, coordinateMap = getContour(projectedVertices, 1, 2)

		#get only the boundary vertices
		boundaryPoints, correspondenceMap = getContourVertices(mesh, coordinates, coordinateMap)

		#plot the points to verify
		plt.scatter(boundaryPoints[:,0], boundaryPoints[:,1])
		plt.show()
		return boundaryPoints, correspondenceMap
	elif (args[0]=='AP'):
		#1. AP contour

		#get the lower bound of the shape in y direction
		#the Xray source will be placed on lower bound
		yLower = getMinimumCoordinate(vertices, 1)

		#define APplane i.e., XZ plane y=ymin -- 0x+1y+0z=yLower
		AP = [0,1,0,-yLower]

		#define position of the xray camera
		#the camera's axis will be on the centroid axis of the 3d shape
		cameraPos = [centroid[0],1000+yLower,centroid[2]]


		print ('AP plane equation - y='+str(yLower))
		print ('AP camera position = '+str(cameraPos))


		#take perspective projection in AP plane
		projectedVertices = perspective_project(vertices, AP, cameraPos)
		#after projection the dimensions of vertices are still the same

		#get the contour of projected vertices
		#arguments 0 and 2 mean in x-z plane
		mesh, coordinates, coordinateMap = getContour(projectedVertices, 0, 2)

		#get only the boundary vertices
		boundaryPoints, correspondenceMap = getContourVertices(mesh, coordinates, coordinateMap)

		#plot the points to verify
		plt.scatter(boundaryPoints[:,0], boundaryPoints[:,1])
		plt.show()

		return boundaryPoints, correspondenceMap
	else:
		print (args[0]+' plane not defined.')


#get data from Vertices.data file
dataPath = 'python_data/'
f = open(dataPath+'Vertices_new.data', 'rb')
vertices = pickle.load(f)
f.close()
print(len(vertices))
boundaryPoints, correspondenceMap = project (vertices, 'AP')

#save boundary poins and correspondence map in python data
f = open(dataPath+'AP_contourPoints.data','wb')
pickle.dump(boundaryPoints, f)
f.close()

f = open(dataPath+'AP_correspondenceMap.data','wb')
pickle.dump(correspondenceMap, f)
f.close()


boundaryPoints, correspondenceMap = project (vertices, 'ML')

#save boundary poins and correspondence map in python data
f = open(dataPath+'ML_contourPoints.data','wb')
pickle.dump(boundaryPoints, f)
f.close()

f = open(dataPath+'ML_correspondenceMap.data','wb')
pickle.dump(correspondenceMap, f)
f.close()