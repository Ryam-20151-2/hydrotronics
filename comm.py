# This file contains the Raspberry Pi side of the communication protocol
#!/usr/bin/env python3
import serial
import time
import requests
api_url = "http://127.0.0.1:5000"
post_endpoint = '/hydro/reading/new'
inter_endpoint = '/hydro/inter/new'

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()
def read_from_serial():
    data_arr = []
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        data_arr = line.split(':')
    return data_arr

def write_new_post(data_arr):
    data = "?humidity="+data_arr[0]+"&temp="+data_arr[1]+"&ph="+data_arr[2]+"&tds="+data_arr[3]+"&growth="+data_arr[4]
    response = requests.post(api_url+post_endpoint+data)
    return response

def write_to_serial(data_in):
    b = bytes(data_in, 'utf-8')
    ser.write(b)

def write_inter_reading(data_arr):
    data = "?humidity="+data_arr[0]+"&temp="+data_arr[1]+"&ph="+data_arr[2]+"&tds="+data_arr[3]
    response = requests.post(api_url+inter_endpoint+data)
    return response