from Adafruit_BME280 import *
import time
import w1_temp 

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
#temp_sensor = W1_TEMP()

#sensor = BME280(mode=BME280_OSAMPLE_8)

# Altitude in meters to calculate sea-level pressure OG = 879 ft = 268 m
altitude = 268

w1_degrees = w1_temp.read_temp_c()
degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
# Adjust pressure to sea level
hectopascals = hectopascals*(1-(0.0065 * altitude)/(w1_degrees + 0.0065 * altitude + 273.15))**(-5.257)
humidity = sensor.read_humidity()
timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

print 'Timestamp = %s'%timestamp + ', Temp = {0:0.3f} deg C'.format(degrees) + ', Pressure = {0:0.2f} hPa'.format(hectopascals) + ', Humidity = {0:0.2f} %'.format(humidity) + ', w1_temp = {0:0.3f} deg C'.format(w1_degrees) 

import sqlite3
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
# Running this script by cron messes up the relative path

try:
    db = sqlite3.connect(os.path.join(dir_path, '../raspi-weather.db'))
    c = db.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS indoor(
        `id`            INTEGER PRIMARY KEY AUTOINCREMENT,
        `timestamp`     DATETIME,
        `temperature`   NUMERIC,
        `humidity`      NUMERIC,
        `pressure`      NUMERIC,
	`w1temp`	NUMERIC)""")
    db.commit()

    args = [timestamp, round(degrees, 2), round(humidity, 2), round(hectopascals, 2), round(w1_degrees, 2 )]
    c.execute('INSERT INTO indoor (timestamp, temperature, humidity, pressure, w1temp) VALUES (?, ?, ?, ?, ?)', args)
    db.commit()
    db.close()
except sqlite3.Error as err:
    f = open(os.path.join(dir_path, 'logger.log'), 'a')
    print(str(err))
    f.write(str(err))
    f.write('\n')
    f.close()

