from flask import Flask, render_template
from pymongo import MongoClient
import json
from bson import json_util

app = Flask(__name__)

projection = {"Reviewer_Score": True, "lat": True, "lng": True}
# Count amount of reviews per date
date_count = [
    {"$group": {"_id": "$Review_Date", "count": {"$sum": 1 } } }
]


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


@app.route("/pie")
def pie():
    labels = 1
    values = 2


if __name__ == "__main__":
    app.run()
