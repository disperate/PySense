from flask import Flask, jsonify, url_for, redirect, request, render_template, send_from_directory
from flask_restful import Api, Resource
import json
from tinydb import TinyDB, Query

db = TinyDB('db.json')
logs = db.table('logs')
trips = db.table('trips')

app = Flask(__name__, static_folder="static")
APP_URL = "http://127.0.0.1:5000"

class Log(Resource):
    def get(self):
        data = []
        cursor = logs.all()
        for log in cursor:
            data.append(log)

        return {"response": data}


class Trip(Resource):
    def get(self, trip_id=None):
        data = []

        if trip_id:
            trip = trips.get(eid=int(trip_id))

            if trip:
                triplogs = []
                for log_id in trip['logs']:
                    triplogs.append(logs.get(eid=int(log_id)))

                trip['logs'] = triplogs
                return trip
            else:
               return "no trip found for {}".format(trip_id)
        else:
            data = []
            for trip in trips.all():
                trip['id'] = trip.eid
                trip['measurementCount'] = len(trip['logs'])
                data.append(trip)
            return data


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
