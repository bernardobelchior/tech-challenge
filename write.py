#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522

writer = SimpleMFRC522.SimpleMFRC522()

try:
    text = input('New data:')
    print("Now place your tag to write")
    writer.write(text)
    print("Written")
finally:
    GPIO.cleanup()
