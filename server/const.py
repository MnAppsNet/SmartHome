import pathlib

class Constants:
    FRONTEND_STATIC = 'client'
    FRONTEND = 'client'

    TIMEZONE = 'Europe/Athens'

    ENCODING = 'UTF-8'
    KEY_FILE = str(pathlib.Path(__file__).parent.resolve().joinpath('keys').joinpath('key.pem'))    #Make sure to generate a key and a certificate! You can use openssl :
    CERT_FILE = str(pathlib.Path(__file__).parent.resolve().joinpath('keys').joinpath('cert.pem'))  #openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -nodes

    LOCAL_FILE_NAME = str(pathlib.Path(__file__).parent.resolve().joinpath('data.json'))
    LOCAL_FILE_NAME_BACKUP = f"{LOCAL_FILE_NAME}.bck"
    LOCAL_FILE_NAME_STATE_LOGS = str(pathlib.Path(__file__).parent.resolve().joinpath('state_changes.json'))

    THERMOSTAT_PIN = '192.168.100.102' #PIN or IP of initial thermostat to use
    SENSOR_PIN = '192.168.100.101' #PIN or IP of initial sensor to use
    SAVE_EVERY = 1 #Loops. after these amount of loops of the service, the data will be hard saved automatically

    REQUEST_HEADER_HASH = "HASH"

    MAX_TEMPERATURE = 80 #max allowed temperature in *C that is allowed
    MAX_TEMPERATURE_CHANGE = 10 #max allowed change in *C on each consequential measurement
    MAX_MEASUREMENT_RETRIES = 5 #max retries when temperature seems faulty
    
    BACKUP_EVERY = 5 #Backup every X save actions performed