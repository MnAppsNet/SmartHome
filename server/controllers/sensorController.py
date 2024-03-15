from handlers.dataHandler import Data, DATA_KEY
import requests
try:
    import Adafruit_DHT as dht
except:
    dht = None #For testing purposes
'''
This script is for DHT22 temperature and humidity sensors.
'''

class Sensor():
    def __init__(self,primarySensorPin,dataHandler:Data = None):
        self._data = dataHandler
        self._sensors = self._data.getValue(DATA_KEY.sensors)
        if (self._sensors == None):
            self._data.setValue(DATA_KEY.sensors, [{
                "pin":primarySensorPin
            }])
        elif (len(self._sensors) == 0):
            self._sensors.append({
                "pin":primarySensorPin
            })
            self._data.setValue(DATA_KEY.sensors, sensors)

    def updateSensorReadings(self):
        for i in range(0,len(self._sensors)):
            self.readData(i)
        self._data.setValue(DATA_KEY.sensors, self._sensors)
        pass

    def readData(self,sensor=0):
        humidity = 0
        temperature = 0
        if (DATA_KEY.SENSORS.pin in self._sensors[sensor]):
            if dht != None:
                humidity,temperature = dht.read_retry(dht.DHT22, self._sensors[sensor][DATA_KEY.SENSORS.pin])
        elif (DATA_KEY.SENSORS.ip in self._sensors[sensor]):
            response = requests.get(self._sensors[sensor][ip])
            if (DATA_KEY.SENSORS.temperature in response): temperature = response[DATA_KEY.SENSORS.temperature]
            if (DATA_KEY.SENSORS.humidity in response): humidity = response[DATA_KEY.SENSORS.humidity]
        if (DATA_KEY.SENSORS.humidityOffset in self._sensors[sensor]):
            try:
                humidity += self._sensors[sensor][DATA_KEY.SENSORS.humidityOffset]
            except: pass
        if (DATA_KEY.SENSORS.temperatureOffset in self._sensors[sensor]):
            try:
                humidity += self._sensors[sensor][DATA_KEY.SENSORS.temperatureOffset]
            except: pass
        if self._data != None and sensor == 0:
            #set current temperature from primary sensor
            self._data.setValue(DATA_KEY.currentTemperature,temperature)
            self._data.setValue(DATA_KEY.currentHumidity,humidity)
        self._sensors[sensor][DATA_KEY.SENSORS.temperature] = temperature
        self._sensors[sensor][DATA_KEY.SENSORS.humidity] = humidity
        return humidity,temperature

    def getHumidity(self,sensor = 0):
        return self._sensors[sensor][DATA_KEY.SENSORS.humidity]

    def getTemperature(self, sensor = 0):
        return self._sensors[sensor][DATA_KEY.SENSORS.temperature]