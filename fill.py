from constructor.db import Collection
from constructor.table import Table
import pandas as pd

review_table = Table('hotel-reviews.csv', './data/table.h5', 'hotel_reviews')
review_table.store()

positive = review_table.query('Reviewer_Score > 5.4')
negative = review_table.query('Reviewer_Score < 5.5')
positive['Sentiment'] = 1
negative['Sentiment'] = 0

positive.rename(columns={'Positive_Review': 'Review_Text'}, inplace=True)
negative.rename(columns={'Negative_Review': 'Review_Text'}, inplace=True)
positive.drop(["Negative_Review"], axis=1)
negative.drop(["Positive_Review"], axis=1)

positive.to_csv(r'./data/Review_pos.csv', index=None, header=True)
negative.to_csv(r'./data/Review_neg.csv', index=None, header=True)

df = pd.concat([positive, negative], sort=False)

Collection(df, 'hotel-reviews').fill()    # Fill mongo with new df
Collection(positive[['Review_Text', 'Sentiment']].sample(n=10000), 'pos').fill()
Collection(negative[['Review_Text', 'Sentiment']].sample(n=10000), 'neg').fill()

print(df.head())
