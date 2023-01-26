from const import Constants
from handlers.dataHandler import Data, DATA_KEY
from handlers.responseHandler import RESPONSE_KEY, MESSAGE
from controllers.thermostatController import MAX_TEMPERATURE_OFFSET
from handlers.stateLogsHandler import StateLogs
#from hashlib import sha256
#import base64

class Actions:

    #/!\ Warning /!\===================================================/!\ Warning /!\#
    # Actions that don't contain the char '_' in their name are exposed by the server #
    #=================================================================================#

    #Authorization to be implemented
    #def authorize_(authToken,data:Data):
    #    '''
    #    Check if use is authorized and return authorized username
    #    '''
    #    if authToken[:6] != 'Basic ':
    #        return
    #    users = data.getValue(DATA_KEY.users)
    #    authToken = authToken[6:]
    #    authToken = base64.b64decode(authToken).decode(Constants.ENCODING)
    #    authToken = authToken.split(':')
    #    if authToken[0] not in users:
    #        return None
    #    authToken[1] = sha256(authToken[1].encode(Constants.ENCODING)).hexdigest()
    #    if users[authToken[0]] == authToken[1]:
    #        return authToken[0]
    #    return None

    #================#
    # Server Actions #
    #================#====================================
    def _getData(data:Data,response,dataKey,actionName):
        if RESPONSE_KEY.data not in response:
            response[RESPONSE_KEY.data] = {}
        response[RESPONSE_KEY.data][actionName] = data.getValue(dataKey)
        return response

    def _setData(data:Data,response,dataKey,value,actionName):
        if RESPONSE_KEY.data not in response:
            response[RESPONSE_KEY.data] = {}
        if data.setValue(dataKey,value) == True:
            response[RESPONSE_KEY.data][actionName] = MESSAGE.Status.success
        else:
            response[RESPONSE_KEY.data][actionName] = MESSAGE.Status.error
        return response

    def _doResult(data:Data,response,action,message:str):
        if RESPONSE_KEY.data not in response:
            response[RESPONSE_KEY.data] = {}
        response[RESPONSE_KEY.data][action] = message
        return response

    #================#
    # Getter Actions #
    #================#====================================
    # Takes 5 arguments: data , response , value, actionName
    def getCurrentTemperature(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":["getCurrentTemperature"]
        '''
        return Actions._getData(data,response,DATA_KEY.currentTemperature,actionName)

    def getRequiredTemperature(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":["getRequiredTemperature"]
        '''
        return Actions._getData(data,response,DATA_KEY.requiredTemperature,actionName)

    def getCurrentHumidity(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":["getCurrentHumidity"]
        '''
        return Actions._getData(data,response,DATA_KEY.currentHumidity,actionName)

    def getThermostatState(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":["getThermostatState"]
        '''
        return Actions._getData(data,response,DATA_KEY.thermostatState,actionName)

    def getRefreshRate(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":["getRefreshRate"]
        '''
        return Actions._getData(data,response,DATA_KEY.refreshRate,actionName)

    def getTemperatureOffset(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":["getTemperatureOffset"]
        '''
        return Actions._getData(data,response,DATA_KEY.temperatureOffset,actionName)

    def getLastUpdate(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":["getLastUpdate"]
        '''
        return Actions._getData(data,response,DATA_KEY.lastUpdate,actionName)

    def getSessionID(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":["getSessionID"]
        '''
        response[RESPONSE_KEY.sessionID] = "" #Don't know the sessionID in this context,
                                              #create the key and it will get populated later
        return response #Don't do anything, call this action when you just want the sessionID

    def getStateLogs(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":[{"getStateLogs":{ "year":year, "month":month, "day":day }}]
        '''
        if type(value) != dict:
            return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        if not "year" in value:
            value["year"] = None
        if not "month" in value:
            value["month"] = None
        if not "day" in value:
            value["day"] = None
        logs = StateLogs().getEntries(value["year"],value["month"],value["day"])
        if not RESPONSE_KEY.data in response:
            response[RESPONSE_KEY.data] = {}
        response[RESPONSE_KEY.data][actionName] = logs
        return response

    #================#
    # Setter Actions #
    #================#====================================
    # Takes 4 arguments: data , response , value , actionName
    def setRequiredTemperature(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":[{"setRequiredTemperature":10}]
        '''
        if type(value) in [str, int]:
            try:
                value = float(value)
            except:
                return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        if type(value) != float:
            return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        return Actions._setData(data,response,DATA_KEY.requiredTemperature,value,actionName)

    def setThermostatState(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":[{"setThermostatState":False}]
        '''
        if type(value) != bool:
            return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        return Actions._setData(data,response,DATA_KEY.thermostatState,value,actionName)

    def setTemperatureOffset(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":[{"setTemperatureOffset":0.5}]
        '''
        if type(value) in [str,int]:
            try:
                value = float(value)
            except:
                return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        if type(value) != float:
            return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        if value > MAX_TEMPERATURE_OFFSET:
            return MESSAGE.setError(response,MESSAGE.overThanMaxTempOffset,str(MAX_TEMPERATURE_OFFSET))
        return Actions._setData(data,response,DATA_KEY.thermostatState,value,actionName)

    def setRefreshRate(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":[{"setRefreshRate":10}]
        '''
        if type(value) in [str,int]:
            try:
                value = int(value)
            except:
                return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        if type(value) != int:
            return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        return Actions._setData(data,response,DATA_KEY.refreshRate,value,actionName)

    #============#
    # Do Actions #
    #============#========================================
    # Takes 3 arguments: data , response , value , actionName
    def doSave(data:Data,response:dict,value,actionName:str):
        '''
        request : "actions":["doSave"]
        '''
        success = data.save()
        if success:
            message = MESSAGE.dataSaved
        else:
            message = MESSAGE.dataSaveFailed
        return Actions._doResult(data,response,actionName,message)