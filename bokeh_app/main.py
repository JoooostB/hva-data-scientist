# Pandas and PyMongo for data management
import pandas as pd
import pymongo

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from scripts.count import count_tab
from scripts.sentiment import sentiment_tab
from scripts.geo import geo_tab
from scripts.input import input_tab

# Make Database Connection
client = pymongo.MongoClient('localhost', 27017)
db = client['assignment-2']
coll = db['hotel-reviews']


def iterator2dataframe(iterator, chunk_size: int):
    """
    The following function is added to meet requirement 3:
    Simulate Big Data & RAM problems.

    This function will import the iterator (a list of the collection)
    and chunks them in a set chunk_size. At the end the df's are concatted
    back together.

    """
    records = []
    frames = []
    for i, record in enumerate(iterator):
        records.append(record)
        if i % chunk_size == chunk_size - 1:
            frames.append(pd.DataFrame(records))
            records = []
    if records:
        frames.append(pd.DataFrame(records))
    return pd.concat(frames)


df = iterator2dataframe(list(coll.find()), 25000)
df = df.drop(columns="_id")

tab1 = count_tab(df)
tab2 = sentiment_tab(df)
tab3 = geo_tab(df)
tab4 = input_tab()

tabs = Tabs(tabs=[tab1, tab2, tab3, tab4])
curdoc().add_root(tabs)

