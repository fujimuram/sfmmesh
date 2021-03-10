import numpy as np
import os
    
ply_file_path = "../ProjectTest/360_net_44_AKAZE_FLOAT_v_1/outReconstruction/colorized2.ply"
path_w1 = "../ProjectTest/360_net_44_AKAZE_FLOAT_v_1/outReconstruction/colorized_sub.ply"
path_w2 = "../ProjectTest/360_net_44_AKAZE_FLOAT_v_1/outReconstruction/colorized3.ply"

i = 0
count = 0
in_point_count = 0
threshold_distance = 0.3
threshold_point_count = 10
x =[]
y = []
z = []
r = []
g = []
b = []
header = []

ply_file = open(ply_file_path)
line = ply_file.readline()
while line:
    if(i <= 9):
         header.append(line)
    if(i > 9):  
        x.append(float(line[0]))
        y.append(float(line[1]))
        z.append(float(line[2]))
        r.append(int(line[3]))
        g.append(int(line[4]))
        b.append(int(line[5]))                         
    i = i + 1
    line = ply_file.readline().split()
ply_file.close()    
  
text_file = open(path_w1, "wt")     
for i in range(len(x)):
    print(i)
    vec_a = np.array([float(x[i]), float(y[i]), float(z[i])])
    in_point_count = 0
    for j in range(len(x)):
         vec_b = np.array([float(x[j]), float(y[j]), float(z[j])])
         distance = np.linalg.norm(vec_a - vec_b)
         if(distance != 0.0 and distance < threshold_distance):
             in_point_count = in_point_count + 1
    if(in_point_count > threshold_point_count):
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
