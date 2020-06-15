from pyntcloud import PyntCloud
#cloud = PyntCloud.from_file("ply/scene_dense.ply")
cloud = PyntCloud.from_file("ply/wall_mesh_scene_dense.ply")
point = cloud.points
print(len(point)) #点群数
print(len(point.columns)) #点当たりの要素数
drop_point = point.index[(point['red']>150) | (point['green']>150) | (point['blue']>150)]#取り除きたい色
point.drop(drop_point, inplace=True)
print(point)
cloud.to_file("ply/wall_mesh_scene_dense_out.ply")
#print(point.at[0,'y'] , point.at[1,'x'])#任意要素の値取得



