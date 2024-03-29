# Fiat Lux
Fiat Lux is a program that was created to run on a Raspberry Pi 4 computer on the International Space Station in the international [AstroPi](https://astro-pi.org/mission-space-lab/) project.

## What does the program do?
The main program takes pictures of the ground for 3 hours. Using the Orbit library, the program decides if it will take pictures at 17 second intervals during the day or at 23 second intervals at night. The coordinates where the photo was taken are stored in the exif of the photo. An event.log file is created in which all events are recorded (e.g. "Took photo: image_0001.jpg"). 

When saving each photo, the number of the photo, whether it was night or day, time, latitude, longitude, altitude are stored in the data.csv file. It also stores the trained model's decision whether the photo is ocean, land or dark.

## Additional programs
### [Sort.py](sort.py)
This program sorts all photos into three folders "dark", "ground" and "ocean" based on the decision of the trained model in the data.csv file. 

## What did we discover?
You can read more about our findings in final report [here](FinalReport.pdf)

## Sample of our photos
<img alt="image_0158" src="https://github.com/NewtonWasTaken/FiatLux/assets/84130106/7e548786-4e4f-4d24-97fc-4e36720a39c3" width="70%">
<br>
<a target="_blank" href="https://goo.gl/maps/MpK4MJqKmc2GTndD8">Position of the photo</a>
<br><br><br>
<img alt="image_0148" src="https://github.com/NewtonWasTaken/FiatLux/assets/84130106/4f41d377-2af9-4629-be6c-379c628a0eae" width="70%">
<br>
<a target="_blank" href="https://goo.gl/maps/JJP9SKRu8kyhXiRE8">Position of the photo</a>
<br><br><br>
<img alt="image_0092" src="https://github.com/NewtonWasTaken/FiatLux/assets/84130106/b42d3a64-3a2a-4af6-be84-62587d54aea2" width="70%">
<br>
<a target="_blank" href="https://goo.gl/maps/WtBBcjCxEUEQhoDMA">Position of the photo</a>
<br><br><br>
<img alt="image_0308" src="https://github.com/NewtonWasTaken/FiatLux/assets/84130106/8cc835ce-c2b7-4db8-a4a6-d4c454a55055" width="70%">
<br>
<a target="_blank" href="https://goo.gl/maps/x1NiutWRmxttEPKY8">Position of the photo</a>
<br><br><br>
<img alt="image_0445" src="https://github.com/NewtonWasTaken/FiatLux/assets/84130106/09a52bc9-0988-4583-9228-eab92118da18" width="70%">
<br>
<a target="_blank" href="https://goo.gl/maps/QC5ADMR1xr9VdhCd9">Position of the photo</a>
<br>
