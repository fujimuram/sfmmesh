
#重心平均化による点群の簡素化
import open3d as o3d
import numpy as np
from scipy import spatial
#pcd = o3d.io.read_point_cloud("./voxel_reduction_ply/scene_dense_reduction_voxel_0.001000_4_2.ply")
pcd = o3d.io.read_point_cloud("./voxel_reduction_ply/thin_avg_1.ply")
point_array = np.asarray(pcd.points)
point_array = np.asarray(sorted(point_array, key=lambda x:(x[1], x[0])))

drop_list = []
point_avg = []
last_point = []

print(point_array.shape)

while len(point_array) != 0:
    tree = spatial.cKDTree(point_array)
    drop_list = tree.query_ball_point(point_array[0], r=1)#rは復元対象のスケールに合わせて変更が必要
    
    if(len(drop_list) == 1):
        last_point.append(point_array[0])
    else:
        for j in drop_list:
            point_avg.append(point_array[j])
        last_point.append(np.mean(point_avg, axis=0, dtype='int64'))    
       
    point_array = np.delete(point_array, drop_list, axis=0)      
    print(point_array.shape)
    point_avg = []
    drop_list = []
    
pcd_last = o3d.geometry.PointCloud()
pcd_last.points = o3d.utility.Vector3dVector(last_point)
o3d.io.write_point_cloud("./voxel_reduction_ply/thin_avg.ply", pcd_last, write_ascii = True)

