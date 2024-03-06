#!/usr/bin/python
import measure_height
from picamera import PiCamera
from time import sleep
target_tds = 500
def determine_target_tds(elapsed_time):
    get_photo()
    if elapsed_time > 1814400:
        target_tds = 600 #subjet to change
    elif elapsed_time > 1209600:
        target_tds = 550 #subjet to change
    elif elapsed_time > 604800:
        target_tds = 500 #subjet to change
    else:
        target_tds = 500 #subjet to change
    return target_tds

def get_photo():
    #I love camera