import numpy as np
import open3d as o3d

input_path="./mesh/"
output_path="./mesh/"
dataname="scene_dense_reduction_voxel_0.003_normals.ply"
point_cloud= np.loadtxt(input_path+dataname,skiprows=14)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(point_cloud[:,:3])
pcd.normals = o3d.utility.Vector3dVector(point_cloud[:,3:6])
pcd.colors = o3d.utility.Vector3dVector(point_cloud[:,6:9]/255)

distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 3 * avg_dist

#BPA
bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2]))

'''
dec_mesh = bpa_mesh.simplify_quadric_decimation(100000)
dec_mesh.remove_degenerate_triangles()
dec_mesh.remove_duplicated_triangles()
dec_mesh.remove_duplicated_vertices()
dec_mesh.remove_non_manifold_edges()
'''

'''
#ポアソン(布で包み込むようにメッシュ化する。網模型には向かない。)
poisson_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=13, width=0, scale=1.1, linear_fit=False)[0]
bbox = pcd.get_axis_aligned_bounding_box()
p_mesh_crop = poisson_mesh.crop(bbox)
'''



o3d.io.write_triangle_mesh(output_path+"bpa_mesh_0.003.ply", bpa_mesh, write_ascii = True, print_progress = True)
#o3d.io.write_triangle_mesh(output_path+"p_mesh_c_0.003.ply", p_mesh_crop, write_ascii = True, print_progress = True)
