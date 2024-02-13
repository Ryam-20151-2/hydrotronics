import cv2
import os
import time
from picamera2 import PiCamera
from matplotlib import pyplot as plt

camera = PiCamera()
def measure_growth():
    get_image(12)
    measure_height()

def measure_height():
    # Opening image
    img = cv2.imread("~/capstone/photos/image_latest.jpg")
    #cv2.imshow("this",img)
    # OpenCV opens images as BRG 
    # but we want it as RGB We'll 
    # also need a grayscale version
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    
    # Use minSize because for not 
    # bothering with extra-small 
    # dots that would look like STOP signs

    stop_data = cv2.CascadeClassifier('H:/UNI stuff/4a4b/capstone/code-proj/capstone-lettuce/cascade_old.xml')

    found = stop_data.detectMultiScale(img_gray, 
                                    minSize =(200, 200))
    
    # Don't do anything if there's 
    # no sign
    amount_found = len(found)
    
    if amount_found != 0:
        
        # There may be more than one
        # sign in the image
        for (x, y, width, height) in found:
            
            # We draw a green rectangle around
            # every recognized sign
            cv2.rectangle(img_rgb, (x, y), 
                        (x + height, y + width), 
                        (0, 255, 0), 20)
            
    # Creates the environment of 
    # the picture and shows it
    #plt.subplot(1, 1, 1)
    plt.imshow(img_rgb)
    plt.show()


def get_image():
    os.rename('~/capstone/photos/image_latest.jpg','~/capstone/photos/growth_photo_'+ time.time() +'.jpg')
    camera.capture('~/capstone/photos/image_latest.jpg')
    