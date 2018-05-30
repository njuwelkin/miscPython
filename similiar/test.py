import cv2
import numpy as np

VLen = 128

def vect(p):
    res = cv2.resize(p, (VLen, VLen)).reshape(VLen*VLen)
    avg = res.sum() / res.size
    v = (res < avg)*2.0 - 1
    return v

def vect2(p):
    res = cv2.resize(p, (VLen, VLen)).reshape(VLen*VLen)
    return (1.0*res)

def vect3(p):
    return vect2(p) - 128

def vect4(p):
    v2 = vect2(p)
    avg = v2.sum() / v2.size
    return v2 - avg

def cos(a, b):
    return (sum(a*b) ** 2) / (sum(a**2) * sum(b**2)) 

p1 = cv2.imread('./p1.jpg', cv2.IMREAD_GRAYSCALE)
p2 = cv2.imread('./p2.jpg', cv2.IMREAD_GRAYSCALE)

pn = 256 - p1

print cos(vect(p1), vect(p2))
print cos(vect2(p1), vect2(p2))
print "v3, p1, p2:", cos(vect3(p1), vect3(p2))
print cos(vect2(p1), vect2(pn))
print cos(vect3(p1), vect3(pn))
print "v4, p1, p2:", cos(vect4(p1), vect4(p2))


print cos(vect2(256-p1), vect2(256-p2))
black = np.zeros((VLen, VLen), dtype="uint8")
black[0, 0] = 1
white = 256 * np.ones((VLen, VLen), dtype="uint8")
print cos(vect2(p1), vect2(black))
print cos(vect2(p1), vect2(white))
print cos(vect3(p1), vect3(black))
print cos(vect3(p1), vect3(white))



p3 = cv2.imread('./portrait.jpeg', cv2.IMREAD_GRAYSCALE)
img = np.array(vect2(p3).reshape((VLen, VLen)), dtype="uint8")

#cv2.namedWindow("img", 1)
#cv2.imshow("img", pn)
#cv2.waitKey(0)
#cv2.imshow("img", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
