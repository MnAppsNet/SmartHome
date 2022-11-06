from handlers.dataHandler import Data, DATA_KEY
try:
    import Adafruit_DHT as dht
except:
    dht = None #For testing purposes
'''
This script is for DHT22 temperature and humidity sensors.
'''

class Sensor():
    def __init__(self,sensorPin,dataHandler:Data = None):
        self._pin = sensorPin
        self._data = dataHandler

    def readData(self):
        if dht != None:
            self.humidity,self.temperature = dht.read_retry(dht.DHT22, self._pin)
        else:
            self.humidity = 0
            self.temperature = 0
        if self._data != None:
            self._data.setValue(DATA_KEY.currentTemperature,self.temperature)
            self._data.setValue(DATA_KEY.currentHumidity,self.humidity)
        return self.humidity,self.temperature

    def getHumidity(self):
        return self.humidity

    def getTemperature(self):
        return self.temperature