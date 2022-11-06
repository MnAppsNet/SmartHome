import traceback
from displayController import TemperatureAndHumidityScreen
from sensorController import Sensor
from thermostatController import Thermostat
from dataHandler import Data, DATA_KEY
from time import sleep
from server import Server

#Constants :
THERMOSTAT_PIN = 11
SENSOR_PIN = 4
SAVE_EVERY = 2 #Loops. after these amount of loops, the data will be hard saved

#Instances of all our handlers :
data = Data()
server = Server(dataHandler=data)
try:
        display = TemperatureAndHumidityScreen(data.getValue(DATA_KEY.font))
        sensor = Sensor(SENSOR_PIN)
        thermostat = Thermostat(THERMOSTAT_PIN,data)

        try:
                count = 1
                while True:
                        humidity,temperature = sensor.readData()
                        thermostat.checkState(temperature)
                        display.showData(humidity,temperature)
                        if data == None: break;
                        sleep(data.getValue(DATA_KEY.refreshRate))
                        if count >= SAVE_EVERY:
                                count = 1
                                data.save()
        except KeyboardInterrupt:
                print("Smart thermostat service stopped by the user...")
        server.stop()
except:
        print(traceback.format_exc())
        server.stop()