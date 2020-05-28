import numpy as np
import os
from pyntcloud import PyntCloud
    
ply_file_path = "../ProjectTest/360_net_44_AKAZE_FLOAT_v_1_test/outReconstruction/colorized2.ply"
path_w1 = "../ProjectTest/360_net_44_AKAZE_FLOAT_v_1_test/outReconstruction/colorized_sub.ply"
path_w2 = "../ProjectTest/360_net_44_AKAZE_FLOAT_v_1_test/outReconstruction/colorized3.ply"

i = 0
count = 0
in_point_count = 0
threshold_distance = 0.3
threshold_point_count = 10

header = []

cloud = PyntCloud.from_file(ply_file_path)
point = cloud.points                     
  
text_file = open(path_w1, "wt")     
for i in range(len(point)):
    print(i)
    vec_a = np.array([point.at[i,'x'], point.at[i,'y'], point.at[i,'z']])
    in_point_count = 0
    for j in range(len(point)):
         vec_b = np.array([point.at[j,'x'], point.at[j,'y'], point.at[j,'z']])
         distance = np.linalg.norm(vec_a - vec_b)
         if(distance != 0.0 and distance < threshold_distance):
             in_point_count = in_point_count + 1
    if(in_point_count > threshold_point_count):
        count = count + 1
        text_file.write(str(point.at[i,'x']) + " " + str(point.at[i,'y']) + " " + str(point.at[i,'z']) + " " + str(point.at[i,'red']) + " " + str(point.at[i,'green']) + " " + str(point.at[i,'blue']) + '\n')
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
