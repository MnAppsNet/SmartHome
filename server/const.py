import pathlib

class Constants:
    FRONTEND_STATIC = 'client'
    FRONTEND = 'client'

    TIMEZONE = 'Europe/Athens'

    ENCODING = 'UTF-8'
    KEY_FILE = str(pathlib.Path(__file__).parent.resolve().joinpath('keys').joinpath('key.pem'))    #Make sure to generate a key and a certificate! You can use openssl :
    CERT_FILE = str(pathlib.Path(__file__).parent.resolve().joinpath('keys').joinpath('cert.pem'))  #openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -nodes

    LOCAL_FILE_NAME = str(pathlib.Path(__file__).parent.resolve().joinpath('data.json'))
    LOCAL_FILE_NAME_STATE_LOGS = str(pathlib.Path(__file__).parent.resolve().joinpath('state_changes.json'))

    THERMOSTAT_PIN = 11
    SENSOR_PIN = 4
    SAVE_EVERY = 1 #Loops. after these amount of loops of the service, the data will be hard saved automatically