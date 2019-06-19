from pymongo import MongoClient
import pandas as pd
import os
import json


class Collection:
    def __init__(self, path, collection):
        self.client = MongoClient('mongodb://localhost:27017')  # Init mongoclient
        self.db = self.client['assignment-2']  # Assign db name
        self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
        self.collection = collection
        self.conn = self.db[self.collection]

    def fill(self):
        data = pd.read_csv(self.path)
        json_data = json.loads(data.to_json(orient='records'))
        self.conn.delete_many({ })    # Clear collection using an empty filter.
        self.conn.insert_many(json_data)
