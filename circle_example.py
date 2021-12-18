import cv2
import numpy as np

def find_circle(cv2_img, param, last_len):
  gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
  retval, bw = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
  bw_floodfill = bw.copy()

  h, w = bw.shape[:2]
  mask = np.zeros((h+2, w+2), np.uint8)

  cv2.floodFill(bw_floodfill, mask, (0,0), 255);
  bw_floodfill_inv = cv2.bitwise_not(bw_floodfill)
  kernel = np.ones((15, 15), np.uint8)
  dilation_img = cv2.dilate(bw_floodfill_inv, kernel, iterations=1)
  while(1):
    print(last_len, param)
    print(type(gray))
    circles = cv2.HoughCircles(dilation_img, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=100, param2=param, minRadius=0, maxRadius=0)
    if isinstance(circles, np.ndarray):
      if len(circles[0]) == 1:
        circles = np.uint16(np.around(circles))
        break
      elif len(circles[0]) > 1:
        last_len = len(circles[0])
        param += 1
    else:
      if last_len > 1:
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=100, param2=param-1, minRadius=0, maxRadius=0)
        circles = np.uint16(np.around(circles))
        break
      else:
        last_len = 0
        param -= 1
  print(circles[0])
  return circles[0]

if __name__ == '__main__':
  img_name = "circlewood.jpg"

  img = cv2.imread("./image/" + img_name)

  circles = find_circle(img, 50, 0)

  for circle in circles:
    # 円周を描画する
    cv2.circle(img, (circle[0], circle[1]), circle[2], (0, 165, 255), 5)
    # 中心点を描画する
    cv2.circle(img, (circle[0], circle[1]), 2, (0, 0, 255), 3)

  cv2.imwrite("./treatmentedImage/result_" + img_name, img)
