try:
    import RPi.GPIO as GPIO
except:
    GPIO = None #For testing purposes
from handlers.dataHandler import Data, DATA_KEY

'''
This script is working with a heat element that can be enabled and disabled by connection or reconnecting
two cables, like a switch. These cables can be bridged with the Collector and the Emitter of a BJT transistor
and the switch can be done by providing a positive voltage between the Base and the Emitter of the transistor.
'''

#Constants
DEFAULT_THRESHOLD_TEMPERATURE = 20
DEFAULT_TEMPERATURE_OFFSET = 0.5
MAX_TEMPERATURE_OFFSET = 2
class Thermostat:
    def __init__(self,thermostatPin, dataHandler:Data = None):
        self._data = dataHandler
        self._pin = thermostatPin            #The pin where the heat switch is connected
        self._on = True                      #Thermostat is not off and it is working
        if GPIO != None:
            GPIO.setwarnings(False)
            GPIO.setup(self._pin, GPIO.OUT)

    def _setHeatState(self,state):
        if state:
            #If we are about to open the heat, check if thermostat is off
            self._on = self._getThermostatState()
        if self._on == False: return #Can't enable heat when thermostat is off
        if GPIO != None:
            GPIO.output(self._pin,state)
            if self._data != None:
                actualState = True if GPIO.input(self._pin) == 1 else False
                self._data.setValue(DATA_KEY.thermostatState,actualState)

    def _getThermostatState(self):
        if self._data == None:
            return self._off
        self._off = self._data.getValue(DATA_KEY.thermostatState)
        return self._off

    def _getTemperatureThreshold(self):
        if self._data == None:
            return DEFAULT_THRESHOLD_TEMPERATURE
        return self._data.getValue(DATA_KEY.requiredTemperature)

    def _getTemperatureOffset(self):
        if self._data == None:
            return DEFAULT_TEMPERATURE_OFFSET
        return self._data.getValue(DATA_KEY.requiredTemperature)

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
        threshold = self._getTemperatureThreshold()
        offset = self._getTemperatureOffset()
        if GPIO == None:
            return
        if temperature < threshold: #It's cold...
            #Turn heat on
            self._setHeatState(GPIO.HIGH)
        elif temperature > threshold + offset: #It's hot...
            #Turn heat off
            self._setHeatState(GPIO.LOW)