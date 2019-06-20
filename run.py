from constructor.db import Collection
from constructor.table import Table

review_table = Table('hotel-reviews.csv', './data/table.h5', 'hotel_reviews')
review_table.store()
positive = review_table.query('Reviewer_Score > 5.4')
#positive.rename(columns={'Positive_Review': 'Review_Text'})
print(positive)
positive.drop(['Negative_Review'])
positive['Sentiment'] = 1


negative = review_table.query('Reviewer_Score < 5.5')
negative.rename(columns={'Negative_Review': 'Review_Text'})
negative.drop(['Positive_Review'])
negative['Sentiment'] = 0

positive.to_csv(r'./data/Review_pos.csv', index=None, header=True)
negative.to_csv(r'./data/Review_neg.csv', index=None, header=True)

df = pd.concat([positive, negative])    # Combine dataframes after adding sentiment
Collection(df, 'hotel-reviews').fill()    # Fill mongo with new df
Collection(positive[['Review_Text', 'Sentiment']].sample(n=10000), 'pos').fill()
Collection(negative[['Review_Text', 'Sentiment']].sample(n=10000), 'neg').fill()

print(df.head())


