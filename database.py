#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
import mysql.connector as mariadb
import logging
import flask
import time
from config import config
from config import config2
from datetime import datetime
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
   ph = request.args.get('ph', None)
   tds = request.args.get('tds', None)
   try: 
    cur.execute("INSERT INTO reading (TimeStamp,Humidity,Temp,Growth,ph,tds) VALUES (%s,%s,%s,%s,%s,%s)", (datetime.timestamp(datetime.now()),humidity,temp,growth,ph,tds))
   except mariadb.Error as e: 
    print(f"Error: {e}")

   conn.commit()
   return "Success" #need to update

# route to insert a new reading
@app.route('/hydro/inter/new', methods=['POST'])
def new_inter_reading():
   # connection for MariaDB
   conn = mariadb.connect(**config2)
   # create a connection cursor
   cur = conn.cursor()
   # execute a SQL statement 
   humidity  = request.args.get('humidity', None)
   temp = request.args.get('temp', None)
   ph = request.args.get('ph', None)
   tds = request.args.get('tds', None)
   try: 
    cur.execute("INSERT INTO inter (TimeStamp,Humidity,Temp,ph,tds) VALUES (%s,%s,%s,%s,%s)", (datetime.timestamp(datetime.now()),humidity,temp,ph,tds))
   except mariadb.Error as e: 
    print(f"Error: {e}")

   conn.commit()
   return "Success" #need to update


app.run(host='0.0.0.0')