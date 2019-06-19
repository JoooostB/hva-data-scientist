from constructor.db import Collection
from constructor.table import Table

coll = Collection('/Users/joost/PycharmProjects/hva-data-scientist/hotel-reviews.csv', 'hotel-reviews')
coll.fill()

review_table = Table('hotel-reviews.csv', './data/table.h5', 'hotel_reviews')
review_table.store()
