#結び目探索(6角形網):targetは探索範囲に戻さない
#端点から5近傍(Y字になっていない）に対して補正線を引き、なす角が最も大きくなるベクトル1つを採用する(point_array2でループ)
#探索して先頭に出てくる近傍点は探索点自身

import numpy as np
import open3d as o3d
from scipy import spatial

work_dir = "thinning0"

pcd = o3d.io.read_point_cloud("./" + work_dir + "/thin_avg.ply")
point_array = np.asarray(pcd.points)
point_array = sorted(point_array, key=lambda x:(x[1], x[0]))
point_array2 = point_array
tree = spatial.cKDTree(point_array)

points = []
lines = []
new_points = []
deg_list = []
i = 0
max_deg = 0
accept_index = 0
c = 1
N = 10.0 #距離しきい値(復元対象のスケールに合わせて変更が必要)

for j in range(len(point_array)):
    target = point_array[0]
    point_array = np.delete(point_array, 0, axis=0)
    tree = spatial.cKDTree(point_array)     
    distance, index = tree.query(target)
    points.append(target.tolist())
    
    #1近傍
    if(distance<N):
        points.append(point_array[index].tolist())
        lines.append([i, i+c])
        c = c + 1
    
    print(point_array.shape)
    i = i + c
    c = 1


#端点からの補正線
tree = spatial.cKDTree(point_array2)
c = 1
cnt = len(points)
flag = False
for n, k in enumerate(point_array2):
    k = k.tolist()
    if(points.count(k) == 1):
        even_odd = points.index(k)
        if(even_odd % 2 == 1):#奇数
            p = points[even_odd-1]
            vec1 = np.array([k[0]-p[0], k[1]-p[1], k[2]-p[2]])   
        else:#偶数
            p = points[even_odd+1]
            vec1 = np.array([p[0]-k[0], p[1]-k[1], p[2]-k[2]])
            
        distance, index = tree.query(k,5)
        print("---------------------------------------------------------------------------------------------")
        print(" target: #", n, k, "\n", "distance:", distance, "\n", "index:", index, "\n")
        
        for a in range(len(index)):
            p = point_array2[index[a]]
            vec2 = np.array([p[0]-k[0], p[1]-k[1], p[2]-k[2]])
            inner = np.inner(vec1, vec2)
            norm = np.linalg.norm(vec1) * np.linalg.norm((vec2))
            cos = inner / norm
            deg = np.rad2deg(np.arccos(np.clip(cos, -1.0, 1.0)))
            deg_list.append(deg)
            if(points.count(point_array2[index[a]].tolist()) == 2):
                if(deg > max_deg and distance[a] < N and deg > 100):
                    max_deg = deg
                    accept_index = index[a]
                    flag = True
        
        print(deg_list)    
        if(flag == True):
            print(" Line Connect Success :", k, "<----->", point_array2[accept_index], max_deg)
            print("---------------------------------------------------------------------------------------------")
            points.append(k)
            points.append(point_array2[accept_index].tolist())
            lines.append([cnt, cnt+c])
            c = c + 1
            cnt = cnt + c
            flag = False
        else: print(" Line Connect Failure")
              
        c = 1
        max_deg = 0
        accept_index = 0
        deg_list = []


#重複削除と網の交点抽出
for k in points:
    if(points.count(k) == 3 and not(k in new_points)):
        new_points.append(k)

       
line_set = o3d.geometry.LineSet(
    points=o3d.utility.Vector3dVector(points),
    lines=o3d.utility.Vector2iVector(lines),
)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(new_points)
o3d.io.write_point_cloud("./" + work_dir + "/new_points.ply", pcd, write_ascii = True)
o3d.visualization.draw_geometries([line_set])


