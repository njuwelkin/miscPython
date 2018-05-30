import cv2
import math
from math import sin, cos, pi
import numpy as np
from scipy import sparse
import random
import time
from datetime import datetime
import sys
import os

class Lines(object):
    def __init__(self, Nodes):
        self.mat = np.zeros((Nodes, Nodes), dtype="bool")
        self._updated = True
        self.mask = ~ np.tril(np.ones((Nodes, Nodes), dtype="bool"))

    def append(self, (i, j)):
        if self.mat[i, j]:
            return False
        self.mat[i, j] = True
        self._updated = True
        return True

    def getCoo(self):
        if not self._updated:
            self._coo = sparse.coo_matrix(self.mat & Lines.mask)
            self._updated = False
        return self._coo

class Engine(object):
    def __init__(self, Nodes=128, VLen=64, CanvasSize=2048, DeclineFactor=1.0):
        self.Nodes = Nodes
        self.VLen = VLen
        R = VLen / 2
        self.R = R
        self.Anchors = [(R-int(cos(i*2*pi/Nodes)*R+0.5), R+int(sin(i*2*pi/Nodes)*R+0.5)) for i in range(0, Nodes)]

        self.CanvasSize = CanvasSize
        CanvasR = CanvasSize/2
        self.CanvasR = CanvasR
        self.CanvasAnchors = [(CanvasR-int(cos(i*2*pi/Nodes)*CanvasR+0.5), CanvasR+int(sin(i*2*pi/Nodes)*CanvasR+0.5)) for i in range(0, Nodes)]

        self.w = self.round_mask()
        self.DeclineFactor = DeclineFactor

    def round_mask(self):
        VLen, R = self.VLen, self.R

        w = np.zeros((VLen, VLen), dtype="uint8")
        center = (R, R)
        for i in range(0, VLen):
            for j in range(0, VLen):
                d = R - math.sqrt((i - center[0])**2 + (j - center[1])**2)
                t = 1 if d > 0 else 0
                w[i, j] = t
        return w

    def run(self, portrait):
        Nodes, VLen, R, Anchors = self.Nodes, self.VLen, self.R, self.Anchors
        CanvasSize, CanvasR, CanvasAnchors = self.CanvasSize, self.CanvasR, self.CanvasAnchors

        img = self.w * cv2.resize(portrait, (VLen, VLen))
        canvas = np.ones((CanvasSize, CanvasSize), dtype="uint8") *255

        lines = Lines(Nodes)
        color = int(256*VLen*self.DeclineFactor / CanvasSize)

        edge = 0
        linesD = np.ones((Nodes, Nodes), dtype="uint64") * (256 * VLen)
        canvas = np.ones((2048, 2048), dtype="uint8") *255

        while True:
            print "Edges: %s, at %s" % (edge, datetime.now())

            x0 = img.sum()
            dx = 0
            for i in range(0, Nodes):
                for j in range(i+1, Nodes):
                    if lines.mat[i, j]:
                        continue
                    if dx > linesD[i, j]:
                        continue
                    tmp = img.copy()
                    cv2.line(tmp, Anchors[i], Anchors[j], 255, 1)
                    x1 = tmp.sum()
                    d = x1 - x0
                    linesD[i, j] = d
                    if d > dx:
                        i0, j0 = i, j
                        dx = d
            print "	", dx, i0, j0
            mask = np.zeros((VLen, VLen), dtype="uint8")
            cv2.line(mask, Anchors[i0], Anchors[j0], 1, 1)
            coo = sparse.coo_matrix(mask)
            for i, j in zip(coo.row, coo.col):
                p = img[i, j]
                img[i, j] = 255 if (255-color < p) else p+color
            lines.append((i0, j0))

            cv2.line(canvas, CanvasAnchors[i0], CanvasAnchors[j0], 0, 1)
            edge += 1
            if edge % 50 == 0:
                filename = "VLen%s_DeclineFactor%s_%s" % (VLen, self.DeclineFactor, edge)
                np.save("./output/%s.npy" % filename, lines.mat)

                cv2.imwrite("./output/%s.jpg" % filename, canvas)

            if edge > 1800:
                break

            if DEBUG and edge % 10 == 0:
                cv2.imshow("img", cv2.resize(canvas, (800, 800)))
                cv2.waitKey(30)

def getSettings(argv):
    assert len(argv) > 1

    VLen, DeclineFactor, Nodes = 128, 1.0, 128
    if len(argv) > 4:
        Nodes = int(argv[4])
    if len(argv) > 3:
        DeclineFactor = float(argv[3])
    if len(argv) > 2:
        VLen = int(argv[2])
    path = argv[1]
    return path, VLen, DeclineFactor, Nodes

DEBUG = True
if __name__ == '__main__':
    if not os.path.exists("./output"):
        os.mkdir("output")

    argv = sys.argv
    path, VLen, DeclineFactor, Nodes = getSettings(argv)
    print path, VLen, DeclineFactor, Nodes

    portrait = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    engine = Engine(Nodes=Nodes, VLen=VLen, DeclineFactor=DeclineFactor)

    if DEBUG:
        cv2.namedWindow("img", 1)

    engine.run(portrait)

    if DEBUG:
        cv2.destroyAllWindows()



