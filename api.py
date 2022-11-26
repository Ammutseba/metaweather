import mysql.connector
from mysql.connector import errorcode
import flask
from flask import request, jsonify
import requests
import json

#initiating flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Database connection
try:
    cnx = mysql.connector.connect(host="localhost", user='root', password='12345')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Wrong password")
    else:
        print(err)
        
cursor = cnx.cursor()
query = (" SELECT LOCATION, DATE, temperature, FORECAST FROM DEDOMENA.KAIROS")
cursor.execute(query)

first_list = [] #first list contains three forecasts per day
for (location, date, temperature, forecast) in cursor:
    first_list.extend(list((location, date, temperature, forecast)))
    
second_list = [] #second list contains latest forecast per day
for i in range(0, len(first_list), 12):
    second_list.append(first_list[i])
    second_list.append(first_list[i+1])
    second_list.append(first_list[i+2])
    second_list.append(first_list[i+3])

third_list = [] #third list contains average temperature per day
for i in range(0, len(first_list), 12):
    third_list.append(first_list[i])
    third_list.append(first_list[i+1])
    third_list.append((first_list[i+2] + first_list[i+6] + first_list[i+10])/ 3)
    third_list.append(first_list[i+3])
    
@app.route('/', methods=['GET'])
def home():
    return jsonify(second_list) 
 
@app.route('/average_temp', methods=['GET'])
def forecasts():
    return jsonify(third_list) 
 
app.run()