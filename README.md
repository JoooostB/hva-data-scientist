![Logo](http://www.hva.nl/webfiles/1524744682263/img/logo.svg "Hogeschool van Amsterdam")
# Data Engineer & Data Scientist 2018
## Individual Assignment II
In this assignment we’ll use the same dataset as before. Simulating processing and analysing of a Big Data set on your machine can be done by using several libraries. The use of these libraries and their purposes will be the topic of each lesson during this block. Main goal of the second assignment can be stated as:
*“Demonstrating how machine learning can be done in a Big Data Environment”*

So, we want you to use:
* Either [all the data](https://www.kaggle.com/jiashenliu/515k-hotel-reviews-data-in-europe) from the Kaggle dataset on hotel reviews
* Or a dataset to be discussed with the teacher

Assignment goals:
1. To obtain an attractive visual representation of all the data in the dataset. With visual interactive elements to support the socalled Visualisation mantra:
  * Overview: Gain an overview of the entire collection
  * Zoom: Zoom in on items of interest
  * Filter: filter out interesting items or filter in interesting items
  * Details: On demand; select an item or group and get relevant information accordingly
2. To simulate big data and RAM problems, additional libraries are used
  * In case of R , for instance the library FFBASE 
  * In case of Python, for instance the library PyTable
(After some initial selection cleaning the result should be written away as a Review_pos.csv and Review_neg.csv)
3.	All of the  dataset is stored in a NOSQL database, for instance MONGODB. A live connection to filter data during the process of running the script should be implemented:
  * There should be a collection containing all of the data of the Kaggle dataset having the following structure
    * Hotel_Address text,
    * Hotel_Name text,
    * Lat double,
    * Lng double,
    * Average_Score double,
    * Total_Number_of_Reviews int,
    * Additional_Number_of_Scoring int,
    * Reviewer_Nationality text,
    * Review_Date text,
    * Review text,
    * Review_Word_Counts int,
    * Total_Number_of_Reviews_Reviewer_Has_Given int,
    * Reviewer_Score double,
    * Tags text,
    * Sentiment int, additional field indicating a positive Review 1, or a negative review 0
    *There should be a collection of balanced set of reviews, for instance a collection consisting of 10.000 positive and 10.000 negative reviews having a least the following structure
    * Review text,
    * Sentiment int

4.	At least one more or less advanced feature should be implemented.
  * Either the student simulates parallel processing power. For example, a sentiment analysis of the hotel reviews is solved by using Spark.
  * Or the student demonstrates state-of -the-art algorithms. For example, a prediction on the sentiment of a review using the length of the review be built using Keras
