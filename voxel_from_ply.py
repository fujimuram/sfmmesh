import open3d as o3d

voxel_size = 0.0008
pcd = o3d.io.read_point_cloud("./voxel_reduction_ply/scene_dense4_reduction2.ply")
voxel = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size)
print(len(o3d.geometry.VoxelGrid.get_voxels(voxel)))
o3d.io.write_voxel_grid("./voxel_reduction_ply/scene_dense_reduction_voxel_%f_4_2.ply" % voxel_size, voxel, True)
