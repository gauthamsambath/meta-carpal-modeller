import pickle
import numpy as np
import sys
import shutil
#if first argument is 0 do it for inner mesh else for outer mesh


x = np.loadtxt('temp/X_ray_APinnercontour.txt')

f = open('../2_innerMesh/scripts/python_data/X_ray_APcontour.data', 'wb')

pickle.dump(x, f)
f.close()
print('-----------------')
print('X_ray_APcontour of inner mesh saved in ../2_innerMesh/scripts/python_data/ directory')
print ('-----------------')
x = np.loadtxt('temp/X_ray_MLinnercontour.txt')

f = open('../2_innerMesh/scripts/python_data/X_ray_MLcontour.data', 'wb')
pickle.dump(x, f)
f.close()

print('X_ray_MLcontour of inner mesh saved in ../2_innerMesh/scripts/python_data/ directory')
print('-----------------')

x = np.loadtxt('temp/X_ray_APoutercontour.txt')

f = open('../3_outerMesh/scripts/python_data/X_ray_APcontour.data', 'wb')
pickle.dump(x, f)
f.close()

print('X_ray_APcontour of outer mesh saved in ../3_outerMesh/scripts/python_data/ directory')
print('-----------------')

x = np.loadtxt('temp/X_ray_MLoutercontour.txt')

f = open('../3_outerMesh/scripts/python_data/X_ray_MLcontour.data', 'wb')
pickle.dump(x, f)
f.close()

print ('X_ray_MLcontour of outer mesh saved in ../3_outerMesh/scripts/python_data/ directory')
print('-----------------')

shutil.rmtree('temp')