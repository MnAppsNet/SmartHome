from http.server import BaseHTTPRequestHandler
from handlers.dataHandler import Data
from handlers.responseHandler import MESSAGE, RESPONSE_KEY, RESPONSE_CODE
from handlers.actionHandler import Actions
from const import Constants
import json, traceback

class HEADER_KEY:
    authorization = 'Authorization'
    contentLength = 'Content-Length'
    contentType = 'Content-type'
    jsonContent = 'application/json'
    textContent = 'text/html'
    authentication = 'WWW-Authenticate'
    authenticationType = 'Basic realm="RaspbPi"'
    encoding = 'Accept-Encoding'


class REQUEST_KEY:
    actions = 'actions'


def requestHandler(data:Data):
    class requestHandler(BaseHTTPRequestHandler):

        def _sendResponse(self,response)->None:
            '''
            Send response back to client
            '''
            self.wfile.write(bytes(json.dumps(response), Constants.ENCODING))

        def _getRequestData(self)->dict:
            '''
            Check the validity of the inbound request
            Returns : requestData:Dict
            '''
            content_length = int(self.headers[HEADER_KEY.contentLength])
            requestData = self.rfile.read(content_length).decode(Constants.ENCODING)
            return json.loads(requestData)

        def _checkRequest(self,request, response)->dict:
            '''
            Check the validity of the inbound request
            Returns : Response:dict
            '''
            #Check for authorization header
            if self.headers.get(HEADER_KEY.authorization) == None:
                self.do_AUTHHEAD()
                response = MESSAGE.setError(response,MESSAGE.noAuthHeader)
                return response, None

            #Check if the request is authorized
            username = Actions.authorize_(self.headers.get(HEADER_KEY.authorization),data)
            if username == None:
                response = MESSAGE.setError(response,MESSAGE.notAuthorized)
                return response, None

            #Check actions are provided
            if REQUEST_KEY.actions not in request:
                response = MESSAGE.setError(response,MESSAGE.noActions)
                return response, None

            #Check if actions are correctly formatted
            validTypes = [str,list,dict]
            if type(request[REQUEST_KEY.actions]) not in validTypes:
                response = MESSAGE.setError(response,MESSAGE.invalidJson)
                return response, None

            return response, username

        def _checkAction(self,action,response)->tuple:
            '''
            Check action validity
            Returns : Action:str , Value:any , Response:dict
            '''
            if type(action) == str:
                #This must be a Getter or a Do action
                if action[:3] != 'get' and action[:2] != 'do':
                    response = MESSAGE.setError(MESSAGE.invalidAction,action)
                return action, None , response
            elif type(action) == dict:
                #This must be a Setter action
                valid = True
                if len(action) < 1:
                    return None, None, response
                if len(action) > 1:
                    valid = False
                for key in action:
                    if key[:3] != 'set' and key[:2] != 'do' or valid == False:
                        response = MESSAGE.setError(MESSAGE.invalidAction,action)
                    return key, action[key], response #Action , Value , Response

        def do_HEAD(self):
            #Create headers for the response
            self.send_response(RESPONSE_CODE.success)
            self.send_header(HEADER_KEY.contentType, HEADER_KEY.jsonContent)
            self.send_header(HEADER_KEY.encoding, Constants.ENCODING)
            self.end_headers()

        def do_AUTHHEAD(self):
            self.send_response(RESPONSE_CODE.not_authorized)
            self.send_header(HEADER_KEY.authentication, HEADER_KEY.authenticationType)
            self.send_header(HEADER_KEY.contentType, HEADER_KEY.jsonContent)
            self.send_header(HEADER_KEY.encoding, Constants.ENCODING)
            self.end_headers()

        def do_GET(self):
            #Handle GET requests
            self.do_HEAD()
            response = {RESPONSE_KEY.status:True}
            self._sendResponse(response)

        def do_POST(self):
            #Handle POST requests
            response = {
                RESPONSE_KEY.status : '',
                RESPONSE_KEY.message : ''
            }
            try:
                request = self._getRequestData()
            except:
                self.do_HEAD()
                response = MESSAGE.setError(response,MESSAGE.invalidJson)
                self._sendResponse(response)
                return

            response, currentUser = self._checkRequest(request,response)
            if response[RESPONSE_KEY.status] != MESSAGE.noAuthHeader:
                self.do_HEAD()

            #If an error occurred, exit the process
            if response[RESPONSE_KEY.status] == MESSAGE.Status.error:
                self._sendResponse(response)
                return
            #If a single action is given, convert it into a list
            if type(request[REQUEST_KEY.actions]) != list:
                request[REQUEST_KEY.actions] = [request[REQUEST_KEY.actions]]

            try:
                #START-FOR
                for action in request[REQUEST_KEY.actions]:
                    #Don't execute actions that contains the char '_' in their name
                    if '_' in action:
                        continue

                    value = None        #The value of a setter action, used only on setter actions

                    #Check if action is a Getter, a Do or a Setter
                    action,value,response = self._checkAction(action,response)
                    if response[RESPONSE_KEY.status] == MESSAGE.Status.error: break
                    if action == None: continue

                    #Get action method
                    try:
                        actionMethod = getattr(Actions, action)
                    except:
                        response = MESSAGE.setError(response,MESSAGE.invalidAction,action)
                        break;

                    #Execute action :
                    response = actionMethod(data,response,value,action,currentUser)

                    if response[RESPONSE_KEY.status] == MESSAGE.Status.error: break
                #END-FOR
            except:
                print(traceback.format_exc())
                response = MESSAGE.setError(response,MESSAGE.actionsFailed)

            if response[RESPONSE_KEY.status] == '':
                MESSAGE.setSuccess(response,MESSAGE.successfulExecution)

            self._sendResponse(response)

    return requestHandler