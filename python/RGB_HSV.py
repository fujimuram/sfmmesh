import cv2
import numpy as np


# 入力画像の読み込み
img = cv2.imread("./images/net_model/CIMG3404.jpg")
print(img)
# 方法2(OpenCVで実装)       
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
print("hsv")
print(hsv)    

# 結果を出力
cv2.imwrite("./images/hsv.jpg", hsv)

