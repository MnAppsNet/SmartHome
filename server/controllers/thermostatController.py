try:
    import RPi.GPIO as GPIO
except:
    GPIO = None #For testing purposes
import json, pytz
from handlers.dataHandler import Data, DATA_KEY
from const import Constants
from handlers.stateLogsHandler import StateLogs
from datetime import datetime

'''
This script is working with a heat element that can be enabled and disabled by connection or reconnecting
two cables, like a switch. These cables can be bridged with the Collector and the Emitter of a BJT transistor
and the switch can be done by providing a positive voltage between the Base and the Emitter of the transistor.
'''

#Constants
DEFAULT_THRESHOLD_TEMPERATURE = 20
DEFAULT_TEMPERATURE_OFFSET = 0.2
MAX_TEMPERATURE_OFFSET = 2
class Thermostat:
    def __init__(self,thermostatPin, dataHandler:Data = None):
        self._data = dataHandler
        self._pin = thermostatPin            #The pin where the heat switch is connected
        self._off = False                    #Thermostat is not off and it is working
        if GPIO != None:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self._pin, GPIO.OUT, initial=False)

    def _setHeatState(self,state):
        if state == True:
            #If we are about to open the heat, check if thermostat is off
            self._off = self._getThermostatState()
        if self._off == True: state = False #Can't enable heat when thermostat is off
        if GPIO != None:
            GPIO.output(self._pin,state)
        return state

    def _getThermostatState(self):
        if self._data == None:
            return self._off
        self._off = self._data.getValue(DATA_KEY.thermostatOff)
        return self._off

    def _getTemperatureThreshold(self):
        if self._data == None:
            return DEFAULT_THRESHOLD_TEMPERATURE
        return self._data.getValue(DATA_KEY.requiredTemperature)

    def _getTemperatureSchedule(self):
        if self._data == None:
            return None
        return self._data.getValue(DATA_KEY.schedule)

    def _getTemperatureOffset(self):
        if self._data == None:
            return DEFAULT_TEMPERATURE_OFFSET
        return self._data.getValue(DATA_KEY.temperatureOffset)

    def _logStateChanges(self,currentState,temperature,threshold):
        prevState = self._data.getValue(DATA_KEY.thermostatState)
        if prevState == currentState:
            return #State not changed
        StateLogs.addEntry(currentState,temperature,threshold)

    def turnOff(self):
        self._off = True
        self._data.setValue(DATA_KEY.thermostatState,False)

    def turnOn(self):
        self._off = False
        self._data.setValue(DATA_KEY.thermostatState,True)

    def setTemperatureThreshold(self,temperature):
        self._threshold = temperature
        if self._data != None:
            self._data.setValue(DATA_KEY.requiredTemperature,temperature)

    def setTemperatureOffset(self,offset):
        self._offset = offset
        if self._data != None:
            self._data.setValue(DATA_KEY.temperatureOffset,offset)

    def checkTemperatureSchedule(self):
        '''
        Check the temperature schedules defined and change the required temperature accordingly
        '''
        schedule = self._getTemperatureSchedule()
        if schedule == None: return
        #Get the current time in a numeric format that can be compared :
        currentTime = int(datetime.now(pytz.timezone(Constants.TIMEZONE)).strftime("%H%M"))
        #Get current refresh rate in minutes if more that two minutes (we don't wont to skip any schedule) :
        refreshRate = None
        if self._data != None:
            refreshRate = self._data.getValue(DATA_KEY.refreshRate)
        if refreshRate == None:
            refreshRate = 60
        refreshRate = int(refreshRate / 120)
        #Check all defined temperature schedules :
        for key in schedule:
            #Convert key into number to be compared :
            time = key.split(':')
            if len(time) != 2: continue
            time = time[0] + time[1]
            time = int(time)
            #Check if schedule applies and if yes set required temperature :
            if (time - refreshRate <= currentTime and time >= currentTime ):
                self.setTemperatureThreshold(schedule[key]);
                break;

    def checkState(self,temperature):
        '''
        Check the thermostat state and set it according to required temperature
        '''
        actualState = False
        prevState = self._data.getValue(DATA_KEY.thermostatState)
        threshold = self._getTemperatureThreshold()
        offset = self._getTemperatureOffset()
        if GPIO == None:
            print("Please install GPIO module...")
            return
        if temperature < threshold: #It's cold...
            #Turn heat on
            actualState = True
        elif prevState == True and temperature < threshold + offset:
            #If it was previously turned on and the new temp is not reached yet
            #Keep the heat on
            actualState = True

        actualState = self._setHeatState(actualState)

        #Get the actual state of the thermostat
        if self._data != None:
            self._logStateChanges(actualState,temperature,threshold)
            self._data.setValue(DATA_KEY.thermostatState,actualState)

        return actualState