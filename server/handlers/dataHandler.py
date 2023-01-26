
from os import path
from const import Constants
from handlers.responseHandler import MESSAGE
import json
#from hashlib import sha256

class DATA_KEY:
    host                = "host"
    port                = "port"
    serviceStatus       = 'serviceStatus'
    requiredTemperature = 'requiredTemperature'
    currentTemperature  = 'currentTemperature'
    currentHumidity     = 'currentHumidity'
    temperatureOffset   = 'temperatureOffset'
    refreshRate         = 'refreshRate'
    font                = 'font'
    thermostatState     = 'thermostatState'
    users               = 'users'
    lastUpdate          = 'lastUpdate'
    thermostatOff       = 'thermostatOff'
    stateLogs           = 'stateLogs'
    class USERS_KEY:
        username = 'username'
        password = 'password'

DEFAULT_ADMIN_USER = 'admin'
DEFAULT_ADMIN_PASSWORD = '756bc47cb5215dc3329ca7e1f7be33a2dad68990bb94b76d90aa07f4e44a233a'

DEFAULT_VALUES = {
    DATA_KEY.host : "192.168.100.100",
    DATA_KEY.port : 6969,
    DATA_KEY.serviceStatus : False,
    DATA_KEY.currentTemperature : 0, #*C
    DATA_KEY.currentHumidity : 0, #*C
    DATA_KEY.requiredTemperature : 20, #*C
    DATA_KEY.temperatureOffset : 0.5, #*C
    DATA_KEY.refreshRate : 60, #Seconds
    DATA_KEY.lastUpdate : '00:00:00', #hh:mm:ss
    DATA_KEY.font : '',
    DATA_KEY.thermostatOff : False,
    DATA_KEY.thermostatState : False, #Closed
    DATA_KEY.users : #/!\ Default username and password for the initial user /!\
        {DEFAULT_ADMIN_USER : DEFAULT_ADMIN_PASSWORD}
        #Password is the sha256 of the sha256 of the actual user password, default: 1234
        #The password is hashed once on the client and we get the hashed password and hash it again
        #before we store it.
        #The first user in the dictionary is administrator and can create and delete users
        #The first time you create a user using the admin user, the default admin user is deleted
        #and the new user is the new user with admin rights
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
        if key == DATA_KEY.users: return False #No user changes allowed!
        try:
            self._data[key] = value
            return True
        except:
            return False

    def deleteKey(self,key):
        if key == DATA_KEY.users: return False #No user changes allowed!
        del self._data[key]

    def load(self):
        if not path.isfile(Constants.LOCAL_FILE_NAME):
            self._data = DEFAULT_VALUES
            return;
        try:
            file = open(Constants.LOCAL_FILE_NAME,'r')
        except:
            return
        self._data = json.load(file)
        file.close()

    def save(self):
        try:
            if self._data == {}:
                return False
            try:
                file = open(Constants.LOCAL_FILE_NAME,'w')
            except:
                return False
            json.dump(self._data,file)
            file.close()
            return True
        except:
            return False