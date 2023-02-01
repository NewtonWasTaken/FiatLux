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


def take_photo(counter, location):
    """
    Takes photo, which has asigned the EXIF data
    :param counter: Takes counter from main loop
    :param location: Takes ISS.coordinates object
    :return:
    """

    #Location of the photo
    image_file = f"{base_folder}/photos/image_{counter:04d}.jpg"

    #Convert the location data to EXIF format
    south, exif_latitude = convert(location.latitude)
    west, exif_longitude = convert(location.longitude)

    #Adds the EXIF data to the photo
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    #Capture the photo
    camera.capture(image_file)

def convert(angle):
    """
    Converts angle from ISS.location object to an EXIF format
    :param angle: Takes one angle from ISS.coordinates object
    :return: Returns boolean and converted angle. Boolean says if the angle is negative (True) or positive (False)
    """

    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'

    return sign < 0, exif_angle


#Main loop of the program
while (now_time < start_time + timedelta(minutes=180)):
    try:
        #Loads the ISS location in current time
        location = ISS.coordinates() 

        #Takes photo and sings the information about location into to photo
        take_photo(counter, location)

        #Completes cycle
        counter += 1

        # Decides wheater to take pictures in night or in day
        timescale = load.timescale()
        t = timescale.now()
        if ISS.at(t).is_sunlit(ephemeris):
            sleep(15)
        else:
            sleep(20)

        #Sets the current time
        now_time = datetime.now()

    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')



    