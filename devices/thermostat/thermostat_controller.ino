#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <MD5.h>

#define HEADER_HASH "HASH"
#define ARG_STATE "state"
#define ARG_STATE_ON "ON"

MD5Builder md5;

//Credentials
const char* ssid = "YOUR_SSID_HERE";            //You network SSID
const char* password = "YOUR_PASSWORD_HERE";    //You network WiFi password
String SECRET = "YOUR_SECRET_HERE";             //This is the secret part of the PIN

ESP8266WebServer server(80);

const int led = 2;                              //LED Pin
const int switchPin = 15;                       //GPIO15

bool STATE = false;                             //Thermostat state

String PIN = "";                                //A new PIN is generated every time the old one is consumed
String HASH = "";                               //This is the hash of the PIN + SECRET

const uint pinLength = 10;                       //PIN length

void generatePIN() {
  unsigned long currentTime = millis();
  const char characters[] = "0123456789qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM.,$#&_";

  //Generate new PIN
  PIN = "";
  for (int i = 0; i < pinLength; i++) {
    PIN += characters[random(0, strlen(characters)-1)];
  }
  
  //Calculate the hash of the PIN
  md5.begin();
  md5.add(PIN+SECRET);
  md5.calculate();
  HASH = md5.toString();
  HASH.toUpperCase();

  //Printout...
  Serial.print("PIN: ");
  Serial.println(PIN);
  Serial.print("Hash: ");
  Serial.println(HASH);
}

void handleState() {
  //HTTP GET: /
  digitalWrite(led, 0);
  server.send(200, "text/plain", (STATE)?"on":"off");
  digitalWrite(led, 1);
}

void handleSet() {
  //HTTP GET: /set?state="on/off"
  digitalWrite(led, 0);
  String message = "";
  
  //Check if request has the correct PIN hash
  //The requester must include in the request the header 'PIN' that contains
  //the MD5 hash of the concatication of the PIN provided by the server and the SECRET
  char requestHashBuffer[34];
  char requestStateBuffer[5];
  server.header(HEADER_HASH).toCharArray(requestHashBuffer, sizeof(requestHashBuffer)-1);
  server.arg(ARG_STATE).toCharArray(requestStateBuffer, sizeof(requestStateBuffer)-1);
  String requestHash = String(requestHashBuffer);
  String requestState = String(requestStateBuffer);
  requestHash.toUpperCase();
  requestState.toUpperCase();
  Serial.println("Request Received");
  Serial.println("Request Hash: "+requestHash);
  Serial.println("Request State: "+requestState);
  
  if (requestHash.equals(HASH)){
    generatePIN();
    if (requestState.equals(ARG_STATE_ON)){
      STATE = true;
    }else{
      STATE = false;
    }
    digitalWrite(switchPin, (STATE)?1:0);
    message += "Switch state is now ";
    message += (STATE)?"on":"off";
  }else{
    message += PIN;
  }

  server.send(200, "text/plain", message);
  digitalWrite(led, 1);
}

void setup(void) {
  pinMode(led, OUTPUT);
  digitalWrite(led, 1);
  pinMode(switchPin, OUTPUT);
  digitalWrite(switchPin, 0);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  generatePIN();

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) { Serial.println("MDNS responder started"); }
  server.on("/set", handleSet);
  server.on("/", handleState);
  const char *headerKeys[] = {HEADER_HASH};
  size_t headerKeysSize = sizeof(headerKeys) / sizeof(char *);
  server.collectHeaders(headerKeys,headerKeysSize);
  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}