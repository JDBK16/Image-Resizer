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

def find_seam(image, seams, pixel):
    if pixel[1] == image.shape[1]:
        seams[(pixel[0], pixel[1])] = [image[pixel[0]][pixel[1]], None]
        return seams, pixel
    seams, best = find_seam(image, seams, (pixel[0] + 1, pixel[1]))
    if pixel[1] > 0:
        seams, left = find_seam(image, seams, (pixel[0] + 1, pixel[1] - 1))
        if seams[left][0] < seams[best][0]:
            best = left
    if pixel[1] < image.shape[1]:
        seams, right = find_seam(image, seams, (pixel[0] + 1, pixel[1] + 1))
        if seams[right][0] < seams[best][0]:
            best = right
    return seams, best

    
def carve(image):
    seams = {}
    for col in range(0, image.shape[1]):
        cost = image[0, col]
        seams, next = find_seam(image, seams, (0, col))
        seams[(0, col)] = [cost + seams[next][0], seams[next][1]]
        
    return seams
        
print("hi")
seams = carve(sobelY)
print(seams)