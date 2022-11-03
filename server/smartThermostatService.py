import serviceTools as tools
from displayController import Display
from sensorController import Sensor
from thermostatController import Thermostat
from dataHandler import Data, DATA_KEY
from time import sleep, strftime, localtime
from httpHandler import Server

#Constants :
THERMOSTAT_PIN = 11
SENSOR_PIN = 4
SAVE_EVERY = 2 #Loops. after these amount of loops, the data will be hard saved

#Instances of all our handlers :
data = Data()
server = Server(dataHandler=data)
display = Display(data.getValue(DATA_KEY.font))
sensor = Sensor(SENSOR_PIN)
thermostat = Thermostat(THERMOSTAT_PIN,data)

try:
    count = 1
    while True:
        humidity,temperature = sensor.readData()
        thermostat.checkState(temperature)
        lastUpdateText = tools.getLastUpdateTimeText()
        humidityText = tools.getLastUpdateTimeText(humidity)
        temperatureText = tools.getLastUpdateTimeText(temperature)
        display.writeText(lastUpdateText,8)
        display.writeText(temperatureText,12)
        display.writeText(humidityText,14)
        display.flush()
        sleep(data.getValue(DATA_KEY.refreshRate))
        server.serviceStatus = tools.SERVICE_STATUS.Active
        if count >= SAVE_EVERY:
            count = 1
            data.save()
except KeyboardInterrupt:
        print("Smart thermostat service stopped by the user...")
except Exception as e:
        print(e)
server.stop()
server.serviceStatus = tools.SERVICE_STATUS.Inactive