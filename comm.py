# This file contains the Raspberry Pi side of the communication protocol
#!/usr/bin/env python3
import serial
import time
import requests
api_url = "http://192.168.0.146:5000"
post_endpoint = '/hydro/reading/new'

def read_from_serial(ser):
    data_arr = []
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        data_arr = line.split(':')
    return data_arr

def write_new_post(data_arr):
    data = "?humidity="+data_arr[0]+"&temp="+data_arr[1]+"&ph="+data_arr[2]+"&tds="+data_arr[3]+"&growth="+data_arr[4]
    response = requests.post(api_url+post_endpoint+data)
    return response

def write_to_serial(data_in,ser):
    ser.write(data_in)
