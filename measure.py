#!/usr/bin/python

#import measure_height
import os, os.path
from picamera2 import Picamera2
from time import sleep

camera = Picamera2()
camera_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
camera.configure(camera_config)
camera.start_preview()
target_tds = 500
growth = 0
def determine_target_tds(elapsed_time):
    get_photo()
    if elapsed_time > 1814400:
        target_tds = 600 #subject to change
        growth = 80
    elif elapsed_time > 1209600:
        target_tds = 550 #subject to change
        growth = 60
    elif elapsed_time > 604800:
        growth = 40
        target_tds = 500 #subject to change
    else:
        growth = 20
        target_tds = 500 #subject to change
    return target_tds, growth

def get_photo():
    # Camera warm-up time
    camera.start()
    sleep(2)
    camera.capture_file('../photos/temp.jpg')
    manage_files()

def manage_files():
    onlyfiles = next(os.walk("../photos"))[2]
    os.rename('../photos/temp.jpg', '../photos/photo_'+str(len(onlyfiles))+'.jpg')
