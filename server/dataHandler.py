
from os import path
import json

class DATA_KEY:
    serviceStatus       = 'serviceStatus'
    requiredTemperature = 'requiredTemperature'
    currentTemperature  = 'currentTemperature'
    currentHumidity     = 'currentHumidity'
    temperatureOffset   = 'temperatureOffset'
    refreshRate         = 'refreshRate'
    font                = 'font'
    thermostatState     = 'thermostatState'

LOCAL_FILE_NAME = 'data.json'
DEFAULT_VALUES = {
    DATA_KEY.serviceStatus : 'inactive',
    DATA_KEY.currentTemperature : 20, #*C
    DATA_KEY.requiredTemperature : 20, #*C
    DATA_KEY.temperatureOffset : 0.5, #*C
    DATA_KEY.refreshRate : 60, #Seconds
    DATA_KEY.font : '',
    DATA_KEY.thermostatState : False #Closed
}

class Data:
    def __init__(self):
        self._data = {}
        self.load()

    def getValue(self,key):
        if key in self._data:
            return None
        return self._data[key]

    def setValue(self,key,value):
        self._data[key] = value

    def deleteKey(self,key):
        del self._data[key]

    def load(self):
        if not path.isfile(LOCAL_FILE_NAME):
            self._data = DEFAULT_VALUES
            return;
        try:
            file = open('file.json','r')
        except:
            return
        self._data = json.load(file)
        file.close()

    def save(self):
        if self._data == {}:
            return
        try:
            file = open('file.json','w')
        except:
            return
        json.dump(self._data,file)
        file.close()