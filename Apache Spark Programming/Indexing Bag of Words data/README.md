In this project, I will create a partitioned index of words to documents that contain the words. Using this index you can search for all the documents that contain a particular word efficiently. Data source: http://archive.ics.uci.edu/ml/datasets/Bag+of+Words. 

The data consists of two files:

1. The first file is called docword.txt, which contains the contents of all the documents. It has the following attributes:
   * docId: The ID of the document that contains the word
   * vocabId: Instead of storing the word itself, we store an ID from the vocabulary file.
   * count: An integer representing the number of times this word occurred in this document.
    
2. The second file called vocab.txt contains each word in the vocabulary, which is indexed by vocabIndex from the docword.txt file:
   * docId
   * vocabId
   * count

I'll be using Spark SQL to perform the following tasks:

* Task 3a. [spark SQL] Calculate the total count of each word across all documents. List the words in ascending alphabetical order.
* Task 3b. [spark SQL] Create a dataframe containing rows with four fields: (word, docId, count, firstLetter). Save the results in parquet format partitioned by firstLetter to docwordIndexFilename.
* Task 3c. [spark SQL] Load the previously created dataframe stored in parquet format from subtask b). For each document ID in the docIds list, display the following: the document ID, the word with the most occurrences in that document (break ties arbitrarily), and the number of occurrences of that word in the document. Use an optimisation to prevent loading the parquet file into memory multiple times.
* Task 3d. [spark SQL] Load the previously created dataframe stored in parquet format from subtask b). For each word in the queryWords list, display the docId with the most occurrences of that word (break ties arbitrarily). Use an optimisation based on how the data is partitioned.
