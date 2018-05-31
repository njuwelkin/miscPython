import cv2
import numpy as np
import sys

img=cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)


cv2.namedWindow("img", 1)

base = 5.0
for i in range(0, 20):
    a = (base + i) / base
    newImg = np.uint8(np.clip((img - 127.0) * a + 127, 0, 255))
    print a
    cv2.imshow("img", cv2.resize(newImg, (512, 512)))
    k = cv2.waitKey(0)
    if k == 13:
        print "asdfasdfkalkj"
        cv2.imwrite("./contrast.jpg" , newImg)

cv2.destroyAllWindows()
