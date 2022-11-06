class RESPONSE_CODE:
    not_authorized = 401
    success = 200

class RESPONSE_KEY:
    status = 'status'
    message = 'message'
    data = 'data'

class MESSAGE:
    noAuthHeader = "No authorization header received"
    notAuthorized = "Not authorized"
    noActions = "No actions provided"
    invalidJson = "JSON request is invalid"
    actionsFailed  = "At least one of the actions failed to execute"
    invalidAction = "Action '&1' is invalid"
    invalidSetAction = "One of the setter actions is invalid"
    successfulExecution = "Execution was successful"
    wrongValueType = "The value type of action '&1' is invalid"
    overThanMaxTempOffset = "Maximum allowed temperature offset is &1 *C"
    userNotAuthorized = "User '&1' is not authorized to perform this action"
    userAlreadyExists = "User already exists"
    noSelfDeletion = "You can not delete your own user"
    #. . . .

    class Status:
        error = 'E'
        success = 'S'
        warning = 'W'
        information = 'I'

    def _setMessage(response:dict,message:str,type:str):
        response[RESPONSE_KEY.message] = message
        response[RESPONSE_KEY.status] = type
        return response

    def _setPlaceHolders(message:str,var1='',var2='',var3=''):
        if var1=='' and var2=='' and var3=='':
            return message
        return message.replace('&1',var1).replace('&2',var2).replace('&3',var3)

    def setError(response:dict,message:str,var1='',var2='',var3=''):
        message = MESSAGE._setPlaceHolders(message,var1,var2,var3)
        return MESSAGE._setMessage(response,message,MESSAGE.Status.error)

    def setSuccess(response:dict,message:str,var1='',var2='',var3=''):
        message = MESSAGE._setPlaceHolders(message,var1,var2,var3)
        return MESSAGE._setMessage(response,message,MESSAGE.Status.success)

    def setWarning(response:dict,message:str,var1='',var2='',var3=''):
        message = MESSAGE._setPlaceHolders(message,var1,var2,var3)
        return MESSAGE._setMessage(response,message,MESSAGE.Status.warning)

    def setInfo(response,message,var1='',var2='',var3=''):
        message = MESSAGE._setPlaceHolders(message,var1,var2,var3)
        return MESSAGE._setMessage(response,message,MESSAGE.Status.information)