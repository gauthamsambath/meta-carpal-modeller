from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
import math
import pickle
#import project as p

#define a helper function for calculating distance between 2d coordinates
def distance(v1, v2):
	return math.sqrt(math.pow(v1[0]-v2[0], 2)+math.pow(v1[1]-v2[1], 2))



#triangulate given x and y coordinates using delaunay and plot
def triangulate(x, y):
	coordinates = []
	for i in range(len(x)):
		coordinates.append([x[i], y[i]])

	coordinates = np.array(coordinates)
	mesh = Delaunay(coordinates)
	return mesh, coordinates



#constrain the mesh by deleting the triangles whose any side is more than constrain
#below 2 functions will be useful
#mesh.simplices = np.delete(mesh.simplices, 1, 0)
#mesh.simplices.size
def contrainMesh(mesh, vertices, contrain_value):
	newSimplices = []
	simplices = mesh.simplices
	for i in range(mesh.simplices.shape[0]):
		#check side of each side of triangle
		tri = mesh.simplices[i]
		#tri will have index number of each vertex
		l1 = distance(vertices[tri[0]], vertices[tri[1]])
		l2 = distance(vertices[tri[1]], vertices[tri[2]])
		l3 = distance(vertices[tri[2]], vertices[tri[0]])
		if l1>contrain_value or l2>contrain_value or l3>contrain_value:
			continue
		else:
			newSimplices.append(tri)
	return np.array(newSimplices)

#Make a function sort 
'''
Arguments - a, b two numbers to be sorted
Return - a,b in sorted order
'''
def sort(a,b):
	if (a>b):
		return b, a
		
	return a, b

#make a function to extract boundary from the triangulated projection
def removeInnerTriangles(mesh):
	edgeDictionary={}
	triangles = mesh.simplices
	newTriangles = []
	for tri in triangles:
		
		e1 = sort(tri[0], tri[1])
		e2 = sort(tri[1], tri[2])
		e3 = sort(tri[0], tri[2])
		#try to find if edge already exists, then increment else make new edge
		try:
			edgeDictionary[e1]+=1
		except:
			edgeDictionary[e1]=1
		try:
			edgeDictionary[e2]+=1
		except:
			edgeDictionary[e2]=1
		try:
			edgeDictionary[e3]+=1
		except:
			edgeDictionary[e3]=1

	#now edge dictionary is complete
	
	#Redo the simplex list
	for tri in triangles:
		e1 = sort(tri[0], tri[1])
		e2 = sort(tri[1], tri[2])
		e3 = sort(tri[0], tri[2])

		if edgeDictionary[e1]==1 or edgeDictionary[e2]==1 or edgeDictionary[e3]==1:
			newTriangles.append(tri)

	return np.array(newTriangles)

#define a function to remove inner vertices from mesh
def removeInnerVertices(mesh, coordinates):
	triangles = mesh.simplices
	indexList = []
	for tri in triangles:
		for ind in tri:
			if ind not in indexList:
				indexList.append(ind)

	indexList.sort()
	j = 0
	for i in range(len(coordinates)):
		if  j<len(indexList) and i == indexList[j]:
			j = j+1
		else:
			coordinates[i] = np.array([0,0])

	newCoordinates = []
	coordinateMap = {}
	j=0
	nMap = {}
	#TODO : organise to make verte
	#vertexIndices = []
	for i in range(len(coordinates)):
		if coordinates[i].all() !=np.array([0,0]).all():
			newCoordinates.append(coordinates[i])
			#vertexIndices.append(i)	
			coordinateMap[i] = j
			nMap[j] = i
			j=j+1
	newCoordinates = np.array(newCoordinates)

	#print vertexIndices
	
	'''
	f = open('indices2.data', 'wb')
	pickle.dump(vertexIndices, f)
	f.close()
	'''
	newTriangles = []

	for tri in triangles:
		nT = []
		for index in tri:
			nT.append(coordinateMap[index])
		newTriangles.append(nT)

	return np.array(newTriangles), newCoordinates, nMap



'''
def getEdgeVertices(mesh, coordinates):
	triangles = mesh.simplices
	vertexIndexList = []
	for tri in triangles:
		for ind in tri:
			if ind not in vertexIndexList:
				vertexIndexList.append(ind)

	newC = []
	for ind in vertexIndexList:
		newC.append(coordinates[ind])
	newC = np.array(newC)
	return newC
'''
#step0	
'''
def main():	
	vertices = p.getVerticesFromPLY('../6_3dModels/meta_carpel_rotated.ply')

#step1 - project, to be changed later
	x, y = p.project(vertices, 1)

#step2 - use delaunay triangulation to triangulate mesh
	mesh, coordinates = triangulate(x, y)
#print coordinates

#step3 - constrain the mesh
	newSimplices = contrainMesh(mesh, coordinates, 2)
	mesh.simplices = newSimplices

#step4 - delete inner triangles from mesh
	newTriangles = removeInnerTriangles(mesh)
	mesh.simplices = newTriangles

#TODO step5 - delete inner vertices from mesh

	mesh.simplices, coordinates = removeInnerVertices(mesh, coordinates)
	print len(coordinates)
#print mesh.simplices


#DEBUG
mesh, coordinates = triangulate( newC[:,0], newC[:,1])
mesh.simplices = contrainMesh(mesh, coordinates, 2)

	plt.triplot(coordinates[:,0], coordinates[:,1], mesh.simplices.copy())
	plt.plot(coordinates[:,0], coordinates[:,1], 'o')
	plt.show()
		
if __name__ == '__main__':
	main()
'''
