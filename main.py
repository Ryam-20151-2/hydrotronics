# This is the main file of the hydrotronics project.
# Running this Python file on the PI will cause the project to run
# May look at making a compiled binary of final version
import comm
import time
import serial
#import measure_height

def main():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        new_data = comm.read_from_serial(ser)
        if(len(new_data) > 0):
            #measure_height.  ##call measure height and return actual value
            new_data.append("15")
            response = comm.write_new_post(new_data)
            print(response)
        else:
            print("No Data")
        time.sleep(1)

if __name__ == "__main__":
    main()