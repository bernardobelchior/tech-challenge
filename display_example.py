#Include libraries
import RPi.GPIO as GPIO 
import time
from RPLCD.gpio import CharLCD

# Configure the LCD
lcd = CharLCD(pin_rs = 38, pin_rw = None, pin_e = 40, pins_data = [36,18,16,12], 
        numbering_mode = GPIO.BOARD)

# Create a variable ‘number’ 
number = 0

lcd.clear()
lcd.write_string("Wacky Assets")

# Main loop
while(True):
    # Increment the number and then print it to the LCD number = number + 1
    number += 1
    lcd.clear()
    lcd.write_string("Count: " + str(number))
    print(str(number))
    time.sleep(1) 

lcd.close() 
GPIO.cleanup()
