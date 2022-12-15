from time import sleep
from picamera import PiCamera
from pathlib import Path
from datetime import datetime, timedelta
import os

#This variable should be on the very top to have the start time accurate
start_time = datetime.now()

#Folder of where the main.py is stored
base_folder = Path(__file__).parent.resolve()

#Initializing folder for photos
os.mkdir(f"{base_folder}/photos")


#Initializing main data.csv file
main_data = open(f"{base_folder}/data.csv", "w")


#Initializing camera
camera = PiCamera()
camera.resolution = (2592, 1944)

#This counts how many times the main loop was executed
counter = 0

#Time when the main loop was last executed
now_time = datetime.now()

while (now_time < start_time + timedelta(minutes=2)):
    image_file = f"{base_folder}/photos/image_{counter:04d}.jpg"
    camera.capture(image_file)
    main_data.write(f"Took image_{counter:04d}.jpg in {datetime.now()} \n")
    print(f"Took image_{counter:04d}.jpg in {datetime.now()} \n")
    counter += 1
    sleep(10)
    now_time = datetime.now()
