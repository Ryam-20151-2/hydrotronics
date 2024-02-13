# This is the main file of the hydrotronics project.
# Running this Python file on the PI will cause the project to run
# May look at making a compiled binary of final version
import comm
import time
import serial
import measure_height
time_start = time.time()
def main():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        new_data = comm.read_from_serial(ser)
        if(len(new_data) > 0):
            #growth = measure_height.measure_growth()
            #new_data.append(growth)
            
            new_data.append("15") # to replace with above
            
            response = comm.write_new_post(new_data)
            print(response)

            #comm.write_to_serial(new_data[4], ser)
        else:
            print("No Data")
        time.sleep(1)

if __name__ == "__main__":
    main()