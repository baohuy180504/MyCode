import cv2
import numpy as np


def nothing(x):
    pass
cv2.namedWindow("AdjustBar")
cv2.createTrackbar("H", "AdjustBar", 0, 179, nothing)
cv2.createTrackbar("S", "AdjustBar", 255, 255, nothing)
cv2.createTrackbar("V", "AdjustBar", 255, 255, nothing)

img_hsv = np.zeros((250, 500, 3), np.uint8)

while True:
    h = cv2.getTrackbarPos("H", "AdjustBar")
    s = cv2.getTrackbarPos("S", "AdjustBar")
    v = cv2.getTrackbarPos("V", "AdjustBar")

    img_hsv[:] = (h, s, v)
    img_bgr = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    cv2.imshow("AdjustBar", img_bgr)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cv2.destroyAllWindows()