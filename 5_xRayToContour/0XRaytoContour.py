'''
Script to extract edge from segmented image and make it as 2d coordinate points

'''

import cv2

import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys
import os

def centroid(vertices):
	c = np.sum(vertices, 0)/vertices.shape[0]
	c = c.reshape(1, c.shape[0])
	return c

print (sys.argv)
#get arguments from the system
#2nd argument is the image name
#3rd argument is the destination name
if (len(sys.argv)<3):
	print '-----------------------'
	print '1st argument - Image name'
	print '2nd argument - Any string, edge detected image and contour file will be save by this name'



	print '-----------------------'
	exit()
source = sys.argv[1]
dest = sys.argv[2]

img = cv2.imread(source, 0)
if img==None:
	print '-----------------------'
	print 'No jpg image named '+source
	print '-----------------------'
	print 'convert it to jpg'
	exit()
edgeD = cv2.Canny(img, 230, 250)

cv2.imwrite(dest+'.jpg', edgeD)

print '-----------------------'
print 'Edge detected image saved as '+dest+'.jpg'

XRay_contour = []

print '-----------------------'
print 'Converting edge points to 2d coordinates'

for i in range(edgeD.shape[0]):
	for j in range(edgeD.shape[1]):
		if edgeD[i][j] == 255:
			x = [j*0.139, -i*0.139]
			XRay_contour.append(x)
XRay_contour = np.array(XRay_contour)
#print XRay_contour

#shift centroid to origin
centroid = centroid(XRay_contour)
XRay_contour = XRay_contour- centroid

try:
	os.mkdir('temp')
except:
	print('temp already made')

np.savetxt('temp/'+dest+'.txt',XRay_contour)
print '-----------------------'
print 'Edge coordinates saved as '+dest+'.txt'
plt.scatter(XRay_contour[:,0], XRay_contour[:,1])
plt.show()