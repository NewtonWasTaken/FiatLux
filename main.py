from time import sleep
from picamera import PiCamera
from pathlib import Path
from datetime import datetime, timedelta

#This variable should be on the very top to have the start time accurate
start_time = datetime.now()

#Folder of where the main.py is stored
base_folder = Path(__file__).parent.resolve()

#Initializing main data.csv file
main_data = open(f"{base_folder}/data.csv", "w")


#Initializing camera
camera = PiCamera()
camera.resolution = (2592, 1944)

#This counts how many times the main loop was executed
counter = 0

#This variable should be as closest to main loop, time when the main loop is started
now_time = datetime.now()

while now_time < start_time + timedelta(minutes=2):
    image_file = f"{base_folder}/photos/image_{counter:04d}.jpg"
    main_data.write(f"Took image_{counter:04d}.jpg in {datetime.now()}")
    counter += 1
    sleep(10)
