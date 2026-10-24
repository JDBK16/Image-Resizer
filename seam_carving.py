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
    
def show_seam_and_carve(image1, image2):
    combined = np.concatenate((image1, image2), axis=1)
    cv2.imshow('Images side by side', combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def find_seam(image, seams, pixel):
    # If pixel already in minimum seam
    if pixel in seams:
        return seams
    
    # If pixel in bottom column i.e. end of seam
    if pixel[0] == image.shape[0] - 1:
        seams[pixel] = [image[pixel[0]][pixel[1]], None]
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
                
    seams[pixel] = [image[pixel[0]][pixel[1]] + seams[best][0], best]    
    return seams

    
def carve(image):
    seams = {}
    for col in range(image.shape[1]):
        seams = find_seam(image, seams, (0, col))
        
    return seams
        

def remove(image, seams, start):
    new_image = []
    current = start
    while current is not None:
        row, col = current

        new_row = np.delete(image[row], col, axis=0)
        new_image.append(new_row)

        current = seams[current][1]

    return np.stack(new_image, axis=0)

def paint_red(image, seams, start):
    current = start
    next = seams[current][1]
    while next != None:
        image[current[0], current[1]] = [0, 0, 255]
        current, next = next, seams[next][1]
    return image

def energy_map(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelX = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobelY = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    energy = np.sqrt(sobelX**2 + sobelY**2)
    energy = energy**2
    return energy

while image.shape[1] > expected_size[1]:
    energy = energy_map(image)
    seams = carve(energy)
    min_coord = min(
        (coord for coord in seams if coord[0] == 0),
        key=lambda coord: seams[coord][0]
    )
    red_seam_image = paint_red(image.copy(), seams, min_coord)
    cut_seam_image = remove(image, seams, min_coord)
    #show_seam_and_carve(red_seam_image, cut_seam_image)
    image = cut_seam_image
    print(image.shape[1], expected_size[1])

cv2.imwrite("images/result.png", cut_seam_image)
cv2.imwrite("images/red.png", red_seam_image)