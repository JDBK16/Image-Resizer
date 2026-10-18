import numpy as np
import cv2
import sys
import os

image_name = sys.argv[1]
filepath = "./images"
if image_name in os.listdir(filepath):
    image = cv2.imread(filepath + "/" + image_name, cv2.IMREAD_COLOR)
else:
    sys.exit()

current_size = list(image.shape[:2])
print("Current Size:    ", current_size[0], "x", current_size[1])
expected_size = [int(sys.argv[2]), int(sys.argv[3])]
print("Expected Size:   ", expected_size[0], "x", expected_size[1])

if expected_size[0] > current_size[0] or expected_size[1] > current_size[1]:
    print("Expected Size Must Be Smaller Than Current Size")
    sys.exit()
    
def show_image(image):
    cv2.imshow('image',image)
    cv2.waitKey(0)
    
gaussian = cv2.GaussianBlur(image, (15, 15), 0)
gray = cv2.cvtColor(gaussian, cv2.COLOR_BGR2GRAY)
sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)

show_image(sobelx)

row_gaps = []
for row in range(sobelx.shape[0]):
    gaps = []
    gap = []
    length = 1
    white = True
    for col in range(sobelx.shape[1]):
        if sobelx[row][col] > 0:
            if white == False:
                gaps.append(gap)
                gap = []
                white = True
        else:
            if white == True:
                white = False
            gap.append(col)
    if white == False:
        gaps.append(gap)
    row_gaps.append(max(gaps, key=len))
    
mins = []
for row in range(len(row_gaps)):
    pixels = gray[row][row_gaps[row][0]:row_gaps[row][-1]]
    dif = min_dif = abs(pixels[0] - pixels[1])
    min_pos = 0
    for i in range(1, len(pixels)):
        dif = abs(pixels[i] - pixels[i-1])
        if i < len(pixels) - 1:
            dif += abs(pixels[i] - pixels[i+1])
            dif = dif // 2
        if dif < min_dif:
            min_dif = dif
            min_pos = i
    mins.append(min_pos)
    
for row, col in enumerate(mins):
    image[row][col] = [0, 0, 255]


    
show_image(image)