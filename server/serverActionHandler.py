from hashlib import sha256
from const import Constants
from dataHandler import Data, DATA_KEY
from responseHandler import RESPONSE_KEY, MESSAGE
from thermostatController import MAX_TEMPERATURE_OFFSET
import base64

class Actions:

    #/!\ Warning /!\===================================================/!\ Warning /!\#
    # Actions that don't contain the char '_' in their name are exposed by the server #
    #=================================================================================#

    def authorize_(authToken,data:Data):
        if authToken[:6] != 'Basic ':
            return
        users = data.getValue(DATA_KEY.users)
        authToken = authToken[6:]
        authToken = base64.b64decode(authToken).decode(Constants.ENCODING)
        authToken = authToken.split(':')
        if authToken[0] not in users:
            return False
        authToken[1] = sha256(authToken[1].encode(Constants.ENCODING)).hexdigest()
        if users[authToken[0]] == authToken[1]:
            return True
        return False

    #================#
    # Server Actions #
    #================#====================================
    def _getData(data:Data,response,dataKey):
        if RESPONSE_KEY.data not in response:
            response[RESPONSE_KEY.data] = {}
        response[RESPONSE_KEY.data][dataKey] = data.getValue(dataKey)
        return response

    def _setData(data:Data,response,dataKey,value):
        if RESPONSE_KEY.data not in response:
            response[RESPONSE_KEY.data] = {}
        if data.setValue(dataKey,value) == True:
            response[RESPONSE_KEY.data]['SET:' + dataKey] = MESSAGE.Status.success
        else:
            response[RESPONSE_KEY.data]['SET:' + dataKey] = MESSAGE.Status.error
        return response

    def _doResult(data:Data,response,action,message:str):
        if RESPONSE_KEY.data not in response:
            response[RESPONSE_KEY.data] = {}
        response[RESPONSE_KEY.data][action] = message
        return response

    #================#
    # Getter Actions #
    #================#====================================
    # Takes 3 arguments: data , response , actionName
    def getCurrentTemperature(data:Data,response:dict):
        return Actions._getData(data,response,DATA_KEY.currentTemperature)

    def getRequiredTemperature(data:Data,response:dict):
        return Actions._getData(data,response,DATA_KEY.requiredTemperature)

    def getCurrentHumidity(data:Data,response:dict):
        return Actions._getData(data,response,DATA_KEY.currentHumidity)

    def getThermostatState(data:Data,response:dict):
        return Actions._getData(data,response,DATA_KEY.thermostatState)

    def getRefreshRate(data:Data,response:dict):
        return Actions._getData(data,response,DATA_KEY.refreshRate)

    def getTemperatureOffset(data:Data,response:dict):
        return Actions._getData(data,response,DATA_KEY.temperatureOffset)

    #================#
    # Setter Actions #
    #================#====================================
    # Takes 4 arguments: data , response , value , actionName
    def setRequiredTemperature(data:Data,response:dict,value,actionName):
        if type(value) == str:
            try:
                value = float(value)
            except:
                return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        if type(value) != float:
            return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        return Actions._setData(data,response,DATA_KEY.requiredTemperature,value)

    def setThermostatState(data:Data,response:dict,value,actionName):
        if type(value) != bool:
            return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        return Actions._setData(data,response,DATA_KEY.thermostatState,value)

    def setTemperatureOffset(data:Data,response:dict,value,actionName):
        if type(value) == str:
            try:
                value = float(value)
            except:
                return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        if type(value) != float:
            return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        if value > MAX_TEMPERATURE_OFFSET:
            return MESSAGE.setError(response,MESSAGE.overThanMaxTempOffset,str(MAX_TEMPERATURE_OFFSET))
        return Actions._setData(data,response,DATA_KEY.thermostatState,value)

    def setRefreshRate(data:Data,response:dict,value,actionName):
        if type(value) == str:
            try:
                value = int(value)
            except:
                return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        if type(value) != int:
            return MESSAGE.setError(response,MESSAGE.wrongValueType,actionName)
        return Actions._setData(data,response,DATA_KEY.refreshRate,value)

    #============#
    # Do Actions #
    #============#========================================
    # Takes 3 arguments: data , response , value , actionName
    def doSave(data:Data,response:dict,value,actionName):
        success = data.save()
        if success:
            message = MESSAGE.Status.success
        else:
            message = MESSAGE.Status.error
        return Actions._doResult(data,response,actionName,message)