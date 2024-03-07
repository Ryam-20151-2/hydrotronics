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
    "SELECT MAX(TimeStamp) FROM reading"
    )

    return_data=[]
    for data in cur:
        return_data.append(data)
    cur.execute(
    "SELECT tds, TimeStamp FROM inter WHERE TimeStamp BETWEEN "+str(return_data[0][0])+" AND "+str(datetime.timestamp(datetime.now())))
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
    plt.show()

def plot_ph():
       # connection for MariaDB
    conn = mariadb.connect(**config2)
    # create a connection cursor
    cur = conn.cursor()
    # execute a SQL statement
    cur.execute(
    "SELECT MAX(TimeStamp) FROM reading"
    )

    return_data=[]
    for data in cur:
        return_data.append(data)
    cur.execute(
    "SELECT ph, TimeStamp FROM inter WHERE TimeStamp BETWEEN "+str(return_data[0][0])+" AND "+str(datetime.timestamp(datetime.now())))
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
    plt.show()

plot_tds()
plot_ph()
