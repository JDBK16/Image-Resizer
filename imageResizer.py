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
    

red = image.copy()
for row, col in enumerate(row_gaps):
    for i in col:
        red[row][i] = [0, 0, 255]

            
show_image(red) 
        