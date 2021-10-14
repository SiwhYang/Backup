from stl import mesh
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import griddata
from cv2 import cv2
import test_cpp



your_mesh = mesh.Mesh.from_file ('/Users/shuan/Desktop/20210505_S_R/SCORPIO_R20210505.stl')
x_coordinate = your_mesh.x[:,0].flatten()
y_coordinate = your_mesh.y[:,0].flatten()
z_coordinate = your_mesh.z[:,0].flatten()

grid_size=math.ceil(max(x_coordinate.max(),y_coordinate.max()))            
image_sizex= grid_size*1000
image_sizey= grid_size*1000
LCDXUseage = 3000#子圖片pixel數 預設1000
LCDYUseage = 3000
xsheet=int(image_sizex/(LCDXUseage)) #計算x軸子圖片張數
ysheet=int(image_sizey/(LCDYUseage)) #計算x軸子圖片張數
shiftx=grid_size*LCDXUseage/image_sizex
shifty=grid_size*LCDYUseage/image_sizey
zmax = z_coordinate.max()

layers = 10 #層數 預設10
layer=np.linspace(z_coordinate.min(), zmax, layers)
save_file = '/Users/shuan/Desktop/imageoutput/wwww'
'''
LCDxshift = 1000 #圖片x軸間距pixel的參數 預設1000
print('image_size = ',image_sizex)
shiftx = grid_size*LCDXUseage/image_sizex #算x軸子圖片間隔pixel數 算出為１
image_sizex = grid_size * 1000  #如果X軸比y軸長的話
#image_sizex = (grid_size / grid_size ) * lcddxuseafe / 1000 = 1
print('shiftx = ',shiftx)
'''
start_time = time.time()

class scipy_method:
    '''
    def interpolation(self,x,y,z, Pv, Qv):
        interp = LinearNDInterpolator(list(zip(x, y)), z)
        znew = interp(Pv, Qv)
        return znew
    '''
    def interpolation(self,x,y,z, Pv, Qv):
        znew = griddata((x,y), z, (Pv, Qv), method = 'linear')  
        znew[znew<0] = 0            
        return znew
    
    def operator1 (self):
        picture_name='1'
        
        for i in range(xsheet):
            for j in range(ysheet):
                P = np.linspace(shiftx*(i+1), shiftx*(i), LCDXUseage)
                Q = np.linspace(shifty*(j+1), shifty*(j), LCDYUseage)    
                Pv, Qv = np.meshgrid(P,Q)  
                znew_cubic = self.interpolation(x_coordinate,y_coordinate,z_coordinate, Pv, Qv) 
                for l in range(len(layer)-1):
                    zm=layer[l]
                    ZM=layer[l+1] 
                    znew_cubic[(znew_cubic>zm)&(znew_cubic<=ZM)] \
                    =((znew_cubic[(znew_cubic>zm)&(znew_cubic<=ZM)]-zm)/(ZM-zm))*255 
                    cv2.imwrite(save_file+'\\image'+'\\{}_{}_{}.bmp'.format(picture_name,i+1,j+1),znew_cubic) 
                    
    def operator2 (self):
        picture_name='2'
        for i in range(xsheet):
            for j in range(ysheet):
                P = np.linspace(shiftx*(i+1), shiftx*(i), LCDXUseage)
                Q = np.linspace(shifty*(j+1), shifty*(j), LCDYUseage)    
                Pv, Qv = np.meshgrid(P,Q)  
                znew_cubic = self.interpolation(x_coordinate,y_coordinate,z_coordinate, Pv, Qv)  
                z_layers = (zmax/(layers-1))
                znew_cubic = test_cpp.remainder1(znew_cubic,z_layers)
                cv2.imwrite(save_file+'\\image'+'\\{}_{}_{}.bmp' \
                .format(picture_name,i+1,j+1),znew_cubic) 

    def operator3 (self):
        picture_name='3'
        for i in range(xsheet):
            for j in range(ysheet):
                P = np.linspace(shiftx*(i+1), shiftx*(i), LCDXUseage)
                Q = np.linspace(shifty*(j+1), shifty*(j), LCDYUseage)    
                Pv, Qv = np.meshgrid(P,Q)  
                znew_cubic = self.interpolation(x_coordinate,y_coordinate,z_coordinate, Pv, Qv)  
                znew_cubic = (znew_cubic % (zmax/(layers-1)))*\
                (255/(zmax/(layers-1)))
                cv2.imwrite(save_file+'\\image'+'\\{}_{}_{}.bmp' \
                .format(picture_name,i+1,j+1),znew_cubic) 


    
'''                
znew_cubic = (znew_cubic % (zmax/(layers-1)))*\
                (255/(zmax/(layers-1)))
'''

#z_layers = (zmax/(layers-1))
#znew_cubic = (znew_cubic % z_layers)*(255/z_layers)
#先取出每層在原scale的寬度 然後將原本的scale除以這寬度取餘數 將這餘數放大到255 scale
result = scipy_method()


result.operator1()
end_time_1 = time.time()    
print('O1 cosume time = ', end_time_1 - start_time, 's')   

result.operator2()        
end_time_2 = time.time()    
print('O2 cosume time = ', end_time_2 - end_time_1 , 's')   

result.operator3()
end_time_3 = time.time()
print('O3 cosume time = ', end_time_3 - end_time_2 , 's')  
 
'''
HRESHOLD = 0.01

from scipy.interpolate.interpnd import _ndim_coords_from_arrays
from scipy.spatial import cKDTree

# Construct kd-tree, functionality copied from scipy.interpolate
tree = cKDTree(xy)
xi = _ndim_coords_from_arrays(tuple(Pv, Qv), ndim=xy.shape[1])
dists, indexes = tree.query(xi)
'''
