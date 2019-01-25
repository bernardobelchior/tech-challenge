# import the necessary packages
from imutils.video import VideoStream
from datetime import datetime
from pyzbar import pyzbar
from Scale import Scale
from Scanner import Scanner
from Auth import get_member_info
from Camera import Camera
from SnipeIT import SnipeIT
from Display import Display
from urllib.parse import unquote
import logging
import imutils
from time import sleep
import cv2
import RPi.GPIO as GPIO

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

display = Display()

print("[0/2] Starting setup...")
display.print("[0/2] Setup\n\rstarted")

snipe_it = SnipeIT()
reader = Scanner()
scale = Scale()

print("[0/2] Taring the scale. Remove everything and press Enter.")
_ = input()
print("[0/2] Taring the scale...")
scale.tare()
print("[1/2] Scale taring complete.")

# initialize the video stream and allow the camera sensor to warm up
print("[1/2] Starting video stream...")
camera = Camera()
print("[2/2] Video stream started...")
print("[2/2] Setup complete")
display.print("[2/2] Setup\n\rcomplete")

try:
  while True:
    asset_id = None
    
    display.print("Place kit\n\runder camera")
    print("Waiting for QR Code")
    while asset_id is None:
      asset_id = camera.scan_qr_code()
      sleep(1)

    logging.debug('Asset ID: {}'.format(asset_id))

    last_activity = snipe_it.get_asset_last_activity(asset_id)

    if last_activity is None:
        display.print("QR Code not\n\rrecognized. Try again.")
        logging.error("QR Code does not belong to an asset.")
        continue

    uid = None

    display.print("Place your\n\rcard")
    print("Awaiting authentication...")

    while uid is None:
      uid = reader.read_uid()

    ## TODO: Add timeout

    if uid is not None:
      logging.debug("Card UID is {}".format(uid))

      weight = scale.get_weight()
      image_path = "./images/{}.jpg".format(datetime.now().isoformat())
      cv2.imwrite(image_path, camera.get_image()) 
      member_id = int(get_member_info(uid)['MemberID'])

      if last_activity.get('note') is not None:
        last_weight = last_activity['note'].get('weight')

        if last_weight is not None:
            if abs((float(last_weight) - weight) / float(last_weight)) > 0.05:
                print('Aborting checkin/checkout process due to max weight difference exceeded. Last weight: {}. New weight: {}'.format(last_weight, weight))
                display.print("Failure: weight\n\rdiff exceeded.")

                sleep(3)
                continue

      # An activity's action_type can be 'checkout', 'checkin from' or others.
      # As such, we can't just rely on the last activity, but have to check them
      # all until we find one that is either check in or check out.
      if last_activity['action_type'] == 'checkout':
        if snipe_it.checkin(asset_id, weight, image_path):
          display.print("Checkin\n\rsuccessful")
          print("Equipment checkin completed successfully.")
        else:
          display.print("Checkin\n\rfailed")
          print("Equipment checkin failed.")
      else:
        if snipe_it.checkout(asset_id, member_id, weight, image_path):
          display.print("Checkout\n\rsuccessful")
          print("Equipment checkout completed successfully")
        else: 
          display.print("Checkout\n\rfailed")
          print("Equipment checkout failed")
      
      sleep(3)
 
finally:
  display.print("[0/1] Cleaning\n\rup...")
  print("[0/1] Cleaning up...")
  GPIO.cleanup()
  print("[1/1] Clean up completed successfully.")

