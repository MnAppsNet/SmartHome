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
        if primarySensorPin == None:
            primarySensorPin = Constants.SENSOR_PIN
        self._sensors = self._data.getValue(DATA_KEY.sensors)
        if (self._sensors == None ): self._sensors = {}
        if (not self._sensors):
            self._sensors = {
                primarySensorPin:{
                    DATA_KEY.SENSORS.ip:False,
                    DATA_KEY.SENSORS.name:"Main"
                }
            }
            self._data.setValue(DATA_KEY.sensors, self._sensors)

    def CheckIPSensor(sensor):
        response = requests.get(sensor)
        if (DATA_KEY.SENSORS.temperature in response or DATA_KEY.SENSORS.humidity in response):
            return True
        else: return False

    def updateSensorReadings(self):
        for sensor in self._sensors:
            self.readData(sensor)
        self._data.setValue(DATA_KEY.sensors, self._sensors)

    def readData(self,sensor=-1):
        humidity = 0
        temperature = 0
        if (sensor==-1): sensor = data.getValue(DATA_KEY.primarySensor)
        if (sensor==None): sensor = Constants.SENSOR_PIN

        if (DATA_KEY.SENSORS.humidityOffset not in self._sensors[sensor]):
            self._sensors[sensor][DATA_KEY.SENSORS.humidityOffset] = 0
        if (DATA_KEY.SENSORS.temperatureOffset not in self._sensors[sensor]):
            self._sensors[sensor][DATA_KEY.SENSORS.temperatureOffset] = 0
        if (DATA_KEY.SENSORS.ip not in self._sensors[sensor]):
            self._sensors[sensor][DATA_KEY.SENSORS.ip] = bool('.' in sensor)
        if (DATA_KEY.SENSORS.temperature not in self._sensors[sensor]):
            self._sensors[sensor][DATA_KEY.SENSORS.temperature] = 0
        if (DATA_KEY.SENSORS.humidity not in self._sensors[sensor]):
            self._sensors[sensor][DATA_KEY.SENSORS.humidity] = 0
        if (DATA_KEY.SENSORS.name not in self._sensors[sensor]):
            self._sensors[sensor][DATA_KEY.SENSORS.name] = "Unnamed"

        if (not self._sensors[sensor][DATA_KEY.SENSORS.ip]): #PIN sensor
            if dht != None:
                humidity,temperature = dht.read_retry(dht.DHT22, sensor)
        else: #IP sensor
            response = requests.get(sensor)
            if (DATA_KEY.SENSORS.temperature in response): temperature = response[DATA_KEY.SENSORS.temperature]
            if (DATA_KEY.SENSORS.humidity in response): humidity = response[DATA_KEY.SENSORS.humidity]

        #Apply offsets
        humidity += self._sensors[sensor][DATA_KEY.SENSORS.humidityOffset]
        temperature += self._sensors[sensor][DATA_KEY.SENSORS.temperatureOffset]

        if self._data != None:
            if sensor == self._data.getValue(DATA_KEY.primarySensor):
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