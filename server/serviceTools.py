import time
from os import environ

class SERVICE_STATUS:
    Active = 'active'
    Inactive = 'inactive'

def getLastUpdateTimeText():
    #Set time zone
    environ['TZ'] = 'Europe/Athens'
    try:
        time.tzset()
    except:
        pass #System is not UNIX
    return "Last update: {0}".format(time.strftime("%H:%M:%S"))

def getTemperatureText(temperature):
    return "Temperature: {0:0.1f}".format(temperature)

def getHumidityText(humidity):
    return "Humidity: {0:0.1f}".format(humidity)