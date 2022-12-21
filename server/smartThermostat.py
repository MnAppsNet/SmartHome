import traceback, pytz
from controllers.displayController import Texts #, TemperatureAndHumidityScreen <= Can be commented out in a screen needed
from controllers.sensorController import Sensor
from controllers.thermostatController import Thermostat
from handlers.dataHandler import Data, DATA_KEY
from time import sleep
from const import Constants
from datetime import datetime
from server import Server

TIMEZONE = 'Europe/Athens'

#Instances of all our handlers :
data = Data()
host = data.getValue(DATA_KEY.host)
port = data.getValue(DATA_KEY.port)
if host == None: host = '0.0.0.0'
if port == None: port = 6969
server = Server( host, port ,data)
server.start()

print(f"Server started at {host}:{port}")

try:
        thermostat = Thermostat(Constants.THERMOSTAT_PIN,data)
        #display = TemperatureAndHumidityScreen(data.getValue(DATA_KEY.font)) <= Can be commented out in a screen needed
        sensor = Sensor(Constants.SENSOR_PIN)
        try:
                prevTemp = -100
                count = 0
                while True:
                        humidity,temperature = sensor.readData()
                        if temperature == None:
                                print("Failed to get temperature... Trying again...")
                                continue;
                        if temperature < prevTemp - 4 and prevTemp != -100:
                                #Very huge temperature difference in a sort time frame
                                #Measure could be faulty... Try again...
                                print("Measurement seems faulty... Try again...")
                                continue
                        else:
                                prevTemp = temperature
                        thermostatState = thermostat.checkState(temperature)
                        #display.showData(humidity,temperature,thermostatState) <= Can be commented out in a screen needed
                        if data == None: break;
                        data.setValue(DATA_KEY.serviceStatus,True)
                        data.setValue(DATA_KEY.lastUpdate,datetime.now(pytz.timezone('TIMEZONE')).strftime("%H:%M:%S"))
                        data.setValue(DATA_KEY.currentTemperature,temperature)
                        data.setValue(DATA_KEY.currentHumidity,humidity)

                        #Print to console the current state :
                        print(Texts.getLastUpdateTimeText())
                        print(Texts.getHumidityText(humidity))
                        print(Texts.getTemperatureText(temperature))
                        print(Texts.getThermostatState(thermostatState))

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