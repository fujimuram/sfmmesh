import open3d as o3d
import numpy as np

pcd = o3d.io.read_point_cloud("./voxel_reduction_ply/scene_dense4_reduction2.ply")
point_array = np.asarray(pcd.points)
color_array = np.asarray(pcd.colors)
point_array2 = []
color_array2 = []

index = [i for i, x in enumerate(color_array) if x[0]<0.45 and x[1]<0.45 and x[2]<0.45]#0~1の色表現

for i in index:
    point_array2.append(point_array[i]) 
    color_array2.append(color_array[i]) 

pcd.points = o3d.utility.Vector3dVector(point_array2)
pcd.colors = o3d.utility.Vector3dVector(color_array2)

o3d.io.write_point_cloud("./voxel_reduction_ply/scene_dense4_reduction2_2.ply", pcd, write_ascii = True)

        