import logging
from time import sleep
from picamera import PiCamera
from pathlib import Path
from datetime import datetime, timedelta
import os
from logzero import logger, logfile
from orbit import ISS, ephemeris
from skyfield.api import load
import csv
from PIL import Image
from pycoral.adapters import common
from pycoral.adapters import classify
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.dataset import read_label_file


def create_data_file(data_file):
    """
    Creates a file with data and makes a first row with headers
    :param data_file: Takes file where this header should be created
    :return:
    """
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Counter", "Photo","Day", "Date/time", "Latitude", "Longitude","Elevation", "Ground", "Ocean", "Dark")
        writer.writerow(header)
        f.flush()
        os.fsync(f.fileno())

def add_data_file(data_file, data):
    """
    Adds one row of data to data file
    :param data_file: Takes data file, where the line should be added
    :param data: Takes the data, that should be written to the file
    :return:
    """
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        f.flush()
        os.fsync(f.fileno())

def recognize_image(counter):
    """
    Recognizes the image based on the trained model
    :param counter: Takes the counter of the main loop
    :return: Returns dict with results
    """
    # Here the probability from the Coral model will be stored
    results = {}

    # Changing the size of the image to fit with the model
    size = common.input_size(interpreter)
    image = Image.open(base_folder / "photos" / f"image_{counter:04d}.jpg").convert('RGB').resize(size, Image.Resampling.LANCZOS)

    # Running the rescaled image through the model
    common.set_input(interpreter, image)
    interpreter.invoke()

    # Getting the results
    classes = classify.get_classes(interpreter, top_k=3)
    labels = read_label_file(label_file)

    # Converting the results to percentage and storing it in the results dictionary
    for c in classes:
        results.update({labels.get(c.id, c.id): 100 * float(f"{c.score:.5f}")})
    image.close()

    return results


def take_photo(counter, location):
    """
    Takes photo, with asigned EXIF data
    :param counter: Takes counter from main loop
    :param location: Takes ISS.coordinates object
    :return:
    """

    # File location of the photo
    image_file = f"{base_folder}/photos/image_{counter:04d}.jpg"

    # Convert the location data to EXIF format
    south, exif_latitude = convert(location.latitude)
    west, exif_longitude = convert(location.longitude)

    # Adds the EXIF data to the photo
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # Capture the photo
    camera.capture(image_file)


def convert(angle):
    """
    Converts angle from ISS.location object to an EXIF format
    :param angle: Takes one angle from ISS.coordinates object
    :return: Returns boolean and converted angle. Boolean says if the angle is negative (True) or positive (False)
    """

    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds * 10:.0f}/10'

    return sign < 0, exif_angle


# Time when the program was started
start_time = datetime.now()

# Folder of where the main.py is stored
base_folder = Path(__file__).parent.resolve()

# Initializing folder for photos
os.mkdir(f"{base_folder}/photos")

# Initialize log
logfile(base_folder / "events.log")

# Initializing main data.csv file
main_data = base_folder/"data.csv"
create_data_file(main_data)

# Initializing camera
camera = PiCamera()
camera.resolution = (2592, 1944)

# Initializing the model for ML Coral
model_file = base_folder / 'ground-vs-ocean-model.tflite'
label_file = base_folder / 'ground-vs-ocean.txt'

# Initializing the interpreter for Coral
interpreter = make_interpreter(f"{model_file}")
interpreter.allocate_tensors()

# This counts how many times the main loop was executed
counter = 1

# Time when the main loop was last executed
now_time = datetime.now()

# Main loop of the program
while (now_time < start_time + timedelta(minutes=180-0.5)):
    try:
        # Loads the ISS location in current time
        location = ISS.coordinates()

        # Takes photo and signs the information about location into to photo
        take_photo(counter, location)
        logging.info(f"Took photo: image_{counter:04d}.jpg")

        # Recognizes the image based on the Coral model
        results = recognize_image(counter)
        logging.info(f"Processed photo image_{counter:04d}.jpg with Coral model")


        # Initializing time for checking if it is day or night
        timescale = load.timescale()
        t = timescale.now()

        # Creating one row in data.csv
        data = (counter, f"image_{counter:04d}.jpg",ISS.at(t).is_sunlit(ephemeris),datetime.now(), location.latitude.degrees, location.longitude.degrees, location.elevation.km, results["ground"], results["ocean"], results["dark"])

        # Adding the row to data.csv
        add_data_file(main_data, data)
        logging.info(f"Wrote data about photo image_{counter:04d}.jpg to data.csv")

        # Logging the loop
        logger.info(f"Completed {counter}. loop")

        # Completes cycle
        counter += 1


        # Decides if to take pictures in night or in day
        if ISS.at(t).is_sunlit(ephemeris):
            logger.info("Waiting 15 seconds for next loop")
            sleep(15)
            logger.info(f"Loop took {datetime.now() - now_time} to finish")
        else:
            logger.info("Waiting 20 seconds for next loop")
            sleep(20)
            logger.info(f"Loop took {datetime.now() - now_time} to finish")
            

        # Sets the current time
        now_time = datetime.now()

    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

camera.close()
