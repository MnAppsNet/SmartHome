
from os import path, remove
from const import Constants
from handlers.responseHandler import MESSAGE
import json, shutil
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
    schedule            = 'schedule'
    sensors             = 'sensors'
    primarySensor       = 'primarySensor'
    thermostat          = 'thermostat'
    thermostatSecret    = 'thermostatSecret'
    class SENSORS:
        ip                  = "ip"
        name                = "name"
        temperature         = "temperature"
        humidity            = "humidity"
        temperatureOffset   = "temperatureOffset"
        humidityOffset      = "humidityOffset"
        delete              = "delete"
        primary             = "primary"
        offline             = "offline"
    class USERS_KEY:
        username = 'username'
        password = 'password'

DEFAULT_ADMIN_USER = 'admin'
DEFAULT_ADMIN_PASSWORD = '756bc47cb5215dc3329ca7e1f7be33a2dad68990bb94b76d90aa07f4e44a233a'

DEFAULT_VALUES = {
    DATA_KEY.host : "0.0.0.0",
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
    DATA_KEY.sensors : {},      #Define sensors to be used - dictionaries with either 'pin' or 'ip' as key
    DATA_KEY.thermostat : Constants.THERMOSTAT_PIN, #Thermostat PIN or IP
    #[ { "pin"/"ip":"" 
    # "temperature":"",
    # "humidity":"",
    # "temperatureOffset":"",
    # "humidityOffset":"" }]
    DATA_KEY.schedule : {},
    DATA_KEY.primarySensor : Constants.SENSOR_PIN,
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
        self.numberOfSaves = 0

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
            return
        
        data_loader = False
        while not data_loader:
            try:
                file = open(Constants.LOCAL_FILE_NAME,'r')
            except:
                return
            try:
                self._data = json.load(file)
                data_loader = True
            except:
                file.close()
                if path.exists(Constants.LOCAL_FILE_NAME_BACKUP):
                    shutil.copy2(Constants.LOCAL_FILE_NAME_BACKUP, Constants.LOCAL_FILE_NAME)
                    remove(Constants.LOCAL_FILE_NAME_BACKUP)
                else:
                    return
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

            #Backup data file
            self.numberOfSaves += 1
            if self.numberOfSaves >= Constants.BACKUP_EVERY:
                self.numberOfSaves = 0
                if path.exists(Constants.LOCAL_FILE_NAME):
                    if path.exists(Constants.LOCAL_FILE_NAME_BACKUP):
                        remove(Constants.LOCAL_FILE_NAME_BACKUP)
                    shutil.copy2(Constants.LOCAL_FILE_NAME, Constants.LOCAL_FILE_NAME_BACKUP)
            return True
        except:
            return False