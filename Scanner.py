#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
from lib import MFRC522

class Scanner():
    def __init__(self):
        self.reader = MFRC522.MFRC522()


    def read_uid(self):    
        # Scan for cards    
        (status,TagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
    
        # If a card is found
        if status == self.reader.MI_OK:
            print( "Card detected")
        
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
                print( "Authentication error")
