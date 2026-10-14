import numpy as np
import cv2
import sys
import os

image_name = sys.argv[1]
filepath = "./images"
if image_name in os.listdir(filepath):
    image = cv2.imread(filepath + "/" + image_name, cv2.IMREAD_COLOR)

def show_image(image):
    cv2.imshow('image',image)
    cv2.waitKey(0)

def horizontal_pixels(image):
    pixels = []
    

current_size = list(image.shape[:2])
print("Current Size:    ", current_size[0], "x", current_size[1])
expected_size = [int(sys.argv[2]), int(sys.argv[3])]
print("Expected Size:   ", expected_size[0], "x", expected_size[1])

if expected_size[0] > current_size[0] or expected_size[1] > current_size[1]:
    print("Expected Size Must Be Smaller Than Current Size")
    sys.exit()

while expected_size[0] < current_size[0] or expected_size[1] < current_size[1]:
    hz = vt = None
    if expected_size[0] < current_size[0]:
        hz = horizontal_pixels(image)
    if expected_size[0] < current_size[1]:
        vt = vertical_pixels(image)