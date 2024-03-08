#!/usr/bin/python

#import measure_height
import os, os.path
from picamera import PiCamera
from time import sleep

# camera = PiCamera()
# camera.resolution = (1024, 768)
# camera.start_preview()
target_tds = 500
growth = 10
def determine_target_tds(elapsed_time):
    #get_photo()
    if elapsed_time > 1814400:
        target_tds = 600 #subject to change
    elif elapsed_time > 1209600:
        target_tds = 550 #subject to change
    elif elapsed_time > 604800:
        target_tds = 500 #subject to change
    else:
        target_tds = 500 #subject to change
    return target_tds, growth

def get_photo():
    # Camera warm-up time
    sleep(2)
    camera.capture('temp.jpg')
    manage_files()

def manage_files():
    onlyfiles = next(os.walk("../photos"))[2]
    print (len(onlyfiles))
    os.rename('../photos/temp.jpg', '../photos/photo_'+str(len(onlyfiles))+'.jpg')