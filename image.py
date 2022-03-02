import cv2
import numpy as np
#read the image and covert to gray scale

def convert_gray(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image