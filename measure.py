#!/usr/bin/python

#import measure_height
import os, os.path
from picamera2 import Picamera2
from time import sleep
import comm

camera = Picamera2()
camera_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
camera.configure(camera_config)
camera.start_preview()
growth = 0
green_per = 0
def determine_target_tds(elapsed_time):
    get_photo()
    
    growth = max((elasped_time/24192),green_per,height/2)
    if growth > 80 and elapsed_time < (2419200*0.8):
        growth = elasped_time/24192 # accoounting for error

    if growth > 80:
        comm.write_to_serial("1.7 \n")
    elif growth > 40:
        comm.write_to_serial("1.7 \n")
    return growth

def get_photo():
    # Camera warm-up time
    camera.start()
    sleep(5)
    camera.capture_file('../photos/temp.jpg')
    green_per, height = measure_plant('../photos/temp.jpg')
    manage_files()

def manage_files():
    onlyfiles = next(os.walk("../photos"))[2]
    os.rename('../photos/temp.jpg', '../photos/photo_'+str(len(onlyfiles))+'.jpg')


determine_target_tds(1000)