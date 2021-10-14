from stl import mesh
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import griddata
from cv2 import cv2
import itertools
import multiprocessing
#

your_mesh = mesh.Mesh.from_file ('/Users/shuan/Desktop/20210505_S_R/SCORPIO_R20210505.stl')
x_coordinate = your_mesh.x[:,0].flatten()
y_coordinate = your_mesh.y[:,0].flatten()
z_coordinate = your_mesh.z[:,0].flatten()

grid_size=math.ceil(max(x_coordinate.max(),y_coordinate.max()))            
image_sizex= grid_size*1000
image_sizey= grid_size*1000
LCDXUseage = 500#子圖片pixel數 預設1000
LCDYUseage = 500
xsheet=int(image_sizex/(LCDXUseage)) #計算x軸子圖片張數
ysheet=int(image_sizey/(LCDYUseage)) #計算x軸子圖片張數
shiftx=grid_size*LCDXUseage/image_sizex
shifty=grid_size*LCDYUseage/image_sizey
zmax = z_coordinate.max()

layers = 10 #層數 預設10
layer=np.linspace(z_coordinate.min(), zmax, layers)
save_file = '/Users/shuan/Desktop/imageoutput/wwww'

start_time = time.time()


def interpolation(x,y,z, Pv, Qv):
    znew = griddata((x,y), z, (Pv, Qv), method = 'linear')  
    znew[znew<0] = 0            
    return znew


def process(pa):
    picture_name='2'
    xsheet = pa[0]
    ysheet = pa[1]
    P = np.linspace(shiftx*(xsheet+1), shiftx*(xsheet), LCDXUseage)
    Q = np.linspace(shifty*(ysheet+1), shifty*(ysheet), LCDYUseage)    
    Pv, Qv = np.meshgrid(P,Q)  
    znew_cubic = interpolation(x_coordinate,y_coordinate,z_coordinate, Pv, Qv)  
    znew_cubic = (znew_cubic % (zmax/(layers-1)))*\
    (255/(zmax/(layers-1)))
    cv2.imwrite(save_file+'\\image'+'\\{}_{}_{}.bmp' \
    .format(picture_name,xsheet+1,ysheet+1),znew_cubic) 


if __name__ == '__main__':
    xsheet = np.arange(0,xsheet,1)
    ysheet = np.arange(0,ysheet,1)
    paramlist = list(itertools.product(xsheet,ysheet))
    pool = multiprocessing.Pool(processes=6,maxtasksperchild=1000)
    #Distribute the parameter sets evenly across the cores
    res  = pool.map(process,paramlist)
    end_time_2 = time.time()    
    print('O2 cosume time = ', end_time_2 - start_time , 's')  



