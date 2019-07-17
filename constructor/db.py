from pymongo import MongoClient


class Collection:
    def __init__(self, df, collection):
        self.client = MongoClient('mongodb://mongodb:27017')  # Init mongoclient
        self.db = self.client['assignment-2']  # Assign db name
        self.df = df
        self.collection = collection
        self.conn = self.db[self.collection]

    def fill(self):
        dict = self.df.to_dict(orient='records')
        self.conn.delete_many({ })    # Clear collection using an empty filter.
        self.conn.insert_many(dict)
