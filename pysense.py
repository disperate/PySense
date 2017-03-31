from flask import Flask, jsonify, url_for, redirect, request, render_template, send_from_directory
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from bson import json_util, ObjectId
import json

app = Flask(__name__, static_folder="static")
app.config["MONGO_DBNAME"] = "pysense"
mongo = PyMongo(app, config_prefix='MONGO')
APP_URL = "http://127.0.0.1:5000"


class Log(Resource):
    def get(self):
        data = []
        cursor = mongo.db.log.find()
        for log in cursor:
            data.append(log)

        return json.loads(json_util.dumps({"response": data}))


class Trip(Resource):
    def get(self, trip_id=None):
        data = []

        if trip_id:

            trip = mongo.db.trip.aggregate(
                [
                    {"$match": {"_id": ObjectId(trip_id)}},
                    { "$unwind": "$logs" },
                    {"$lookup": {"from": "log", "localField": "logs", "foreignField": "_id", "as": "logData"}},
                    {"$project":
                        {
                            "_id": 1,
                            "startDate": 1,
                            "endDate": 1,
                            "logData": 1
                        }
                    }

                ])
            if trip:
                data.append(trip)
            else:
                data.append("no trip found for {}".format(trip_id))
        else:
            trip = mongo.db.trip.aggregate(
                [
                    {"$project": {"_id": 1, "startDate": 1, "endDate": 1, "measurementCount": {"$size": "$logs"}}}
                ])
            data.append(trip)

        return json.loads(json_util.dumps(data))


@app.route("/")
def static_index():
    return render_template("index.html")


@app.route("/trip/<trip_id>")
def static_trip(trip_id):
    return render_template("trip.html")


api = Api(app)
api.add_resource(Log, "/api/logs", endpoint="logs")
api.add_resource(Trip, "/api/trips", endpoint="trips")
api.add_resource(Trip, "/api/trips/<string:trip_id>", endpoint="id")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
