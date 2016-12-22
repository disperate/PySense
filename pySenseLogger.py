from pymongo import MongoClient
import datetime

MAX_TRIP_AGE_SECONDS = 10

client = MongoClient()
db = client.pysense


def logUltraSonic(sensorname, value):
    SENSOR_TYPE = "ULTRA_SONIC"

    logID = db.log.insert_one(
        {
            "value": value,
            "date": datetime.datetime.utcnow(),
            "sensor": {
                "name": sensorname,
                "type": SENSOR_TYPE
            }
        }
    ).inserted_id

    addLogIdToTrip(logID)


def logNotice(sender, text):
    SENSOR_TYPE = "TEXT"

    logID = db.log.insert_one(
        {
            "value": text,
            "date": datetime.datetime.utcnow(),
            "sensor": {
                "name": sender,
                "type": SENSOR_TYPE
            }
        }
    ).inserted_id

    addLogIdToTrip(logID)


def addLogIdToTrip(logID):

    filterDate = getMaxTripAgeTime()

    trip = db.trip.find_one({"endDate": {"$gt": filterDate}})

    if trip is not None:
        db.trip.update({'_id': trip['_id']}, {
            '$addToSet': {'logs': logID},
            '$set': {"endDate": datetime.datetime.utcnow()}
        })
    else:
        db.trip.insert_one(
            {
                "startDate": datetime.datetime.utcnow(),
                "endDate": datetime.datetime.utcnow(),
                "logs": [
                    logID
                ]
            }
        )


def getMaxTripAgeTime():
    dateNow = datetime.datetime.utcnow()
    return dateNow + datetime.timedelta(seconds=-MAX_TRIP_AGE_SECONDS)