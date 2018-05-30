import cv2
import numpy as np

img=cv2.imread("/Users/fuy3/Downloads/IMG_2463.heic", cv2.IMREAD_GRAYSCALE)


cv2.namedWindow("img", 1)

base = 5.0
for i in range(1, 20):
    a = (base + i) / base
    newImg = np.uint8(np.clip(img * a, 0, 255))
    print a
    cv2.imshow("img", cv2.resize(newImg, (512, 512)))
    k = cv2.waitKey(0)
    if k == 13:
        print "asdfasdfkalkj"
        cv2.imwrite("./contrast%s.jpg" % a, newImg)

cv2.destroyAllWindows()
