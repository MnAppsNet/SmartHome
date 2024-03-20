try:
    import Adafruit_GPIO.SPI as SPI
    import Adafruit_SSD1306
except: pass
import time
from PIL import Image, ImageDraw, ImageFont

'''
This script is working with an SD1306 OLED display with size 128x64.
The size can be changed from within the constructor
'''

class Display():
    def __init__(self,font='',imageRotation = 180):
        try:
            self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=None) #< Change this if you have a different size screen
            self.disp.begin()
            self.disp.clear()
            self.disp.display()
            self.width = self.disp.width
            self.height = self.disp.height
            self.font = font
            self.y = -1 * self.disp.height
            self.image = None
            self.rotation = imageRotation
        except:
            self.disp = None
            self.image = None

    def _get_image(self):
        if self.image is None:
            self.image = Image.new('1', (self.width, self.height))
            return self.image
        else:
            return self.image

    def writeText(self,text,fontSize = 12,spaceAfterLine = 2):
        if self.disp == None:
            print(text)
            return
        if self.font != None and self.font != '':
            font = ImageFont.truetype(self.font, fontSize)
        else:
            font = ImageFont.load_default()
        self.image = self._get_image()
        draw = ImageDraw.Draw(self.image)
        draw.text((0, self.y),text,  font=font, fill=255)
        _,_,_,height = font.getbbox(text)
        self.y += height + spaceAfterLine
        print(text);

    def flush(self):
        if self.image == None: return
        self.image = self.image.rotate(self.rotation)
        #Show image :
        self.disp.clear()
        self.disp.image(self.image)
        self.disp.display()
        self.image = None
        self.y = 0

    def clear(self):
        if self.disp == None: return
        self.disp.clear()
        self.image = None

class TemperatureAndHumidityScreen(Display):
    def __init__(self,font='',imageRotation = 180):
        self._parent = super(TemperatureAndHumidityScreen, self)
        self._parent.__init__(font,imageRotation)

    def showData(self,humidity,temperature,thermostatState):
        lastUpdateText = Texts.getLastUpdateTimeText()
        humidityText = Texts.getHumidityText(humidity)
        temperatureText = Texts.getTemperatureText(temperature)
        thermostat = Texts.getThermostatState(thermostatState)
        self._parent.writeText(lastUpdateText,12)
        self._parent.writeText(temperatureText,12)
        self._parent.writeText(humidityText,12)
        self._parent.writeText(thermostat,12)
        self._parent.flush()

class Texts:
    def getLastUpdateTimeText():
        return "Last update: {0}".format(time.strftime("%H:%M:%S"))

    def getTemperatureText(temperature):
        return "Temperature: {0:0.1f}".format(temperature)

    def getHumidityText(humidity):
        return "Humidity: {0:0.1f}".format(humidity)

    def getThermostatState(state):
        return "Thermostat: {}".format("On" if state else "Off")