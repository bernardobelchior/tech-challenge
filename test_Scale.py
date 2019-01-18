import RPi.GPIO as GPIO
import time
import sys
from src.Scale import Scale

scale = Scale()

print("Taring...")

scale.tare()

print("Taring complete")

while True:
    print(scale.get_weight())
    time.sleep(1)
