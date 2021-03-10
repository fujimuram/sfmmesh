import cv2
from time import sleep

image = cv2.imread("./images/100_7104.JPG", 1)
img_depth = cv2.imread("./images/depth0004.png", 0)

result = cv2.bitwise_and(image, image, mask=img_depth) # 元画像とマスクを合成
cv2.imwrite('./images/depth_mask_image.jpg', result)
cv2.namedWindow("BGR_test1",cv2.WINDOW_NORMAL)
cv2.resizeWindow("BGR_test1",640,480)
cv2.imshow('BGR_test1', result)
sleep(1)

while True:
    # キー入力を1ms待って、keyが「q」だったらbreak
    key = cv2.waitKey(1)&0xff
    if key == ord('q'):
        break

cv2.destroyAllWindows()