# import the necessary packages
from imutils.video import VideoStream
from datetime import datetime
from pyzbar import pyzbar
from Scale import Scale
from Scanner import Scanner
from Auth import get_member_info
from Camera import Camera
import imutils
import time
import cv2
import RPi.GPIO as GPIO

print("Setting up...")

reader = Scanner()
scale = Scale()

print("[0/2] Taring the scale. Remove everything and press Enter.")
_ = input()
print("[0/2] Taring the scale...")
scale.tare()
print("[0/2] Scale taring complete.")

# initialize the video stream and allow the camera sensor to warm up
print("[1/2] Starting video stream...")
camera = Camera()
print("[1/2] Video stream started...")
print("[2/2] Setup complete")


try:
  while True:
    qr_code_data = None
    
    print("Waiting for QR Code")
    while qr_code_data is None:
      qr_code_data = camera.scan_qr_code()
      time.sleep(1)
    
    print("Awaiting authentication...")

    uid = None

    while uid is None:
      uid = reader.read_uid()

    ## Add timeout

    if uid is not None:
      print("Card UID is {}".format(uid))

      weight = scale.get_weight()
      image_path = "./images/{}.jpg".format(datetime.now().isoformat())
      cv2.imwrite(image_path, camera.get_image()) 
      info = get_member_info(uid)

      print("User ID: {}".format(info['MemberID']))
      print("Active: {}".format(info['Active']))
      print("Weight: {}".format(weight))
      print("Image saved to '{}'".format(image_path))
      print("Equipment checkout completed successfully")
 
finally:
  GPIO.cleanup()
# close the output CSV file do a bit of cleanup
print("[1/1] Cleaning up...")
csv.close()
vs.stop()
print("[1/1] Clean up completed successfully.")
