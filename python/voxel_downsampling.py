import open3d as o3d
import numpy as np

pcd = o3d.io.read_point_cloud("./voxel_reduction_ply/scene_dense.ply")
downpcd = pcd.voxel_down_sample(voxel_size=0.001)
downpcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
#print(pcd)
print(downpcd)
#print(np.asarray(pcd.points))
print(np.asarray(downpcd.points))
#o3d.visualization.draw_geometries([pcd])
o3d.visualization.draw_geometries([downpcd])
o3d.io.write_point_cloud("./mask_ply/scene_dense_reduction_down.ply", downpcd)