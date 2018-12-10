# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2
import RPi.GPIO as GPIO
import SimpleMFRC522


reader = SimpleMFRC522.SimpleMFRC522()

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

 
# open the output CSV file for writing and initialize the set of
# barcodes found thus far
found = set()

# loop over the frames from the video stream
try:
  while True:
  # grab the frame from the threaded video stream and resize it to
  # have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    
    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)
    
    # loop over the detected barcodes
    for barcode in barcodes:
      # extract the bounding box location of the barcode and draw
      # the bounding box surrounding the barcode on the image
      
      # the barcode data is a bytes object so if we want to draw it
      # on our output image we need to convert it to a string first
      barcodeData = barcode.data.decode("utf-8")
      
      # draw the barcode data and barcode type on the image
      text = "Found QR Code with content: {}".format(barcodeData)
      print(text)
      print("Awaiting authentication...")
      
      _id, text = reader.read()

      print("User authenticated as {}".format(text))
      print("Equipment checkout completed successfully")
      
      # if the barcode text is currently not in our CSV file, write
      # the timestamp + barcode to disk and update the set
      if barcodeData not in found:
        found.add(barcodeData)
 
finally:
  GPIO.cleanup()
# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
csv.close()
vs.stop()
