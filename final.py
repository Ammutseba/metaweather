import mysql.connector
from mysql.connector import errorcode
import datetime
import requests
import json

# Database connection
try:
    cnx = mysql.connector.connect(host="localhost", user='root', password='12345')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Wrong password")
    else:
        print(err)

#Table creation
cursor = cnx.cursor()
cursor.execute("CREATE DATABASE DEDOMENA")
cursor.execute("CREATE TABLE dedomena.kairos (location VARCHAR(50),date date, temperature float, forecast varchar(50), created varchar(80))")

#retrieve data
add = ("INSERT INTO dedomena.kairos"
       "(location, date, temperature, forecast, created) "
       "VALUES (%(location)s, %(date)s, %(temperature)s, %(forecast)s, %(created)s)")
cities = {
    'Barcelona': 753692,
    'Venice': 725746,
    'Athens': 946738,
}

for city, id in cities.items():
    for x in range(0,7):    #loop gia 7 meres
        date = datetime.datetime.now() + datetime.timedelta(days=x)
        place = requests.get("https://www.metaweather.com/api/location/{}/{}/{}/{}/".format(id, date.year, date.month, date.day))
        place_json = json.loads(place.text)
        for y in range(0,3):    #loop gia ta 3 teleytea forecasts tis imeras
            data = {
                'location': city,
                'date': place_json[y]["applicable_date"],
                'temperature': place_json[y]["the_temp"],
                'forecast': place_json[y]["weather_state_name"],
                'created': place_json[y]["created"],
            }
            cursor.execute(add, data)

cnx.commit()
cnx.close()