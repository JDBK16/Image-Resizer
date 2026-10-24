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
    # If pixel already in minimum seam
    if pixel in seams:
        return seams
    
    # If pixel in bottom column i.e. end of seam
    if pixel[0] == image.shape[0] - 1:
        seams[pixel] = [sum(image[pixel[0]][pixel[1]]), None]
        return seams
    
    # Initialise next pixels in seam
    next_left = (pixel[0] + 1, pixel[1] - 1)
    next_middle = (pixel[0] + 1, pixel[1])
    next_right = (pixel[0] + 1, pixel[1] + 1)
    
    # Calculate next pixels in seam
    if next_left[1] >= 0:
        seams = find_seam(image, seams, next_left)
    seams = find_seam(image, seams, next_middle)
    if next_right[1] < image.shape[1]:
        seams = find_seam(image, seams, next_right)
        
    # Choose best path
    options = [next_left, next_right]
    best = next_middle
    for option in options:
        if option[1] >= 0 and option[1] < image.shape[1]:
            if seams[best][0] > seams[option][0]:
                best = option
                
    seams[pixel] = [sum(image[pixel[0]][pixel[1]]) + seams[best][0], best]    
    return seams

    
def carve(image):
    seams = {}
    seams = find_seam(image, seams, (0, image.shape[1]//2))
        
    return seams
        
seams = carve(sobelY)

max_cost = seams[max(seams, key=lambda k: seams[k][0])][0]

seam_image = image.copy()
print(image.shape)