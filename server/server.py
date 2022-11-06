from http.server import HTTPServer
from dataHandler import Data
from requestHandler import requestHandler
from threading import Thread
from const import Constants
import ssl

class Server():
    def __init__(self,host='localhost',port=6969,dataHandler:Data=None):
        #Start the hosting...
        self._serve = True
        self._data = dataHandler
        handler = requestHandler(self._data)
        self._server = HTTPServer((host,port),handler)
        self._server.socket = ssl.wrap_socket(self._server.socket,
                                              keyfile=Constants.KEY_FILE,
                                              certfile=Constants.CERT_FILE,
                                              ssl_version=ssl.PROTOCOL_TLS)
        self._thread = Thread(target=self._start, name="HTTPHandler")
        self._thread.start()

    def _start(self):
        while (self._serve):
            self._server.handle_request()

    def setDataHandler(self,dataHandler:Data):
        self._data = dataHandler

    def stop(self):
        self._serve = False
        self._thread.join()
        self._server.server_close()