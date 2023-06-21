import csv
import os
from logzero import logger
from pathlib import Path


# Folder of where the main.py is stored
base_folder = Path(__file__).parent.resolve()

# Creates directories to move the photos
os.mkdir(f"{base_folder}/ocean")
os.mkdir(f"{base_folder}/ground")
os.mkdir(f"{base_folder}/dark")


# Opens data.csv
with open("data.csv", "r") as f:
    reader = csv.reader(f)

    # Loops through the data.csv
    for row in reader:

        # Skipping the first line with heading
        if row[1] == "Photo":
            continue
        else:
            image_name = row[1]

            # Extracting from data.csv to data dictionary
            data = {"ground": row[7], "ocean": row[8], "dark": row[9]}
            logger.info(f"Gathered following data from file: \n{data}")

            # Sorting the data dictionary from the highest value to the lowest
            sorted_data = sorted(data.items(), key=lambda item: float(item[1]), reverse=True)
            logger.info(f"Sorted the data desciding: \n{sorted_data}")

            # Moves the current photo based on the decision from Coral model
            os.replace(f"{base_folder}/photos/{image_name}", f"{base_folder}/{sorted_data[0][0]}/{image_name}")
            logger.info(f"Moved {image_name} to {sorted_data[0][0]} folder.\n")
