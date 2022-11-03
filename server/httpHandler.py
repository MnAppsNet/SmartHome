from http.server import HTTPServer, BaseHTTPRequestHandler
from dataHandler import DATA_KEY
from threading import Thread
import serviceTools
import json

ENCODING = 'UTF-8'

class Server(BaseHTTPRequestHandler):

    def _createHeaders(self):
        #Create headers for the response
        self.send_response('200')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _getData(self,key):
        #Get data from data handler
        if self._data == None:
            return None
        return self._data.getValue(key)

    def _start(self):
        while (self._serve):
            self._server.handle_request()

    def start(self,host='localhost',port=6969,dataHandler=None):
        #Start the hosting...
        self._serve = True
        self._server = HTTPServer(host,port,Server)
        self._data = dataHandler
        self._thread = Thread(target=self._start, name="HTTPHandler")
        self._thread.start()

    def setDataHandler(self,dataHandler):
        self._data = dataHandler

    def stop(self):
        self._serve = False
        self._thread.join()
        self._thread.close()
        self._server.server_close()

    def do_GET(self):
        self._createHeaders()

        response = {
            "serviceStatus":self.getData[DATA_KEY.serviceStatus]
        }
        self.wfile.write(bytes(json.dumps(response), ENCODING))

    def do_POST(self):
        self._createHeaders()
        content_length = int(self.headers['Content-Length'])
        requestData = self.rfile.read(content_length).decode(ENCODING)
        response = {
            ""
        }
        try:
            data = json.loads(requestData)
        except:
            pass
        self.wfile.write(bytes(json.dumps(response), ENCODING))