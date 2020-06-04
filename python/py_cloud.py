from pyntcloud import PyntCloud
#cloud = PyntCloud.from_file("ply/scene_dense.ply")
cloud = PyntCloud.from_file("ply/scene_dense_mesh_2.ply")
point = cloud.points
print(len(point)) #点群数
print(len(point.columns)) #点当たりの要素数
drop_point = point.index[(point['red']<10) & (point['green']<10) & (point['blue']<10)]
point.drop(drop_point, inplace=True)
print(point)
cloud.to_file("ply/out.ply")
#print(point.at[0,'y'] , point.at[1,'x'])#任意要素の値取得



