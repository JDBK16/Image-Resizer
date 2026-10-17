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


def show_image(image):
    cv2.imshow('image',image)
    cv2.waitKey(0)

current_size = list(image.shape[:2])
print("Current Size:    ", current_size[0], "x", current_size[1])
expected_size = [int(sys.argv[2]), int(sys.argv[3])]
print("Expected Size:   ", expected_size[0], "x", expected_size[1])

if expected_size[0] > current_size[0] or expected_size[1] > current_size[1]:
    print("Expected Size Must Be Smaller Than Current Size")
    sys.exit()
    
def least_important_pixels(laplacian, n, axis):
    if axis == 1:
        print("Horizontal: Remove,", n)
        pixels = []
        for row in laplacian:
            remove = []
            for index, pixel in enumerate(row):
                left = row[max(0, index-1)]
                right = row[min(len(row) - 1, index + 1)]
                difference = abs(pixel - left) + abs(pixel - right)
                if len(remove) < n:
                    remove.append([index, difference])
                else:
                    dif = -1
                    pos = -1
                    for i in range(len(remove)):
                        if remove[i][1] > difference and remove[i][1] < dif:
                            dif = remove[i][1]
                            pos = i
                    if dif != -1:
                        remove[pos] = [index, difference]
                pixels.append([i[0] for i in remove])
    return pixels
                
def mark_pixels(image, horizontal_pixels):
    for row in range(image.shape[1]):
        for i in horizontal_pixels[row]:
            image[row][i] == [0, 0, 255]
    return image      
                        
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)
horizontal_pixels = least_important_pixels(laplacian, current_size[1] - expected_size[1], 1)
print(len(horizontal_pixels))
marked = mark_pixels(image, horizontal_pixels)



while True == False:
    hz = vt = bt = None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)
    current_size = list(image.shape[:2])
    if expected_size[1] < current_size[1]:
        hz = horizontal_pixels(laplacian)
        image = np.array([
            np.delete(row, pixel, axis=0)
            for row, pixel in zip(image, hz)
        ])

    current_size = list(image.shape)
    print(expected_size, current_size)

show_image(marked)

    