import findspark
import pyspark
import requests
from pyspark.sql import SQLContext, HiveContext
from pyspark.sql import functions as fn
from pyspark.ml.feature import RegexTokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import CountVectorizer
from pyspark.ml import Pipeline
from pyspark.ml.feature import IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

conf = pyspark.SparkConf().\
    setAppName('hva-data-scientist').\
    setMaster('local[*]')

sc = pyspark.SparkContext(conf=conf)
sqlContext = HiveContext(sc)

findspark.init()


class Spark:
    def __init__(self):
        # Convert Pandas dataframe to PySpark dataframe.
        df = sqlContext.read.format("csv").option("header", "true").load("hotel-reviews.csv")
        # df = sqlContext.createDataFrame(pandas_df)

        # Change Reviewer_Score in Sentiment value (1 <= 5.5, 0 < 5.5)
        df = df.withColumn('Reviewer_Score', fn.when(df.Reviewer_Score >= 7.0, 1).otherwise(0))
        df = df.withColumnRenamed('Reviewer_Score', 'Sentiment')

        # Concatenate the negative and positive to a single review text
        df_with_text = df.withColumn('Review_Text',
                                     fn.concat(fn.col('Negative_Review'), fn.lit(' '), fn.col('Positive_Review')))

        # Strip Dataframe to only what is necessary for sentiment analysis
        df_stripped = df_with_text.select('Negative_Review', 'Positive_Review', 'Review_Text', 'Sentiment')

        # Importing Stopwords to filter out of the reviews to exclude stopwords
        stop_words = requests.get('http://ir.dcs.gla.ac.uk/resources/linguistic_utils/stop_words').text.split()

        # Configure tokenizer to extract words with only letters and save in column words
        tokenizer = RegexTokenizer().setGaps(False) \
            .setPattern("\\p{L}+") \
            .setInputCol("Review_Text") \
            .setOutputCol("words")

        # Configure stopwords filter
        sw_filter = StopWordsRemover() \
            .setStopWords(stop_words) \
            .setCaseSensitive(False) \
            .setInputCol("words") \
            .setOutputCol("filtered")

        cv = CountVectorizer(minTF=1., minDF=5., vocabSize=2 ** 17) \
            .setInputCol("filtered") \
            .setOutputCol("tf")

        # Create Pipeline with Tokenizer, Stopwords Filter and CountVectorizer
        cv_pipeline = Pipeline(stages=[tokenizer, sw_filter, cv]).fit(df_stripped)

        # Configure TFIDF
        idf = IDF(). \
            setInputCol('tf'). \
            setOutputCol('tfidf')

        idf_pipeline = Pipeline(stages=[cv_pipeline, idf]).fit(df_stripped)

        # Split data into training, validation and testing data (60%, 30%, 10%)
        training_df, validation_df, testing_df = df_stripped.randomSplit([0.6, 0.3, 0.1], seed=0)

        # Configure LogisticRegression for analysis of the reviews
        lr = LogisticRegression(). \
            setLabelCol('Sentiment'). \
            setFeaturesCol('tfidf'). \
            setRegParam(0.0). \
            setMaxIter(100). \
            setElasticNetParam(0.)

        # Create new Pipelines for the LogisticRegression and train the model
        self.model = Pipeline(stages=[idf_pipeline, lr]).fit(training_df)

        # Calculate Score of our Model using the validation Dataframe
        self.model.transform(validation_df). \
            select(fn.expr('float(prediction = Sentiment)').alias('correct')). \
            select(fn.avg('correct')).show()

        spark = SparkSession \
            .builder \
            .appName("user_input_analysis") \
            .getOrCreate()

    def user_input(self, userinput):
        if userinput:
            usersentiment = {'text': userinput}
            df_userinput = sqlContext.createDataFrame([usersentiment])
            result_df = self.model.transform(df_userinput.withColumnRenamed('text', 'Review_Text')).select('Review_Text',
                                                                                                  'prediction')
            result_df.show()

            result = str(result_df.collect()[0][1])
            print("Result is " + result)

            #if result == "1.0":
            if "1.0" in result:
                print("Your review is positive!")
                return True
            else:
                print("Your review is negative!")
                return False
        else:
            print("No user input was given")


