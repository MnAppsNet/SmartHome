import traceback
from controllers.displayController import TemperatureAndHumidityScreen
from controllers.sensorController import Sensor
from controllers.thermostatController import Thermostat
from handlers.dataHandler import Data, DATA_KEY
from time import sleep
from const import Constants
import time
from server import Server

#Set time zone
try:
        time.environ['TZ'] = Constants.TIMEZONE
        time.tzset()
except:
        pass #System is not UNIX

#Instances of all our handlers :
data = Data()
server = Server(dataHandler=data)
try:
        display = TemperatureAndHumidityScreen(data.getValue(DATA_KEY.font))
        sensor = Sensor(Constants.SENSOR_PIN)
        thermostat = Thermostat(Constants.THERMOSTAT_PIN,data)

        try:
                count = 0
                while True:
                        humidity,temperature = sensor.readData()
                        thermostat.checkState(temperature)
                        display.showData(humidity,temperature)
                        if data == None: break;
                        data.setValue(DATA_KEY.serviceStatus,True)
                        data.setValue(DATA_KEY.lastUpdate,time.strftime("%H:%M:%S"))
                        sleep(data.getValue(DATA_KEY.refreshRate))
                        count += 1
                        if count >= Constants.SAVE_EVERY:
                                count = 0
                                data.save()
        except KeyboardInterrupt:
                print("Smart thermostat service stopped by the user...")
        data.setValue(DATA_KEY.serviceStatus,False)
        server.stop()
except:
        print(traceback.format_exc())
        data.setValue(DATA_KEY.serviceStatus,False)
        server.stop()