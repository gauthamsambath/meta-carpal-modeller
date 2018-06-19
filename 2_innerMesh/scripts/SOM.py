import math
import numpy as np
import pickle 
import matplotlib.pyplot as plt


#utility function to get the distance between 2 points
def distance(a, b):
	x = a-b
	x = np.power(x,2)
	return math.sqrt(np.sum(x))

def n(a, b, t_frac):
	dst = distance(a,b)
	sigma = 0.6+t_frac*(0.1-0.6)
	p = dst/(2*np.power(sigma,2))
	return np.exp(-p)

def SOM(source, target):
	total_iter = 10


	for current_iter in range(total_iter):
		#go through all the target points
		for i in range(len(target)):
			target_vertex = target[i]
			#get the source point that is nearest to target_vertex
			m = distance(source[0], target_vertex)
			winner_index = 0
			for i in range(1, len(source)):
				d = distance(source[i], target_vertex)
				if (d<m):
					m=d
					winner_index = i

			#source[winner_index] is the source point that is nearest to target_vertex

			#define t_frac
			t_frac = float(current_iter+1)/float(total_iter)

			#print (t_frac)
			#define update factor l
			l = 0.5 + t_frac*(0.1-0.5)
			#update each source point to the new source point
			for i in range(len(source)):
				source[i] = source[i] + l*n(source[winner_index], source[i], t_frac)*(target_vertex - source[i])

			#print(source, target)
			
			#if (i>=10):
			#	break

			plt.cla()
			plt.scatter (source[:,0], source[:,1], color = 'r')

			plt.scatter (target[:,0], target[:,1])
			plt.draw()
			plt.pause(0.001)
	plt.show()
	return source


def elem_found(vertex, vertex_list):
	flag = 0
	for v in vertex_list:
		if vertex.all() == v.all():
			return True
	return False

def minimize(source,target):
	newTarget = []
	for i in range(len(source)):
		d_min = distance(source[i], target[0])
		min_index = 0
		for j in range(1,len(target)):
			d = distance(source[i], target[j])
			if d<d_min and (elem_found(target[j], newTarget)):
				d_min = d
				min_index = j

		newTarget.append(target[min_index])
	return np.array(newTarget)


dataPath = 'python_data/'


#perform SOM for AP plane

#load the source points i.e., ICP_AP_contourPoints
f = open(dataPath+'ICP_ML_contourPoints.data', 'rb')
source = pickle.load(f)
f.close()

#load the target points i.e., X_ray_APcontour
f = open(dataPath+'X_ray_MLcontour.data', 'rb')
target = pickle.load(f)
f.close()

#newTarget = target

newTarget = minimize(source, target)

#print (len(newTarget),len(source))

plt.scatter (source[:,0], source[:,1], color = 'r')
plt.scatter (newTarget[:,0], newTarget[:,1])
plt.show()


SOM_AP_contourPoints = SOM(source, newTarget)

#save the new source points as SOM_AP_contourPoints.data
f = open(dataPath+'SOM_AP_contourPoints.data', 'wb')
pickle.dump(SOM_AP_contourPoints, f)
f.close()
print('--------------')
print('modified AP contour points saved as SOM_AP_contourPoints.data in python_data directory')

#perform SOM for ML plane


#load the source points i.e., ICP_AP_contourPoints
f = open(dataPath+'ICP_ML_contourPoints.data', 'rb')
source = pickle.load(f)
f.close()

#load the target points i.e., X_ray_APcontour
f = open(dataPath+'X_ray_MLcontour.data', 'rb')
target = pickle.load(f)
f.close()

#newTarget = target

newTarget = minimize(source, target)

#print (len(newTarget),len(source))

plt.scatter (source[:,0], source[:,1], color = 'r')
plt.scatter (newTarget[:,0], newTarget[:,1])
plt.show()


SOM_AP_contourPoints = SOM(source, newTarget)

#save the new source points as SOM_AP_contourPoints.data
f = open(dataPath+'SOM_ML_contourPoints.data', 'wb')
pickle.dump(SOM_AP_contourPoints, f)
f.close()

print('--------------')
print('modified AP contour points saved as SOM_ML_contourPoints.data in python_data directory')