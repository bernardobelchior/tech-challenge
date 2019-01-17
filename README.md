# MakerSpace Asset Management System

Asset Management System for MakerSpace.

# Structure
* `MFRC5222.py` and `SimpleMFRC5222.py` are Python libraries to read/write from/to a RFID card. 
* `rfid-read.py` and `rfid-write.py` are two Python scripts useful to read/write from/to a RFID card.
* `scanner.py`: example program of how to scan a QR Code using an USB Camera.
* `stream-video-to-vlc.sh`: bash script to stream video from Raspberry Pi to another computer in the network using VLC
* `main.py`: program that represents the actual business logic of the Asset Management System

# Dependencies

* OpenCV
* RPi.GPIO
* [SPI-Py](https://github.com/lthiery/SPI-Py)
