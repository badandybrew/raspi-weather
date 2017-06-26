#!/usr/bin/python
import w1_temp
from Adafruit_BME280 import *

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

#sensor = BME280(mode=BME280_OSAMPLE_8)

# Altitude in meters to calculate sea-level pressure OG = 879 ft = 268 m
altitude = 268

try:
	w1_degrees = w1_temp.read_temp_c()
	temperature = sensor.read_temperature() 
	humidity = sensor.read_humidity()
	pascals = sensor.read_pressure()
    	hectopascals = pascals / 100
   	# Adjust pressure to sea level
   	hectopascals = hectopascals*(1-(0.0065 * altitude)/(w1_degrees + 0.0065 * altitude + 273.15))**(-5.257)
   	
	print '{0:0.1f} deg F\n{1:0.1f}% R.H.\n{2:0.1f} hPa\n{3:0.1f} deg F'.format(temperature*9/5 +32, humidity, hectopascals, w1_degrees*9/5 +32)
except RuntimeError as e:
   	print 'error\n{0}'.format(e)
except:
    	print 'error\nFailed to read sensor data'
