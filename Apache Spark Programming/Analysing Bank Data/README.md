In this project, I'll be doing some analytics on real data from a Portuguese banking institution. The data is stored in a semicolon (“;”) delimited format. Data source: http://archive.ics.uci.edu/ml/datasets/Bank+Marketing. 

I'll be using HiveQL and Spark RDD to perform the following tasks:
* Task 1a. [Hive] Report the number of clients of each job category. Write the results to “Task_1a-out”.
* Task 1b. [Hive] Report the average yearly balance for all people in each education category. Write the results to “Task_1b-out”.
* Task 1c. [Spark RDD] Group balance into the following three categories:
  a. Low: -infinity to 500
  b. Medium: 501 to 1500 =>
  c. High: 1501 to +infinity
Report the number of people in each of the above categories. Write the results to “Task_1c-out” in text file format.
* Task 1d. [Spark RDD] Sort all people in ascending order of education. For people with the same education, sort them in descending order by balance. For each person, report the following attribute values: education, balance, job, marital, and loan. Write the results to “Task_1d-out” in text file format. 

