import sys
import cv2
import numpy as np
import math

VLen = 128

def gen_weight():
    w = np.zeros((VLen, VLen), dtype="float64")
    VLen_f = float(VLen)
    center = (VLen_f/2-0.5, VLen_f/2-0.5)
    for i in range(0, VLen):
        for j in range(0, VLen):
            #t = math.sqrt(math.fabs(VLen_f/2 - math.sqrt((i - center[0])**2 + (j - center[1])**2)))
            d = VLen_f/2 - math.sqrt((i - center[0])**2 + (j - center[1])**2)
            t = d if d > 0 else 0
            t = math.sqrt(math.sqrt(t))
            w[i, j] = t
    return w.reshape(VLen*VLen)

def vect2(p):
    res = cv2.resize(p, (VLen, VLen)).reshape(VLen*VLen)
    return (1.0*res)

def vect4(p):
    v2 = vect2(p)
    avg = v2.sum() / v2.size
    return v2 - avg

def cos(a, b):
    #w = gen_weight()
    #a *= w
    #b *= w
    return math.sqrt((sum(a*b) ** 2) / (sum(a**2) * sum(b**2)))

if __name__ == '__main__':
    argv = sys.argv
    assert len(argv) == 3
    path1 = argv[1]
    path2 = argv[2]

    p1 = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
    p2 = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)


    print cos(vect4(p1), vect4(p2))


