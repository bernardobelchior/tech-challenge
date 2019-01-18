import RPi.GPIO as GPIO
import signal
from lib.hx711 import HX711

class Scale():
    def __init__(self):
        self.scale = HX711(29, 31)
        self.scale.set_reading_format("MSB", "MSB")
        self.scale.set_reference_unit(400.614754098)
        #self.scale.reset()

    def tare(self):
        self.scale.tare()

    def get_weight(self):
        value = self.scale.get_weight(10)

        ## Needed??
        #self.scale.power_down()
        #self.scale.power_up()

        return value

