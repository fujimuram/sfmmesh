import numpy as np
import cv2

IMAGE_PATH = "./thinning4_2_hough/net2.png" # 読み込む画像

def main():
    image  = cv2.imread(IMAGE_PATH) # 画像読み込み
    image2 = cv2.imread(IMAGE_PATH) # 画像読み込み
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # グレースケール化
    outLineImage = cv2.Canny(gray, 120, 250, apertureSize = 3)   # 輪郭線抽出

    #cv2.imwrite("./thinning4_2_hough/outLine.png", outLineImage)    # ファイル保存

    hough_lines(image, outLineImage)     # ハフ変換による直線抽出
    cv2.imwrite("./thinning4_2_hough/result_hough.png", image)    # ファイル保存

    hough_lines_p(image2, outLineImage)   # 確率的ハフ変換による直線抽出
    cv2.imwrite("./thinning4_2_hough/result_houghP.png", image2)  # ファイル保存
    


# ハフ変換で直線を抽出する関数
def hough_lines(image, outLineImage):
    result = image
    lines = cv2.HoughLines(outLineImage, rho=1, theta=np.pi/180, threshold=245) # ハフ変換で直線抽出
    print("hough_lines: ", len(lines))

    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(result,(x1,y1),(x2,y2),(0,0,255),2) # 赤色で直線を引く

    return result


# 確率的ハフ変換で直線を抽出する関数
def hough_lines_p(image, outLineImage):
    resultP = image
    # 確率的ハフ変換で直線を抽出
    lines = cv2.HoughLinesP(outLineImage, rho=1, theta=np.pi/180, threshold=200, minLineLength=100, maxLineGap=70)
    print("hough_lines_p: ", len(lines))

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(resultP,(x1,y1),(x2,y2),(0,255,0),2) # 緑色で直線を引く

    return resultP


if __name__ == '__main__':
    main()

