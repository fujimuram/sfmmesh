import cv2
from glob import glob

IMAGE_PATH = "./images/human"

for file in glob(IMAGE_PATH + '/*.jpg'):
    img = cv2.imread(file)
    img_mask = cv2.Canny(img, 30, 200, apertureSize = 3) # マスクを作成
    result = cv2.bitwise_and(img, img, mask=img_mask) # 元画像とマスクを合成
    rename_file = file.replace("images", "outLineImages")
    print(rename_file)
    cv2.imwrite(rename_file, result)
