import math
import numpy as np
import os

#   fit a sphere to X,Y, and Z data points
#   returns the radius and center points of
#   the best fit sphere
def sphereFit(spX,spY,spZ):
    #   Assemble the A matrix
    spX = np.array(spX)
    spY = np.array(spY)
    spZ = np.array(spZ)
    A = np.zeros((len(spX),4))
    A[:,0] = spX*2
    A[:,1] = spY*2
    A[:,2] = spZ*2
    A[:,3] = 1

    #   Assemble the f matrix
    f = np.zeros((len(spX),1))
    f[:,0] = (spX*spX) + (spY*spY) + (spZ*spZ)
    C, residules, rank, singval = np.linalg.lstsq(A,f,rcond=None)

    #   solve for the radius
    t = (C[0]*C[0])+(C[1]*C[1])+(C[2]*C[2])+C[3]
    radius = math.sqrt(t)

    return radius, C[0], C[1], C[2]


ply_file_path = "../ProjectTest/360_net_44_AKAZE_FLOAT_v_1/outReconstruction/colorized.ply"
path_w1 = "../ProjectTest/360_net_44_AKAZE_FLOAT_v_1/outReconstruction/colorized_sub.ply"
path_w2 = "../ProjectTest/360_net_44_AKAZE_FLOAT_v_1/outReconstruction/colorized2.ply"

i = 0
count = 0
x =[]
y = []
z = []
r = []
g = []
b = []
cam_x =[]
cam_y = []
cam_z = []
header = []

ply_file = open(ply_file_path)
line = ply_file.readline()
while line:
    if(i <= 9):
         header.append(line)
    if(i > 9):  
        if(line[3] == '0' and line[4] == '255' and line[5] == '0'):
            cam_x.append(float(line[0]))
            cam_y.append(float(line[1]))
            cam_z.append(float(line[2]))
        else:
            x.append(float(line[0]))
            y.append(float(line[1]))
            z.append(float(line[2]))
            r.append(int(line[3]))
            g.append(int(line[4]))
            b.append(int(line[5]))        
              
    i = i + 1
    line = ply_file.readline().split()
ply_file.close()

#call_func
ret = sphereFit(cam_x, cam_y, cam_z)

vec_a = np.array([float(ret[1]), float(ret[2]), float(ret[3])])

text_file = open(path_w1, "wt")            
for i in range(len(x)):    
    vec_b = np.array([float(x[i]), float(y[i]), float(z[i])])
    distance = np.linalg.norm(vec_a - vec_b)
    if(distance < float(ret[0])):
        count = count + 1
        text_file.write(str(x[i]) + " " + str(y[i]) + " " + str(z[i]) + " " + str(r[i]) + " " + str(g[i]) + " " + str(b[i]) + '\n')
text_file.close()         

text_file = open(path_w2, "wt")   
for i in range(10):
    if(i == 0):
         text_file.write(header[i])
    elif(i == 2):
        text_file.write(header[i][0] + ' ' + header[i][1] + ' ' + str(count) + '\n')
    else:
         text_file.write(' '.join(header[i]) + '\n')
text_file.close() 

text_file = open(path_w1, "r")
data = text_file.read()
text_file.close() 

text_file = open(path_w2, "a")
text_file.write(data)
text_file.close() 

os.remove(path_w1)