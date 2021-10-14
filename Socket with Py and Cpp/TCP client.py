#from socket import *
#port = 37716
#ClientSock = socket(AF_INET, SOCK_STREAM)
#ClientSock.connect(('', port))

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
import socket
import sys
HOST, PORT = "localhost", 37716
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


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
    

start_time = time.time()
picture_name='2'
for i in range(xsheet):
    for j in range(ysheet):
        P = np.linspace(shiftx*(i+1), shiftx*(i), LCDXUseage)
        Q = np.linspace(shifty*(j+1), shifty*(j), LCDYUseage)    
        Pv, Qv = np.meshgrid(P,Q)  
        znew_cubic = interpolation(x_coordinate,y_coordinate,z_coordinate, Pv, Qv)  
        znew_cubic = (znew_cubic % (zmax/(layers-1)))*\
        (255/(zmax/(layers-1)))
        cv2.imwrite(save_file+'\\image'+'\\{}_{}_{}.bmp' \
        .format(picture_name,i+1,j+1),znew_cubic) 
        
        
        stratmessage = 'Image '
        stringi = str(i)
        stringj = str(j)
        endmessage = ' is done !'
        spacestring = ' '
        message_send_to_server = stratmessage+stringi+spacestring+stringj+endmessage
        s.send(bytes(message_send_to_server, 'utf-8'))

end_time = time.time()
print('cosume time =', end_time-start_time, 's')



'''

for x in range(0, 5):
    #print("Step 1")
    #s.send(b'Heo')
    s.send(b'x')
    time.sleep(1)
    #print("Step 2")
    #print(str(s.recv(1000)))
    #print(x)
'''