# This is the main file of the hydrotronics project.
# Running this Python file on the PI will cause the project to run
# May look at making a compiled binary of final version
import comm
import time
#import measure_height
time_start = time.time()
def main():
    time.sleep(6)
    comm.write_to_serial("500\n")
    while True:
        new_data = comm.read_from_serial()
        if(len(new_data) > 0):
            #growth = measure_height.measure_growth()
            #new_data.append(growth)
            
            new_data.append("500") # to replace with above
            print(new_data)
            response = comm.write_new_post(new_data)
            print(response)

            comm.write_to_serial(new_data[4]+"\n")
        else:
            print("No Data")
        time.sleep(6)

if __name__ == "__main__":
    main()