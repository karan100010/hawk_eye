#using opencv to read image and drwaing Contour and bounding box extracting each image bounding box as a new image
#and saving it in a folder spliting image name and extension
import cv2
import numpy as np
import os
import sys

def image_to_box(image):
    image=cv2.imread(image)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret,thresh=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    contours,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        s=cv2.contourArea(cnt)
        if s>1000:
            save=image.copy()
            x,y,w,h=cv2.boundingRect(cnt)
            cv2.rectangle(save,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.imwrite(os.path.splitext(image)[0]+"_"+str(s)+".jpg",save)
        
                





   