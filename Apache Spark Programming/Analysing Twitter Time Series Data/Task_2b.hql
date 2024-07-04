DROP TABLE twitterdata;

-- Create a table for the input data
CREATE TABLE twitterdata (tokenType STRING, month STRING, count BIGINT,
  hashtagName STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

-- Load the input data
LOAD DATA LOCAL INPATH 'Data/twitter.tsv' INTO TABLE twitterdata;

-- Find hashtag name that was tweeted the most in the entire data set across all months

SELECT hashtagName, SUM(count) as numtweets
FROM twitterdata
GROUP BY hashtagName
ORDER BY numtweets DESC
LIMIT 1;

INSERT OVERWRITE LOCAL DIRECTORY 'Task_2b-out'
  ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY '\t'
  STORED AS TEXTFILE
  SELECT * FROM hashtagCount;