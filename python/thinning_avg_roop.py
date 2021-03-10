#重心平均化による点群の簡素化
import open3d as o3d
import numpy as np
from scipy import spatial
pcd = o3d.io.read_point_cloud("./thinning_test_roop/scene_dense_reduction_voxel_0.001000_4_2.ply")
#pcd = o3d.io.read_point_cloud("./thinning_test_roop/test.ply")
point_array = np.asarray(pcd.points)
point_array = np.asarray(sorted(point_array, key=lambda x:(x[1], x[0])))

drop_list = []
point_avg = []
last_point = []
target = []
pointcloud = []
color = []
pcd_complete = o3d.geometry.PointCloud()
pcd_last = o3d.geometry.PointCloud()
pcd_drop = o3d.geometry.PointCloud()
pcd_array = o3d.geometry.PointCloud()
pcd_target = o3d.geometry.PointCloud()

print(point_array.shape)
c = 0

while len(point_array) != 0:
    tree = spatial.cKDTree(point_array)
    target.append(point_array[0])
    drop_list = tree.query_ball_point(point_array[0], r=3)#rは復元対象のスケールに合わせて変更が必要
    
    if(len(drop_list) < 4):    
        for j in drop_list:
            point_avg.append(point_array[j])
    else:
        for j in drop_list:
            point_avg.append(point_array[j])
        last_point.append(np.mean(point_avg, axis=0, dtype='int64'))    
       
    point_array = np.delete(point_array, drop_list, axis=0)      
    print(point_array.shape)

    
    pcd_last.points = o3d.utility.Vector3dVector(last_point)
    pcd_drop.points = o3d.utility.Vector3dVector(point_avg)
    pcd_array.points = o3d.utility.Vector3dVector(point_array)
    pcd_target.points = o3d.utility.Vector3dVector(target)
    
    pcd_last.paint_uniform_color([1, 0, 0])#赤
    pcd_drop.paint_uniform_color([0, 0, 1])#青
    pcd_array.paint_uniform_color([1, 1, 1])#白
    pcd_target.paint_uniform_color([0, 1, 0])#緑
    
    pointcloud.extend(np.asarray(pcd_last.points))
    pointcloud.extend(np.asarray(pcd_drop.points))
    pointcloud.extend(np.asarray(pcd_array.points))
    pointcloud.extend(np.asarray(pcd_target.points))
    
    color.extend(np.asarray(pcd_last.colors))
    color.extend(np.asarray(pcd_drop.colors))
    color.extend(np.asarray(pcd_array.colors))
    color.extend(np.asarray(pcd_target.colors))
    
    pcd_complete.points = o3d.utility.Vector3dVector(pointcloud)
    pcd_complete.colors = o3d.utility.Vector3dVector(color)
    
    
    o3d.io.write_point_cloud("./thinning_test_roop/thin_avg%d.ply" % c, pcd_complete, write_ascii = True)
    

    drop_list = []
    point_avg = []
    target = []
    pointcloud = []
    color = []
    c = c + 1