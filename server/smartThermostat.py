#!/usr/bin/python3
import traceback, pytz, os
from controllers.displayController import Texts #, TemperatureAndHumidityScreen <= Can be commented out in a screen needed
from controllers.sensorController import Sensor
from controllers.thermostatController import Thermostat
from handlers.dataHandler import Data, DATA_KEY
from time import sleep
from const import Constants
from datetime import datetime
from server import Server

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
        thermostat = Thermostat(data)
        print("Thermostat controller loaded...")
        #display = TemperatureAndHumidityScreen(data.getValue(DATA_KEY.font)) <= Can be commented out in a screen needed
        sensor = Sensor(Constants.SENSOR_PIN,data)
        print("Sensor controller loaded...")
        try:
                prevTemp = None
                count = 0
                faultyTempCount = 0
                while True:
                        if server.isActive() == False:
                                print("Server is offline, restarting...")
                                server.start()
                        primarySensor = data.getValue(DATA_KEY.primarySensor)
                        if (primarySensor == None): primarySensor = Constants.SENSOR_PIN
                        print("Primary sensor: "+str(primarySensor))
                        humidity,temperature = sensor.readData(primarySensor)
                        if temperature != None:
                                if (prevTemp == None): prevTemp = temperature #Initialize...
                                if ( temperature < prevTemp - Constants.MAX_TEMPERATURE_CHANGE or 
                                   temperature > prevTemp + Constants.MAX_TEMPERATURE_CHANGE or 
                                   temperature > Constants.MAX_TEMPERATURE ):
                                        #Very huge temperature difference in a sort time frame
                                        #Measure could be faulty... Try again...
                                        print("Measurement seems faulty... Try again...")
                                        faultyTempCount += 1
                                        if faultyTempCount > Constants.MAX_MEASUREMENT_RETRIES:
                                                #If we think a faulty measurement for 20 times, then it is probably not faulty...
                                                prevTemp = temperature
                                        sleep(10)
                                        continue
                                else:
                                        prevTemp = temperature
                                        faultyTempCount = 0
                                thermostat.checkTemperatureSchedule()
                                thermostatState = thermostat.checkState(temperature)
                                #display.showData(humidity,temperature,thermostatState) <= Can be commented out in a screen needed
                                if data == None: break
                                data.setValue(DATA_KEY.serviceStatus,True)
                                data.setValue(DATA_KEY.lastUpdate,datetime.now(pytz.timezone(Constants.TIMEZONE)).strftime("%H:%M:%S"))
                                data.setValue(DATA_KEY.currentTemperature,temperature)
                                if humidity != None: data.setValue(DATA_KEY.currentHumidity,humidity)
                                sensor.updateSensorReadings()

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
except Exception as e:
        print(str(e),flush=True)
        print(traceback.format_exc(),flush=True)
        data.setValue(DATA_KEY.serviceStatus,False)
        try:
                server.stop()
        except:
                pass
        os._exit(1)