import org.apache.spark.sql._
import org.apache.spark.sql.types._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions._

object Main {
  def solution(spark: SparkSession, queryWords: Seq[String]) {
    import spark.implicits._

    println("Query words:")
    for(queryWord <- queryWords) {
      println(queryWord)
    }
    val docwordIndexFilename = "Data/docword_index.parquet"    

    // Load the previously created DataFrame stored in Parquet format 
    val docwordDF = spark.read.parquet(docwordIndexFilename)

    // Create a function to extract the first letter of each word
    def getFirstLetter(words: Seq[String]): Seq[String] = {
      words.map(word => word.substring(0, 1))
    }

    // Get the first letters of the query words to filter partitions
    val firstLetters = getFirstLetter(queryWords).distinct

    // Optimisation based on how the data is partitioned
    val filteredPartitionDF = docwordDF.filter($"firstLetter".isin(firstLetters:_*))

    // Find the docId with maximum occurences of each word and print the result
    for (queryWord <- queryWords) {
      val maxCountDF = filteredPartitionDF.filter($"word" === queryWord).groupBy($"word").agg(max($"count").alias("count"))
      val resultDF = maxCountDF.join(filteredPartitionDF, Seq("word", "count"), "inner").select("word", "docId").first()
      println(resultDF)
    }

  }

  // Do not edit the main function
  def main(args: Array[String]) {
    // Set log level
    import org.apache.log4j.{Logger,Level}
    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)
    // Initialise Spark
    val spark = SparkSession.builder
      .appName("Task3d")
      .master("local[4]")
      .config("spark.sql.shuffle.partitions", 4)
      .getOrCreate()
    // Run solution code
    solution(spark, args)
    // Stop Spark
    spark.stop()
  }
}
