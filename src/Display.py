import RPi.GPIO as GPIO 
from RPLCD.gpio import CharLCD

COLS=16
ROWS=2

class Display():
    def __init__(self):
        # Configure the LCD
        self.lcd = CharLCD(pin_rs = 38, pin_rw = None, pin_e = 40, pins_data = [36,18,16,12], numbering_mode = GPIO.BOARD, auto_linebreaks=False, cols=COLS, rows=ROWS)

    def print(self, string):
        if len(string) > COLS*ROWS:
            print('WARNING: String \'{}\' too big and overflows the display.'.format(string))

        self.lcd.clear()
        self.lcd.write_string(string)

    def __del__(self):
        self.lcd.close() 
