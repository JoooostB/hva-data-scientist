from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo, MongoClient
import json
from bson import json_util
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb://localhost")
database = client["assignment-2"]
collection = database["hotel-reviews"]

projection = {"Reviewer_Score": True, "lat": True, "lng": True}
# Count amount of reviews per date
date_count = [{"$group": {"_id": "$Review_Date", "count": {"$sum": 1}}}]

@app.route("/tutorial")
def tutorial():
    #result = collection.find_one({'Hotel_Name': 'Hotel Arena'})
    return render_template("tutorial.html")


@app.route("/query")
def query():
    data = collection.aggregate(date_count)
    values = []
    try:
        for value in data:
            values.append(value)
    finally:
        print(values)
        #values = sorted(values, key=lambda x: datetime.strptime(x['_id'], "%m/%d/%Y"))
        print(values)
        labels = [y['_id'] for y in values]
        values = [y['count'] for y in values]
        #values = json.dumps(values, default=json_util.default)

    id = request.args.get('id')
    result = collection.find_one({'name': id})
    return render_template("tutorial.html", labels=json.dumps(labels), values=json.dumps(values))


@app.route("/")
def run():
    connection = MongoClient('localhost')
    collection = connection['assignment-2']['hotel-reviews']
    review_country = collection.find(projection=projection, limit=10000)
    cursor = collection.aggregate(date_count)
    json_variables = []
    # TODO Separate values and labels
    try:
        for doc in cursor:
            json_variables.append(doc)
    finally:
        json_variables = json.dumps(json_variables, default=json_util.default)
        data = {'data': json_variables}
        print(str(data))
        connection.close()
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run()
