import sys
import os
import cv2
import numpy as np
from matplotlib.pyplot import imshow

def rawcount(filename):
    with open(filename) as f:
        return sum(1 for _ in f)

def progress(now, count):
    size = 20 * now / count
    sys.stdout.write("Sharpening: [{0}] {1:.2f}%\r".format("#" * size + " " * (20 - size), 100. * now / count))
    sys.stdout.flush()

def sharpen_filter(image):
    img = cv2.imread(image)

    kernel = np.array([[-1,-1,-1,-1,-1],
                        [-1,2,2,2,-1],
                        [-1,2,8,2,-1],
                        [-1,2,2,2,-1],
                        [-1,-1,-1,-1,-1]]) / 8.0
    output = cv2.filter2D(img, -1, kernel)

    os.remove(image)
    cv2.imwrite(image, output)

def sharpen_deblur(image):
    img = cv2.imread(image)

    output = cv2.GaussianBlur(img, (0, 0), 25)
    output = cv2.addWeighted(img, 1.75, output, -0.75, 0)

    os.remove(image)
    cv2.imwrite(image, output)

count = rawcount(sys.argv[1])

i = 0
f = open(sys.argv[1], "r")

while True:
    line = f.readline()
    if not line: break
    sharpen_filter(line[:-1])
    i+=1
    progress(i, count)

f.close()
print ""
