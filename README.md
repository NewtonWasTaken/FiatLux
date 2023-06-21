# Fiat Lux
Fiat Lux is a program that was created to run on a Raspberry Pi 4 computer on the International Space Station in the international [AstroPi](https://astro-pi.org/mission-space-lab/) project.

## What does the program do?
The main program takes pictures of the ground for 3 hours. Using the Orbit library, the program decides if it will take pictures at 17 second intervals during the day or at 23 second intervals at night. The coordinates where the photo was taken are stored in the exif of the photo. An event.log file is created in which all events are recorded (e.g. "Took photo: image_0001.jpg"). 

When saving each photo, the number of the photo, whether it was night or day, time, latitude, longitude, altitude are stored in the data.csv file. It also stores the trained model's decision whether the photo is ocean, land or dark.

## Additional programs
### [Sort.py](sort.py)
This program sorts all photos into three folders "dark", "ground" and "ocean" based on the decision of the trained model in the data.csv file. 

## Sample of our photos
<img alt="image_0158" src="https://github.com/NewtonWasTaken/FiatLux/assets/84130106/507bae04-8401-4e60-b6e9-0abfb15332b5" width="70%">
<img alt="image_0148" src="https://github.com/NewtonWasTaken/FiatLux/assets/84130106/39b61dea-9de8-4bf2-9824-06adb420805a" width="70%">
<img alt="image_0092" src="https://github.com/NewtonWasTaken/FiatLux/assets/84130106/c1cba8ea-6047-48ba-ae46-0b3840391953" width="70%">
<img alt="image_0308" src="https://github.com/NewtonWasTaken/FiatLux/assets/84130106/166b0a5f-5020-43a6-b887-469d7dcecd5d" width="70%">
<img alt="image_0445" src="https://github.com/NewtonWasTaken/FiatLux/assets/84130106/a75e3e32-9787-48b5-9659-88d13aaff2e3" width="70%">