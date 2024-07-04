DROP TABLE bankdata;
DROP TABLE yearlybalance;

-- Create a table for the input data
CREATE TABLE bankdata (age BIGINT, job STRING, marital STRING, education STRING,
  default STRING, balance BIGINT, housing STRING, loan STRING, contact STRING,
  day BIGINT, month STRING, duration BIGINT, campaign BIGINT, pdays BIGINT,
  previous BIGINT, poutcome STRING, termdeposit STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\;';

-- Load the input data
LOAD DATA LOCAL INPATH 'Data/bank.csv' INTO TABLE bankdata;

-- Report the average yearly balance for all people in each education category

CREATE TABLE yearlybalance AS
SELECT education, AVG(balance)
FROM bankdata
GROUP BY education; 

-- Dump the output to file 
INSERT OVERWRITE LOCAL DIRECTORY 'Task_1b-out'
  ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY '\t'
  STORED AS TEXTFILE
  SELECT * FROM yearlybalance;