from tinydb import TinyDB, Query, where
import time

MAX_TRIP_AGE_SECONDS = 10

db = TinyDB('db.json')
logs = db.table('logs')
trips = db.table('trips')

def logUltraSonic(sensorname, value):
    SENSOR_TYPE = "ULTRA_SONIC"

    logID = logs.insert(
        {
            "value": value,
            "timestamp": time.time(),
            "sensor": {
                "name": sensorname,
                "type": SENSOR_TYPE
            }
        }
    )

    addLogIdToTrip(logID)


def logNotice(sender, text):
    SENSOR_TYPE = "TEXT"

    logID = logs.insert(
        {
            "value": text,
            "timestamp": time.time(),
            "sensor": {
                "name": sender,
                "type": SENSOR_TYPE
            }
        }
    )

    addLogIdToTrip(logID)


def addLogIdToTrip(logID):
    result = trips.search(where('endDate') > time.time()-MAX_TRIP_AGE_SECONDS)
    trip = result[0] if result else None

    if trip is not None:
        tmplogs = trips.get(eid=trip.eid)['logs']
        tmplogs.append(logID)
        trips.update({
            'logs': tmplogs,
            'endDate': time.time()
        }, eids=[trip.eid])
    else:
        trips.insert(
            {
                "startDate": time.time(),
                "endDate": time.time(),
                "logs": [
                    logID
                ]
            }
        )
