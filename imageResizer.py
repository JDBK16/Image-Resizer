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


sobelXY = cv2.Sobel(image, cv2.CV_64F, 1, 1, ksize=5)
sobelXY = cv2.normalize(sobelXY, 
                dst = sobelXY, 
                alpha = 0, 
                beta = 1, 
                norm_type = cv2.NORM_MINMAX, 
                dtype = cv2.CV_32F)
show_image(sobelXY)

def remove(image, pixels, axis):
    if axis == 0:
        new_image = []
        for row, i in enumerate(pixels):
            for col in i:
                new_row = np.delete(image[row], col, axis=0)
                new_image.append(new_row)
    
    return np.stack(new_image, axis=0)

def mark_red(image, pixels, axis):
    if axis == 0:
        red = image.copy()
        for row, i in enumerate(pixels):
            for col in i:
                red[row][col] = [0, 0, 255]
    
    return red

def shallowest(gray, pixels, n, axis):
    if axis == 0:
        mins = []
        for row, col in enumerate(pixels):
            gap = gray[row][col[0]:col[-1]]
            dif = min_dif = abs(gap[0] - gap[1])
            min_pos = pixels[row][0]
            for i in range(len(gap)):
                dif = abs(gap[i] - gap[i-1])
                if i < len(gap) - 1:
                    dif += abs(gap[i] - gap[i+1])
                    dif = dif // 2
                if dif < min_dif:
                    min_dif = dif
                    min_pos = pixels[row][i]
            mins.append([min_pos])
    return mins

def main(sobelx, image, gray):
    row_gaps = []
    for row in range(sobelx.shape[0]):
        gaps = []
        gap = []
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
        
    mins = shallowest(gray, row_gaps, 10, 0)
        
    return remove(image, mins, 0), mark_red(image, mins, 0), mark_red(image, row_gaps, 0)

for i in range(0, 1):
    result, red, gaps = main(sobelx, image, gray)
    image = result.copy()
    gaussian = cv2.GaussianBlur(image, (15, 15), 0)
    gray = cv2.cvtColor(gaussian, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
    
cv2.imwrite("images/result.png", result)
cv2.imwrite("images/red.png", red)
cv2.imwrite("images/gaps.png", gaps)
cv2.imwrite("images/sobel.png", sobelx)