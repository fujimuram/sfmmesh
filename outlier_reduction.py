import open3d as o3d


def display_inlier_outlier(cloud, ind):
    inlier_cloud = cloud.select_down_sample(ind)
    outlier_cloud = cloud.select_down_sample(ind, invert=True)

    print("Showing outliers (red) and inliers (gray): ")
    outlier_cloud.paint_uniform_color([1, 0, 0])
    inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])


if __name__ == "__main__":
    # (1) Load a ply point cloud, print it, and render it
    print("Load a ply point cloud, print it, and render it")
    pcd = o3d.io.read_point_cloud("./voxel_reduction_ply/scene_dense_reduction_voxel_0.005.ply")
    o3d.visualization.draw_geometries([pcd])
    # (2) Downsample the point cloud with a voxel
    print("Downsample the point cloud with a voxel of 0.02")
    voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.02)
    o3d.visualization.draw_geometries([voxel_down_pcd])
    # (3) Every 5th points are selected
    print("Every 5th points are selected")
    uni_down_pcd = pcd.uniform_down_sample(every_k_points=5)
    o3d.visualization.draw_geometries([uni_down_pcd])
    # (4) Statistical oulier removal
    print("Statistical oulier removal")
    cl, ind = voxel_down_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    display_inlier_outlier(voxel_down_pcd, ind)
    # (5) Radius oulier removal
    print("Radius oulier removal")
    cl, ind = voxel_down_pcd.remove_radius_outlier(nb_points=16, radius=0.05)
    display_inlier_outlier(voxel_down_pcd, ind)

