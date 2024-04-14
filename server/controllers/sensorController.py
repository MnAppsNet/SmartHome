from handlers.dataHandler import Data, DATA_KEY
import requests
try: #Support for DHT22 temperature sensor
    import Adafruit_DHT as dht
except:
    dht = None

class Sensor():
    def __init__(self,primarySensorPin,dataHandler:Data = None):
        self._data = dataHandler
        if primarySensorPin == None:
            primarySensorPin = Constants.SENSOR_PIN
        self._sensors = self._data.getValue(DATA_KEY.sensors)
        if (self._sensors == None ): self._sensors = {}
        if (not self._sensors):
            self._sensors = {
                str(primarySensorPin):{
                    DATA_KEY.SENSORS.ip:False,
                    DATA_KEY.SENSORS.name:"Main"
                }
            }
            self._data.setValue(DATA_KEY.sensors, self._sensors)

    def CheckIPSensor(sensor):
        if ('.' in sensor or ':' in sensor): 
            return True
        return False

    def updateSensorReadings(self):
        for sensor in self._sensors:
            self.readData(sensor)
        self._data.setValue(DATA_KEY.sensors, self._sensors)

    def readData(self,sensor=-1):
        humidity = 0
        temperature = 0
        if (sensor==-1): sensor = data.getValue(DATA_KEY.primarySensor)
        if (sensor==None): sensor = Constants.SENSOR_PIN
        sensor = str(sensor)

        if (DATA_KEY.SENSORS.humidityOffset not in self._sensors[sensor]):
            self._sensors[sensor][DATA_KEY.SENSORS.humidityOffset] = 0
        if (DATA_KEY.SENSORS.temperatureOffset not in self._sensors[sensor]):
            self._sensors[sensor][DATA_KEY.SENSORS.temperatureOffset] = 0
        if (DATA_KEY.SENSORS.ip not in self._sensors[sensor]):
            self._sensors[sensor][DATA_KEY.SENSORS.ip] = False
        if (DATA_KEY.SENSORS.temperature not in self._sensors[sensor]):
            self._sensors[sensor][DATA_KEY.SENSORS.temperature] = 0
        if (DATA_KEY.SENSORS.humidity not in self._sensors[sensor]):
            self._sensors[sensor][DATA_KEY.SENSORS.humidity] = 0
        if (DATA_KEY.SENSORS.name not in self._sensors[sensor]):
            self._sensors[sensor][DATA_KEY.SENSORS.name] = "Unnamed"

        self._sensors[sensor][DATA_KEY.SENSORS.ip] = Sensor.CheckIPSensor(sensor)
        if (not self._sensors[sensor][DATA_KEY.SENSORS.ip]): #PIN sensor
            if dht != None:
                try:
                    humidity,temperature = dht.read_retry(dht.DHT22, sensor)
                    self._sensors[sensor][DATA_KEY.SENSORS.offline] = False
                except:
                    self._sensors[sensor][DATA_KEY.SENSORS.offline] = True
        else: #IP sensor
            try:
                response = requests.get(sensor)
                json_resp = response.json()
                if (DATA_KEY.SENSORS.temperature in json_resp): temperature = float(json_resp[DATA_KEY.SENSORS.temperature])
                if (DATA_KEY.SENSORS.humidity in json_resp): humidity = float(json_resp[DATA_KEY.SENSORS.humidity])
                self._sensors[sensor][DATA_KEY.SENSORS.offline] = False
            except:
                self._sensors[sensor][DATA_KEY.SENSORS.offline] = True
                temperature = 0
                humidity = 0

        #Apply offsets
        humidity += float(self._sensors[sensor][DATA_KEY.SENSORS.humidityOffset])
        temperature += float(self._sensors[sensor][DATA_KEY.SENSORS.temperatureOffset])

        if self._data != None:
            if sensor == self._data.getValue(DATA_KEY.primarySensor):
                #set current temperature from primary sensor
                self._data.setValue(DATA_KEY.currentTemperature,temperature)
                self._data.setValue(DATA_KEY.currentHumidity,humidity)
        
        self._sensors[sensor][DATA_KEY.SENSORS.temperature] = temperature
        self._sensors[sensor][DATA_KEY.SENSORS.humidity] = humidity
        return humidity,temperature

    def getHumidity(self,sensor = 0):
        return self._sensors[str(sensor)][DATA_KEY.SENSORS.humidity]

    def getTemperature(self, sensor = 0):
        return self._sensors[str(sensor)][DATA_KEY.SENSORS.temperature]