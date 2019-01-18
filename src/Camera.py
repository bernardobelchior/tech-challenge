# import the necessary packages
from imutils.video import VideoStream
from datetime import datetime
from pyzbar import pyzbar
from Scanner import Scanner
from Scale import Scale
import imutils
import time
import cv2
import RPi.GPIO as GPIO

class Camera():
  def __init__(self):
    self.vs = VideoStream(src=0).start()
    time.sleep(2.0)

  def scan_qr_code(self):
    frame = self.vs.read()
    barcodes = pyzbar.decode(frame)

    if len(barcodes) > 0:
      return barcodes[0].data.decode("utf-8")
    else:
      return None

  def get_image(self):
    return self.vs.read()

  def __del__(self):
    self.vs.stop()
