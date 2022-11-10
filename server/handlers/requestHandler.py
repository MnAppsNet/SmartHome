from http.server import BaseHTTPRequestHandler
from handlers.dataHandler import Data
from handlers.responseHandler import MESSAGE, RESPONSE_KEY, RESPONSE_CODE
from handlers.actionHandler import Actions
from const import Constants
from datetime import datetime
import json, traceback, time, re, random

class HEADER_KEY:
    authorization = 'Authorization'
    contentLength = 'Content-Length'
    contentType = 'Content-type'
    jsonContent = 'application/json'
    textContent = 'text/html'
    authentication = 'WWW-Authenticate'
    authenticationType = 'Basic realm="RaspbPi"'
    encoding = 'Accept-Encoding'
    setCookie = 'Set-Cookie'
    cookies = 'Cookie'
    userAgent = 'User-Agent'
    allow = 'Allow'
    get = 'GET'
    post = 'POST'
    origin = 'Origin'
    accessControlAllowMethods = 'Access-Control-Allow-Methods'
    accessControlAllowOrigin = 'Access-Control-Allow-Origin'
    accessControlAllowHeaders = 'Access-Control-Allow-Headers'

class REQUEST_KEY:
    actions = 'actions'


def requestHandler(data:Data):
    sessions = {}
    class requestHandler(BaseHTTPRequestHandler):

        def _generateSessionID(self):
            chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            parts = 4
            sessionID = "-".join("".join(random.choice(chars) for _ in range(random.randint(4,8))) for _ in range(parts))
            return sessionID

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

        def _parseCookies(self, cookie_list):
            return dict(((c.split("=")) for c in cookie_list.split(";"))) if cookie_list else {}

        def _checkSessionID(self):
            if HEADER_KEY.cookies not in self.headers:
                return None
            cookie = self._parseCookies(self.headers[HEADER_KEY.cookies])
            sessionKey = 'sid'
            if sessionKey not in cookie:
                return None
            sid = cookie[sessionKey]
            if sid in sessions:
                ip = sessions[sid][0]
                agent = sessions[sid][2]
                origin = sessions[sid][4]
                currentOrigin = self.headers[HEADER_KEY.origin] if HEADER_KEY.origin in self.headers else None
                currentAgent = self.headers[HEADER_KEY.userAgent] if HEADER_KEY.userAgent in self.headers else None
                if agent == currentAgent and ip == self.client_address[0] and currentOrigin == origin:
                    return sid
                else:
                    del sessions[sid]
            return None

        def _getUserFromSessionID(self,sessionID):
            if sessionID in sessions:
                return sessions[sessionID][1]
            return None

        def _setSessionID(self,username):
            ip = self.client_address[0]
            sessionID = self._generateSessionID()
            origin = None
            if HEADER_KEY.origin in self.headers:
                origin = self.headers[HEADER_KEY.origin]
            agent = self.headers[HEADER_KEY.userAgent] if HEADER_KEY.userAgent in self.headers else None
            sessions[sessionID] = [ip,username,agent,time.strftime("%Y-%d-%mT%H:%M:%S"), origin]
            self.cookie = "sid={}".format(sessionID)
            return sessionID

        def _clearOldSessions(self):
            '''
            Clear sessions older than 30 days
            '''
            for sid in sessions:
                dateTime = datetime.strptime(sessions[sid][3], "%Y-%d-%mT%H:%M:%S")
                if (datetime.today() - dateTime).total_seconds() > 60 * 60 * 24 * 30: #60sec * 60min * 24h * 30days = 2592000 seconds
                    del sessions[sid]

        def _checkRequest(self,request, response)->dict:
            '''
            Check the validity of the inbound request
            Returns : Response:dict
            '''
            #Check if there is an active sessionID for this user
            sessionID = self._checkSessionID()
            username = self._getUserFromSessionID(sessionID)

            #Check for authorization header
            if self.headers.get(HEADER_KEY.authorization) == None and username == None:
                self.do_AUTHHEAD()
                response = MESSAGE.setError(response,MESSAGE.noAuthHeader)
                return response, None

            #Check if the request is authorized
            if username == None:
                #Not already logged in...
                username = Actions.authorize_(self.headers.get(HEADER_KEY.authorization),data)
            if username == None:
                response = MESSAGE.setError(response,MESSAGE.notAuthorized)
                return response, None
            else:
                #Keep user logged in...
                if sessionID == None: sessionID = self._setSessionID(username)

            self.sessionID = sessionID

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

        def _cors_header(self):
            if not HEADER_KEY.origin in self.headers:
                return
            origin = self.headers[HEADER_KEY.origin]
            ip = self.client_address[0]
            if ip == '127.0.0.1' : ip = 'localhost'
            if re.match(f"(http|https):\/\/{ip}:\d+",origin) == None:
                return
            self.send_header(HEADER_KEY.accessControlAllowOrigin, origin)

        def do_HEAD(self):
            #Create headers for the response
            self.send_response(RESPONSE_CODE.ok)
            self.send_header(HEADER_KEY.contentType, HEADER_KEY.jsonContent)
            self.send_header(HEADER_KEY.encoding, Constants.ENCODING)
            self._cors_header()
            try:
                if self.cookie:
                    #Session ID Cookie
                    self.send_header(HEADER_KEY.setCookie, self.cookie)
            except:
                pass
            self.end_headers()

        def do_OPTIONS(self):
            self.send_response(RESPONSE_CODE.ok)
            self.send_header(HEADER_KEY.authentication, HEADER_KEY.authenticationType)
            self.send_header(HEADER_KEY.allow, HEADER_KEY.get + "," + HEADER_KEY.post)
            self.send_header(HEADER_KEY.accessControlAllowMethods, HEADER_KEY.get + "," + HEADER_KEY.post)
            self.send_header(HEADER_KEY.accessControlAllowHeaders, "*")
            self._cors_header()
            self.send_header(HEADER_KEY.encoding, Constants.ENCODING)
            self.end_headers()

        def do_AUTHHEAD(self):
            self.send_response(RESPONSE_CODE.not_authorized)
            self.send_header(HEADER_KEY.authentication, HEADER_KEY.authenticationType)
            self.send_header(HEADER_KEY.contentType, HEADER_KEY.jsonContent)
            self.send_header(HEADER_KEY.accessControlAllowOrigin, "*")
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

                    #SessionID is in the response only when we try to get or delete the session
                    if RESPONSE_KEY.sessionID in response:
                        if response[RESPONSE_KEY.sessionID] == "":
                            response[RESPONSE_KEY.sessionID] = self.sessionID
                        else:
                            if RESPONSE_KEY.sessionID in response: del response[RESPONSE_KEY.sessionID]
                            if self.sessionID in sessions: del sessions[self.sessionID]

                    if response[RESPONSE_KEY.status] == MESSAGE.Status.error: break
                #END-FOR
            except:
                print(traceback.format_exc())
                response = MESSAGE.setError(response,MESSAGE.actionsFailed)

            if response[RESPONSE_KEY.status] == '':
                MESSAGE.setSuccess(response,MESSAGE.successfulExecution)

            self._sendResponse(response)
            self._clearOldSessions()

    return requestHandler