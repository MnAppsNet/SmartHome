
const Constants = {
    Commands : {
        path: "actions", //Server path to send the command
        //GET Commands >>
        getSessionID : "getSessionID",
        getCurrentTemperature: "getCurrentTemperature",
        getRequiredTemperature: "getRequiredTemperature",
        getCurrentHumidity: "getCurrentHumidity",
        getThermostatState: "getThermostatState",
        getRefreshRate: "getRefreshRate",
        getTemperatureOffset: "getTemperatureOffset",
        getLastUpdate: "getLastUpdate",
        //SET Commands >>
        setRequiredTemperature: "setRequiredTemperature",
        setThermostatState: "setThermostatState",
        setTemperatureOffset: "setTemperatureOffset",
        setRefreshRate: "setRefreshRate",
        //DO Commands >>
        doSave: "doSave",
        doCreateUser: "doCreateUser",
        doDeleteUser: "doDeleteUser",
        doLogOut: "doLogOut"
    },
    Response : {
        status      : 'status',
        message     : 'message',
        _data       : 'data',          //Not mandatory, marked with the char '_'
        _sessionID  : 'sessionID' //Not mandatory, marked with the char '_'
    },
    Status : {
        error       : 'E',
        success     : 'S',
        warning     : 'W',
        information : 'I'
    },
    Request : {
        actions             : 'actions',
        authType            : "Basic ",
        postMethod          : "POST",
        userAgentHeader     : "User-Agent",
        authorizationHeader : "Authorization",
        sessionID           : "sid",
        deviceID            : "Device-ID"
    },
    Messages : {
        failedToLogin : "Failed to login, try again...",
        invalidResponse : "Server gave an invalid response..."
    },
    Session : {
        sessionID           : "sessionID",
        localSessionID      : "localSessionID",
        server              : "server",
        requiredTemperature : "requiredTemperature"
    }
}

export default Constants