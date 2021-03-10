import open3d as o3d

pcd = o3d.io.read_point_cloud("./thinning4_2/thin_avg.ply")
pcd.paint_uniform_color([0, 0, 0])

o3d.visualization.draw_geometries([pcd])