import cv2
import matplotlib .pyplot as plt

re_length = 500
img = cv2.imread('image/test.jpg',cv2.IMREAD_COLOR)
h, w = img.shape[:2]
re_h = re_w = re_length / max(h,w)
resize_img = cv2.resize(img, dsize=None, fx=re_h , fy=re_w)
cv2.imshow('test', resize_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
