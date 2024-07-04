In this project, I'll be doing some analytics on real Twitter data. The data is stored in a tab (“\t”) delimited format and contains the following attributes:

* tokenType: In our data set all rows have Token type of hashtag. 
* month: The year and month specified like the following: YYYYMM. So 4 digits for year followed by 2 digits for month. So like the following 200905, meaning the year 2009 and month of May.
* count: An integer representing the number tweets of this hash tag for the given year and month.
* hashtagName: The #tag name, e.g. babylove, mydate, etc.

The full twitter.tsv is too large to be uploaded to GitHub, so I have included a smaller version of it for demonstration purposes.

Data source: http://www.infochimps.com/datasets/twitter-census-conversation-metrics-one-year-of-urls-hashtags-sm. 

I'll be using HiveQL and SparkRDD to perform the following tasks:

* Task 2a. [Spark RDD] Find the single row that has the highest count and for that row report the month, count and hashtag name.
* Task 2b. [Do twice, once using Hive and once using Spark RDD] Find the hash tag name that was tweeted the most in the entire data set across all months. Report the total number of tweets for that hash tag name.
* Task 2c. [Spark RDD] Given two months x and y, where y > x, find the hashtag name that has increased the number of tweets the most from month x to month y. Ignore the tweets in the months between x and y, so just compare the number of tweets at month x and at month y. Report the hashtag name, the number of tweets in months x and y. Ignore any hashtag names that had no tweets in either month x or y. Assume that the combination of hashtag and month is unique.

