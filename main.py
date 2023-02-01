from time import sleep
from picamera import PiCamera
from pathlib import Path
from datetime import datetime, timedelta
import os
from logzero import logger, logfile
from orbit import ISS, ephemeris
from skyfield.api import load

#This variable should be on the very top to have the start time accurate
start_time = datetime.now()

#Folder of where the main.py is stored
base_folder = Path(__file__).parent.resolve()

#Initializing folder for photos
os.mkdir(f"{base_folder}/photos")

#Initialize log
logfile(base_folder/"events.log")

#Initializing main data.csv file
main_data = open(f"{base_folder}/data.csv", "w")


#Initializing camera
camera = PiCamera()
camera.resolution = (2592, 1944)

#This counts how many times the main loop was executed
counter = 0

#Time when the main loop was last executed
now_time = datetime.now()


#Main loop of the program
while (now_time < start_time + timedelta(minutes=180)):
    try:  
        location = ISS.coordinates() 
        
        take_photo(counter, location)

        counter += 1
        timescale = load.timescale()
        t = timescale.now()
        if ISS.at(t).is_sunlit(ephemeris):
            sleep(15)
        else:
            sleep(20)
        now_time = datetime.now()

    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

#Takes photo and logs it into files
def take_photo(counter, location):
    image_file = f"{base_folder}/photos/image_{counter:04d}.jpg"
    camera.capture(image_file)
    