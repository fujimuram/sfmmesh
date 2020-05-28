from pyntcloud import PyntCloud
#cloud = PyntCloud.from_file("ply/scene_dense.ply")
cloud = PyntCloud.from_file("ply/colorized3.ply")
point = cloud.points
print(len(point)) #点群数
print(len(point.columns)) #点当たりの要素数
print(point.at[0,'y'] , point.at[1,'x'])#任意要素の値取得



