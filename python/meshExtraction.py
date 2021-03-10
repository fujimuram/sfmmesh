import cv2
from glob import glob
import colorExtraction

IMAGE_PATH = "./images/netmodel_wall_10"

#色抽出
bgrLower = np.array([0, 0, 0])    # 抽出する色の下限
bgrUpper = np.array([120, 120, 120])    # 抽出する色の上限

for file in glob(IMAGE_PATH + '/*.jpg'):
    img = cv2.imread(file)
    bgrResult = bgrExtraction(img, bgrLower, bgrUpper)
    rename_file = file.replace("images", "outLineImages")
    print(rename_file)
    cv2.imwrite(rename_file, bgrResult)

 
#エッジ抽出    
'''    
for file in glob(IMAGE_PATH + '/*.jpg'):
    img = cv2.imread(file)
    img_mask = cv2.Canny(img, 30, 200, apertureSize = 3) # マスクを作成
    result = cv2.bitwise_and(img, img, mask=img_mask) # 元画像とマスクを合成
    rename_file = file.replace("images", "outLineImages")
    print(rename_file)
    cv2.imwrite(rename_file, result)
'''