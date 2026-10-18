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

sobelY = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
sobelY = cv2.normalize(sobelY, 
                dst = sobelY, 
                alpha = 0, 
                beta = 1, 
                norm_type = cv2.NORM_MINMAX, 
                dtype = cv2.CV_32F)

def carve(sobleY):
    seams = {}
    cost = {}
    for col in range(sobleY.shape[1]):
        seams[(0, col)] = -1
        cost[(0, col)] = sobleY[0][col]
    
    for row in range(0, sobleY.shape[0]):
        for col in range(sobleY.shape[1]):
            left = right = None
            if col != 0:
                left = sobleY[row+1][col-1]
            if col != sobleY.shape[1]-1:
                right = sobleY[row+1][col+1]
            middle = sobleY[row+1][col]
            
            if middle <= (left+right)//2:
                cost[(row+1, col+1)]
            
carve(sobelY)