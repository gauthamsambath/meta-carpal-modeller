import pickle
import numpy as np
import matplotlib.pyplot as plt
import math

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

	return source_new

def SVD(source, target):
	centroid_source = centroid(source)
	centroid_target = centroid(target)

	P = (source - centroid_source).T
	Q = (target - centroid_target)

	M = np.dot(P, Q)

	u, s, vh = np.linalg.svd(M, full_matrices=True)

	#rotation matrix 
	R = np.dot(vh, u.T)

	new_source = (centroid_target.T + np.dot(R, (source-centroid_source).T)).T
	return new_source




#function to equalise number of points in source and target vertices
#for SVD 
def equalize(source, target):
	new_target = []

	for point in source:
		minD = distance(point, target[0])
		ind = 0
		for i in range(1, len(target)):
			if minD>distance(point, target[i]):
				minD = distance(point, target[i])
				ind = i
		new_target.append(target[ind])

	return np.array(new_target)

def error(source, target):
	e = 0
	for i in range(len(source)):
		e = e + math.pow(distance(source[i], target[i]),2)
	e = e/source.shape[0]
	return math.sqrt(e)


#ML plane begin


f = open('python_data/X_ray_MLcontour.data', 'rb')
X_ray_MLcontour = pickle.load(f)
f.close()

f = open('python_data/ML_contourPoints.data', 'rb')
ML_contourPoints = pickle.load(f)
f.close()


newML_contour = PCA(ML_contourPoints, X_ray_MLcontour)
#plt.scatter(X_ray_APcontour[:, 0], X_ray_APcontour[:,1], color='g')
#plt.scatter(newAP_contour[:, 0], newAP_contour[:,1], color='r')

#plt.show()
temp = newML_contour


for i in range(30):
	new_target = equalize(temp, X_ray_MLcontour)

	temp = SVD(temp, new_target)
	print(error(temp, new_target))
#plt.scatter(new_target[:, 0], new_target[:, 1])

	plt.cla()
	plt.scatter(X_ray_MLcontour[:,0], X_ray_MLcontour[:,1])	
	plt.scatter(temp[:, 0], temp[:, 1], color='r')
	plt.draw()
	plt.pause(0.1)	

plt.show()

#AP plane begin

f = open('python_data/ICP_ML_contourPoints.data', 'wb')
pickle.dump(temp,f)
f.close()

f = open('python_data/X_ray_APcontour.data', 'rb')
X_ray_APcontour = pickle.load(f)
f.close()

f = open('python_data/AP_contourPoints.data', 'rb')
AP_contourPoints = pickle.load(f)
f.close()


newAP_contour = PCA(AP_contourPoints, X_ray_APcontour)
#plt.scatter(X_ray_APcontour[:, 0], X_ray_APcontour[:,1], color='g')
#plt.scatter(newAP_contour[:, 0], newAP_contour[:,1], color='r')

#plt.show()
temp = newAP_contour


for i in range(30):
	new_target = equalize(temp, X_ray_APcontour)

	temp = SVD(temp, new_target)
	print(error(temp, new_target))
#plt.scatter(new_target[:, 0], new_target[:, 1])

	plt.cla()
	plt.scatter(X_ray_APcontour[:,0], X_ray_APcontour[:,1])	
	plt.scatter(temp[:, 0], temp[:, 1], color='r')
	plt.draw()
	plt.pause(0.1)	

plt.show()

f = open('python_data/ICP_AP_contourPoints.data', 'wb')
pickle.dump(temp,f)
f.close()

