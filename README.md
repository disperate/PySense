# PySense
PySense – Web Based Sensor Analysis

## Prerequisite
Install mongodb 3.2+
## Install Dependencies
```python
pip install –r requirements.txt
```

## Usage
Log data with these commands:
```python 
import pySenseLogger as log

log.logUltraSonic("SensorLeft", 3.2)
log.logUltraSonic("SensorRight",1.6)
log.logNotice("LoggerTest", "message")

log.img(cv_img_array, "message")
log.stream(cv_img_array)
```

To analyse the logs, start the server:
```python 
python pysense.py
```
Your trips should now be available at [http://localhost:5000/](http://localhost:5000/)
