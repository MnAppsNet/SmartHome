try:
    import RPi.GPIO as GPIO
except:
    GPIO = None #For testing purposes
import json
from handlers.dataHandler import Data, DATA_KEY
from const import Constants
from handlers.stateLogsHandler import StateLogs

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

    def setTemperatureOffset(self,offset):
        self._offset = offset

    def checkState(self,temperature):
        actualState = False
        threshold = self._getTemperatureThreshold()
        offset = self._getTemperatureOffset()
        if GPIO == None:
            print("Please install GPIO module...")
            return
        if temperature < threshold: #It's cold...
            #Turn heat on
            actualState = True
        #elif temperature > threshold + offset: #It's hot...
        #    #Turn heat off
        #    actualState = False

        actualState = self._setHeatState(actualState)

        #Get the actual state of the thermostat
        if self._data != None:
            self._logStateChanges(actualState,temperature,threshold)
            self._data.setValue(DATA_KEY.thermostatState,actualState)

        return actualState