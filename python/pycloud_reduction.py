#KDTreeを用いて最近傍点を探索し、削除する
from pyntcloud import PyntCloud
import scipy.spatial as ss
edge_cloud = PyntCloud.from_file("./mask_ply/edge.ply")
normal_cloud = PyntCloud.from_file("./mask_ply/scene_dense.ply")
edge_point = edge_cloud.points
normal_point = normal_cloud.points

drop_list = []
coords_edge_point = edge_point.drop(['red', 'green', 'blue'], axis=1)
coords_normal_point = normal_point.drop(['red', 'green', 'blue'], axis=1)

for j in range(len(coords_edge_point)):
    tree = ss.KDTree(coords_normal_point.values, leafsize=10000)
    d, i = tree.query(coords_edge_point.values[j])
    print(d, i, j)
    drop_list.append(i)

drop_list_n = list(set(drop_list))

print(drop_list_n)

normal_point.drop(drop_list, inplace=True)

normal_cloud.to_file("mask_ply/scene_dense_out.ply")




#print(len(point)) #点群数
#print(len(point.columns)) #点当たりの要素数
#drop_point = point.index[(point['red']>150) | (point['green']>150) | (point['blue']>150)]#取り除きたい色
#point.drop(drop_point, inplace=True)

#cloud.to_file("ply/wall_mesh_scene_dense_out.ply")
#print(point.at[0,'y'] , point.at[1,'x'])#任意要素の値取得



