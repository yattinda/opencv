import cv2
import numpy as np
import math

def adjust(img, alpha=1.0, beta=0.0):
    dst = alpha * img + beta
    return np.clip(dst, 0, 255).astype(np.uint8)

def accuracy_area(area, circumference):
    area = int(area)
    circumference = int(circumference)
    #area, circumferenceはピクセル数のため真円を元に補正値を掛ける
    correction_value = 1.257
    accuracy = correction_value * ((4 * np.pi * area) / (circumference ** 2))
    accuracy = np.tanh(accuracy - 1)
    accuracy = 1 + accuracy if accuracy < 0 else 1 - accuracy
    return accuracy

def accuracy_aspect(width, height):
    ratio = (height / width) if height > width else (width / height)
    #np.tanh(ratio - 1) は0 < x < 1(小さいほど真円に近い)
    ratio = 1 - np.tanh(ratio - 1)
    return ratio

def accuracy_rad(radius, s_side):
    s_side = s_side / 2
    rad_ratio = (radius / s_side) if radius > s_side else (s_side / radius)
    rad_ratio = 1 - np.tanh(rad_ratio - 1)
    return rad_ratio

def detect_contour(image_path):
    src = cv2.imread(image_path, cv2.IMREAD_COLOR)
    re_length = 800
    h, w = src.shape[:2]
    re_h = re_w = re_length / max(h,w)
    resize_src = cv2.resize(src, dsize=None, fx=re_h , fy=re_w)
    dst = adjust(resize_src, alpha=1.1, beta=0.0)
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    #2値化
    retval, bw = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
    bw_floodfill = bw.copy()
    h, w = bw.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(bw_floodfill, mask, (0,0), 255)
    bw_floodfill_inv = cv2.bitwise_not(bw_floodfill)
    kernel = np.ones((15, 15), np.uint8)
    dilation_img = cv2.dilate(bw_floodfill_inv, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.fillPoly(dilation_img, contours, 255)

    area = 0
    circumference = 0
    width = 0
    height = 0
    radius = 0

    for cnt in contours:
        #円周と面積
        tmp_area = cv2.contourArea(cnt)
        tmp_circumference = cv2.arcLength(cnt, True)
        if area < tmp_area:
            area = tmp_area
        if circumference < tmp_circumference:
            circumference = tmp_circumference
        #縦横比
        rect = cv2.minAreaRect(cnt)
        (cx, cy), (tmp_width, tmp_height), angle = rect
        if width < tmp_width:
            width = tmp_width
        if height < tmp_height:
            height = tmp_height
        #外接円
        center, tmp_radius = cv2.minEnclosingCircle(cnt)
        if radius < tmp_radius:
            radius = tmp_radius

    if area or circumference or width or height or radius != 0:
        s_side = width if width > height else height
        min_accuracy = min(accuracy_aspect(width, height),  accuracy_area(area, circumference), accuracy_rad(radius, s_side))
        max_accuracy = max(accuracy_aspect(width, height),  accuracy_area(area, circumference), accuracy_rad(radius, s_side))
        sum_accuracy = accuracy_aspect(width, height) + accuracy_area(area, circumference) + accuracy_rad(radius, s_side)
        mid_accuracy = sum_accuracy - max_accuracy - min_accuracy

        accuracy = min_accuracy

        if mid_accuracy > 0.98:
            accuracy = mid_accuracy
        elif max_accuracy - min_accuracy > 0.30 and min_accuracy < 0.5 or sum_accuracy <= 1.8:
            accuracy = sum_accuracy / 3
    else:
        accuracy = 0

    print(accuracy_aspect(width, height))
    print(accuracy_area(area, circumference))
    print(accuracy_rad(radius, s_side))
    print("#######################")
    print(accuracy)
    cv2.imshow("bw", bw)
    cv2.imshow("dst", dst)
    # cv2.imshow("Inverted Floodfilled Image", bw_floodfill_inv)
    cv2.imshow("dilation_img", dilation_img)
    cv2.waitKey(0)

if __name__ == '__main__':
  detect_contour('image/circle2.jpg')
