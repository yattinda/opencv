import cv2
import matplotlib .pyplot as plt

img = cv2.imread('image/Lenna.png',cv2.IMREAD_COLOR)

height = img.shape[0]
width = img.shape [1]

trim_img = img [150 : height, 150 : width]
cv2.imshow('trim_Lenna', trim_img)

cv2.waitKey(100000)
cv2.destroyAllWindows()
