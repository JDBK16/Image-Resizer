import numpy as np
import cv2
import sys
import os
import copy

image_name = sys.argv[1]
filepath = "./images"
if image_name in os.listdir(filepath):
    image = cv2.imread(filepath + "/" + image_name, cv2.IMREAD_COLOR)
else:
    sys.exit()


def show_image(image):
    cv2.imshow('image',image)
    cv2.waitKey(0)

def horizontal_pixels(laplacian):
    pixels = []
    for row in laplacian:
        min_pix = (0, row[0])
        for index, pixel in enumerate(row):
            if pixel < min_pix[1]:
                min_pix = (index, pixel)
        pixels.append(min_pix[0])

    return pixels

current_size = list(image.shape[:2])
print("Current Size:    ", current_size[0], "x", current_size[1])
expected_size = [int(sys.argv[2]), int(sys.argv[3])]
print("Expected Size:   ", expected_size[0], "x", expected_size[1])

if expected_size[0] > current_size[0] or expected_size[1] > current_size[1]:
    print("Expected Size Must Be Smaller Than Current Size")
    sys.exit()


while expected_size[0] < current_size[0] or expected_size[1] < current_size[1]:
    hz = vt = None
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

show_image(image)

    