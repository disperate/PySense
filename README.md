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
import pySenseLogger

pySenseLogger.logUltraSonic("SensorLeft", 3.2)
pySenseLogger.logUltraSonic("SensorRight",1.6)
pySenseLogger.logNotice("LoggerTest", "message")
```
The first value of the log function is the sensor name. It may be chosen freely.

To analyse the logs, start the server:
```python 
python pysense.py
```
Your trips should now be available at [http://localhost:5000/](http://localhost:5000/)
