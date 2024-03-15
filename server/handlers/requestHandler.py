from handlers.dataHandler import Data
from handlers.responseHandler import MESSAGE, RESPONSE_KEY
from handlers.actionHandler import Actions
import traceback

class REQUEST_KEY:
    actions = 'actions'

class requestHandler():
    def __init__(self, request):
        self.request = request
        self.response = {
            RESPONSE_KEY.status: '',
            RESPONSE_KEY.message: ''
        }

    def _checkRequest(self, request) -> dict:
        '''
        Check the validity of the inbound request
        '''

        # Check the actions that are provided
        if REQUEST_KEY.actions not in request:
            self.response = MESSAGE.setError(
                self.response, MESSAGE.noActions)
            return

        # Check if actions are correctly formatted
        validTypes = [str, list, dict]
        if type(request[REQUEST_KEY.actions]) not in validTypes:
            self.response = MESSAGE.setError(
                self.response, MESSAGE.invalidJson)
            return

    def _checkAction(self, action) -> tuple:
        '''
        Check action validity
        Returns : Action:str , Value:any
        '''
        if type(action) == str:
            # This must be a Getter or a Do action, Setters require some value
            if action[:3] != 'get' and action[:2] != 'do':
                self.response = MESSAGE.setError(
                    MESSAGE.invalidAction, action)
            return action, None
        elif type(action) == dict:
            valid = True
            if len(action) < 1:
                return None, None #Empty list...
            if len(action) > 1:
                valid = False #The action dictionary should only contain one key and one value
            for key in action:
                if key[:3] != 'set' and key[:2] != 'do' and key[:3] != 'get' or valid == False:
                    self.response = MESSAGE.setError(
                        MESSAGE.invalidAction, action)
                    return None, None
                return key, action[key],  # Action , Value

    def performActions(self,data:Data):
        request = self.request

        self._checkRequest(request)

        # If an error occurred, exit the process
        if self.response[RESPONSE_KEY.status] == MESSAGE.Status.error:
            return

        # If a single action is given, convert it into a list
        if type(request[REQUEST_KEY.actions]) != list:
            request[REQUEST_KEY.actions] = [request[REQUEST_KEY.actions]]

        try:
            # START-FOR
            for action in request[REQUEST_KEY.actions]:
                # Don't execute actions that contains the char '_' in their name
                if '_' in action:
                    continue

                value = None #The extra info that might be needed along with the command

                # Check if action validity
                action, value = self._checkAction(action)
                if self.response[RESPONSE_KEY.status] == MESSAGE.Status.error:
                    break
                if action == None:
                    continue

                # Get action method
                try:
                    actionMethod = getattr(Actions, action)
                except:
                    self.response = MESSAGE.setError(
                        self.response, MESSAGE.invalidAction, action)
                    break

                # Execute action :
                self.response = actionMethod(
                    data, self.response, value, action)

                if self.response[RESPONSE_KEY.status] == MESSAGE.Status.error:
                    break
            # END-FOR
        except:
            print(traceback.format_exc())
            self.response = MESSAGE.setError(
                self.response, MESSAGE.actionsFailed)

        if self.response[RESPONSE_KEY.status] == '':
            MESSAGE.setSuccess(self.response, MESSAGE.successfulExecution)

    def getResponse(self):
        return self.response