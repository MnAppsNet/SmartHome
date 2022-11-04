import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import time
from PIL import Image, ImageDraw, ImageFont

'''
This script is working with an SD1306 OLED display with size 128x64.
The size can be changed from within the constructor
'''

class Display():
    def __init__(self,font='',imageRotation = 180):
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

    def _get_image(self):
        if self.image is None:
            self.image = Image.new('1', (self.width, self.height))
            return self.image
        else:
            return self.image

    def writeText(self,text,fontSize = 12,spaceAfterLine = 2):
        if self.font != '':
            font = ImageFont.truetype(self.font, fontSize)
        else:
            font = ImageFont.load_default()
        self.image = self._get_image()
        draw = ImageDraw.Draw(self.image)
        draw.text((0, self.y),text,  font=font, fill=255)
        _,_,_,height = font.getbbox(text)
        self.y += height + spaceAfterLine

    def flush(self):
        if self.image == None:
            return
        self.image = self.image.rotate(self.rotation)
        #Show image :
        self.disp.clear()
        self.disp.image(self.image)
        self.disp.display()
        self.image = None
        self.y = 0

    def clear(self):
        self.disp.clear()
        self.image = None

class TemperatureAndHumidityScreen(Display):
    def __init__(self,font='',imageRotation = 180):
        self._parent = super(TemperatureAndHumidityScreen, self)
        self._parent.__init__(font,imageRotation)

    def showData(self,humidity,temperature):
        lastUpdateText = Texts.getLastUpdateTimeText()
        humidityText = Texts.getLastUpdateTimeText(humidity)
        temperatureText = Texts.getLastUpdateTimeText(temperature)
        self._parent.writeText(lastUpdateText,8)
        self._parent.writeText(temperatureText,12)
        self._parent.writeText(humidityText,14)
        self._parent.flush()

class Texts:
    def getLastUpdateTimeText():
        #Set time zone
        time.environ['TZ'] = 'Europe/Athens'
        try:
            time.tzset()
        except:
            pass #System is not UNIX
        return "Last update: {0}".format(time.strftime("%H:%M:%S"))

    def getTemperatureText(temperature):
        return "Temperature: {0:0.1f}".format(temperature)

    def getHumidityText(humidity):
        return "Humidity: {0:0.1f}".format(humidity)