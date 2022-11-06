import pathlib

class Constants:
    ENCODING = 'UTF-8'
    KEY_FILE = str(pathlib.Path(__file__).parent.resolve()) + '/key.pem'    #Make sure to generate a key and a certificate! You can use openssl :
    CERT_FILE = str(pathlib.Path(__file__).parent.resolve()) + '/cert.pem'  #openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -nodes