import cv2
import numpy as np

def detect_contour(image_path):
    re_length = 800

    src = cv2.imread(image_path, cv2.IMREAD_COLOR)
    h, w = src.shape[:2]
    re_h = re_w = re_length / max(h,w)
    resize_src = cv2.resize(src, dsize=None, fx=re_h , fy=re_w)
    gray = cv2.cvtColor(resize_src, cv2.COLOR_BGR2GRAY)
    #2値化
    retval, bw = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
    bw_floodfill = bw.copy()

    h, w = bw.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    cv2.floodFill(bw_floodfill, mask, (0,0), 255);
    bw_floodfill_inv = cv2.bitwise_not(bw_floodfill)
    kernel = np.ones((10, 10), np.uint8)
    dilation_img = cv2.dilate(bw_floodfill_inv, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.fillPoly(dilation_img, contours, 255)


    for cnt in contours:

        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        minenclosecircle = cv2.circle(dilation_img,center,radius,(0,255,0),2)
        print(radius)

    cv2.imshow("Inverted Floodfilled Image", bw_floodfill_inv)
    cv2.imshow("dilation_img", dilation_img)
    cv2.imshow("minenclosecircle", minenclosecircle)
    cv2.waitKey(0)



if __name__ == '__main__':
  detect_contour('image/circle2.jpg')
