#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
import mysql.connector as mariadb
import logging
import flask
import json
import time
from config import config

logging.basicConfig(filename='api.log',level=logging.DEBUG)

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# route to return entries by field
@app.route('/hydro/data/<reading_id>', methods=['GET'])
def get_all_values(reading_id):
   # connection for MariaDB
   conn = mariadb.connect(**config)
   # create a connection cursor
   cur = conn.cursor()
   # execute a SQL statement
   cur.execute("SELECT "+reading_id+" FROM reading")
   
   return_data=[]
   for data in cur:
       return_data.append(data)
   return return_data

# route to return data for an entry
@app.route('/hydro/reading/<reading_id>', methods=['GET'])
def get_reading(reading_id):
   # connection for MariaDB
   conn = mariadb.connect(**config)
   # create a connection cursor
   cur = conn.cursor()
   # execute a SQL statement
   cur.execute("SELECT * FROM reading WHERE readingID = "+reading_id)
   
   return_data=[]
   for data in cur:
       return_data.append(data)
   return return_data

# route to insert a new reading
@app.route('/hydro/reading/new', methods=['POST'])
def new_reading():
   # connection for MariaDB
   conn = mariadb.connect(**config)
   # create a connection cursor
   cur = conn.cursor()
   # execute a SQL statement 
   humidity  = request.args.get('humidity', None)
   temp = request.args.get('temp', None)
   growth = request.args.get('growth', None)
   try: 
    cur.execute("INSERT INTO reading (TimeStamp,Humidity,TempSensor1,GrowthStatus) VALUES (%s,%s,%s,%s)", (time.strftime("%c"),humidity,temp,growth))
   except mariadb.Error as e: 
    print(f"Error: {e}")

   conn.commit()
   return "Success" #need to update

app.run(host='0.0.0.0')