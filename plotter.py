#!/usr/bin/python
import matplotlib.pyplot as plt
from config import config2
from datetime import datetime
import mysql.connector as mariadb
def plot_tds():
    
    # connection for MariaDB
    conn = mariadb.connect(**config2)
    # create a connection cursor
    cur = conn.cursor()
    # execute a SQL statement
    

    cur.execute(
    "SELECT TimeStamp FROM reading ORDER BY TimeStamp DESC LIMIT "+str(int(num)+1)
    )

    return_data=[]
    for data in cur:
        return_data.append(data)
    for count in range(0,len(return_data)-1):
        print(return_data)
        print(return_data[int(num) - count -1][0])
        print(return_data[int(num) - count -2][0])
        cur.execute(
        "SELECT tds, TimeStamp FROM inter WHERE TimeStamp BETWEEN "+str(return_data[int(num) - count -1][0])+" AND "+str(return_data[int(num) - count-2][0]))
        values=[]
        times=[]
        for data in cur:
            values.append(data[0])
            times.append(int(float(data[1])))
        new_times = []
        for data in times:
            new_times.append( data - times[0])
        print(values)
        print(new_times)
        plt.plot(new_times,values)
        plt.title("TDS Settling Time From "+str(return_data[int(num) - count -1][0])+" and "+str(return_data[int(num) - count-2][0]))
        plt.xlabel("Time (s)")
        plt.ylabel("TDS Value")
        plt.show()

def plot_ph():
       # connection for MariaDB
    conn = mariadb.connect(**config2)
    # create a connection cursor
    cur = conn.cursor()
    # execute a SQL statement
    cur.execute(
    "SELECT TimeStamp FROM reading ORDER BY TimeStamp DESC LIMIT "+str(int(num)+1)
    )

    return_data=[]
    for data in cur:
        return_data.append(data)
    for count in range(0,len(return_data)-1):
        cur.execute(
        "SELECT ph, TimeStamp FROM inter WHERE TimeStamp BETWEEN "+str(str(return_data[int(num) - count -1][0])+" AND "+str(return_data[int(num) - count-2][0]))
        )
        values=[]
        times=[]
        for data in cur:
            values.append(data[0])
            times.append(int(float(data[1])))
        new_times = []
        for data in times:
            new_times.append( data - times[0])
        print(values)
        print(new_times)
        plt.plot(new_times,values)
        plt.title("PH Settling Time From "+str(return_data[int(num) - count -1][0])+" and "+str(return_data[int(num) - count-2][0]))
        plt.xlabel("Time (s)")
        plt.ylabel("PH Value")
        plt.show()

num = input("How many recent graphs would you like?")
plot_tds()
plot_ph()
