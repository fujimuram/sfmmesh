import cv2
from glob import glob

IMAGE_PATH = "./images"
OUT_IMAGE_PATH = "./outLineImage"

for file in glob(IMAGE_PATH + '/*.jpg'):
    img = cv2.imread(file)
    img_mask = cv2.Canny(img, 30, 200, apertureSize = 3) # マスクを作成
    result = cv2.bitwise_and(img, img, mask=img_mask) # 元画像とマスクを合成
    cv2.imwrite(file, result)
