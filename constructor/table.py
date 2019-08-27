import pandas as pd
from os import path, remove


class Table:
    def __init__(self, csv_file, hdf_file, hdf_key, df_cols_to_index=True):
        self.csv_file = csv_file
        self.hdf_file = hdf_file
        self.hdf_key = hdf_key
        self.df_cols_to_index = df_cols_to_index

    def store(self):
        # Delete hdf file if it exists already.
        if path.exists(self.hdf_file):
            try:
                remove(self.hdf_file)
            except OSError:
                pass
        store = pd.HDFStore(self.hdf_file)
        for chunk in pd.read_csv(self.csv_file, chunksize=500000):
            # don't index data columns in each iteration
            store.append(self.hdf_key, chunk, data_columns=self.df_cols_to_index, index=False)
        # index data columns in HDFStore
        store.create_table_index(self.hdf_key, columns=self.df_cols_to_index, optlevel=9, kind='full')
        store.close()
        return store

    def query(self, query):
        read = pd.HDFStore(self.hdf_file, mode='r').get(self.hdf_key)
        return read.query(query)

    @staticmethod
    def add_sentiment(df, value):
        df['Sentiment'] = value
