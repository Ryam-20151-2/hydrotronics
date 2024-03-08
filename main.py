#!/usr/bin/python
# This is the main file of the hydrotronics project.
# Running this Python file on the PI will cause the project to run
# May look at making a compiled binary of final version
import comm
import measure
import time


def main():
    time_start = time.time()
    target_tds = 500
    growth = 10
    time.sleep(6)
    comm.write_to_serial(str(target_tds) + "\n")
    while True:
        new_data = comm.read_from_serial()
        if(len(new_data) > 0):
            balanced = new_data[4]
            new_data[4] = (str(growth))# to replace with above
            if (balanced == 1):
                target_tds, growth = measure.determine_target_tds(time_start-time.time())
                response = comm.write_new_post(new_data)
            else:
                response = comm.write_inter_reading(new_data)
            comm.write_to_serial(str(target_tds)+"\n")
            print(new_data)
            print(response)
        else:
            print("No Data")
        time.sleep(6)

if __name__ == "__main__":
    main()