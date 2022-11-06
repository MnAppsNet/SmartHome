
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
    users               = 'users'
    class USERS_KEY:
        username = 'username'
        password = 'password'

LOCAL_FILE_NAME = 'data.json'
DEFAULT_VALUES = {
    DATA_KEY.serviceStatus : 'inactive',
    DATA_KEY.currentTemperature : 20, #*C
    DATA_KEY.requiredTemperature : 20, #*C
    DATA_KEY.temperatureOffset : 0.5, #*C
    DATA_KEY.refreshRate : 60, #Seconds
    DATA_KEY.font : '',
    DATA_KEY.thermostatState : False, #Closed
    DATA_KEY.users : #/!\ Default username and password for the initial user /!\
        {'admin' : '756bc47cb5215dc3329ca7e1f7be33a2dad68990bb94b76d90aa07f4e44a233a'}
        #Password is the sha256 of the sha256 of the actual user password, default: 1234
        #The password is hashed once on the client and we get the hashed password and hash it again
        #before we store it
}

class Data:
    def __init__(self):
        self._data = {}
        self.load()

    def getValue(self,key):
        if key not in self._data:
            return None
        return self._data[key]

    def setValue(self,key,value):
        try:
            self._data[key] = value
            return True
        except:
            return False

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
        try:
            if self._data == {}:
                return False
            try:
                file = open('file.json','w')
            except:
                return False
            json.dump(self._data,file)
            file.close()
            return True
        except:
            return False