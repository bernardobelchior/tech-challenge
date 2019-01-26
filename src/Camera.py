from imutils.video import VideoStream
from pyzbar import pyzbar
import time
import cv2

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
    """Returns the image as bytes and encoded as PNG."""
    return cv2.imencode(".png", self.vs.read())[1].tobytes()

  def __del__(self):
    self.vs.stop()
