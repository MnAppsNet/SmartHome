from urllib.request import DataHandler
from dataHandler import Data, DATA_KEY
import Adafruit_DHT as dht

'''
This script is for DHT22 temperature and humidity sensors.
'''

class Sensor():
    def __init__(self,sensorPin,dataHandler:Data = None):
        self._pin = sensorPin
        self._data = dataHandler

    def readData(self):
        self.humidity,self.temperature = dht.read_retry(dht.DHT22, self._pin)
        if self._data != None:
            self._data.setValue(DATA_KEY.currentTemperature,self.temperature)
            self._data.setValue(DATA_KEY.currentHumidity,self.humidity)
        return self.humidity,self.temperature

    def getHumidity(self):
        return self.humidity

    def getTemperature(self):
        return self.temperature