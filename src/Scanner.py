import RPi.GPIO as GPIO
from lib.MFRC522 import MFRC522

class Scanner():
    def __init__(self):
        self.reader = MFRC522()


    def read_uid(self):    
        # Scan for cards    
        (status,TagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
    
        # If a card is found
        if status == self.reader.MI_OK:
            print("Card detected")
        
        # Get the UID of the card
        (status,uid) = self.reader.MFRC522_Anticoll()
    
        # If we have the UID, continue
        if status == self.reader.MI_OK:
    
            card_uid = '{:02X}{:02X}{:02X}{:02X}'.format(uid[0], uid[1], uid[2], uid[3])
            return card_uid
        
            # This is the default key for authentication
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
            
            # Select the scanned tag
            self.reader.MFRC522_SelectTag(uid)
    
            # Authenticate
            status = self.reader.MFRC522_Auth(self.reader.PICC_AUTHENT1A, 8, key, uid)
    
            # Check if authenticated
            if status == self.reader.MI_OK:
                self.reader.MFRC522_Read(8)
                self.reader.MFRC522_StopCrypto1()
            else:
                print("Authentication error")
