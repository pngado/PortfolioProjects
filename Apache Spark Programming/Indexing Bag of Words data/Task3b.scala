import org.apache.spark.sql._
import org.apache.spark.sql.types._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions._

// Define case classes for input data
case class Docword(docId: Int, vocabId: Int, count: Int)
case class VocabWord(vocabId: Int, word: String)

object Main {
  def solution(spark: SparkSession) {
    import spark.implicits._
    // Read the input data
    val docwords = spark.read.
      schema(Encoders.product[Docword].schema).
      option("delimiter", " ").
      csv("Data/docword.txt").
      as[Docword]
    val vocab = spark.read.
      schema(Encoders.product[VocabWord].schema).
      option("delimiter", " ").
      csv("Data/vocab.txt").
      as[VocabWord]
    val docwordIndexFilename = "Data/docword_index.parquet"

    // Extract the first letter of each word

    val wordCount = docwords.join(vocab, "vocabId").select($"word", $"docId", $"count")

    // Create a function to extract the first letter of each word
    def getFirstLetter(word: String): String = {
      word.substring(0, 1)
    }

    // Register the function as a UDF with Spark 
    val getFirstLetterUdf = spark.udf.register[String, String]("getFirstLetter", getFirstLetter)
    
    // Use the UDF to create a new column in the DataFrame
    val firstLetterDF = wordCount.withColumn("firstLetter", getFirstLetterUdf($"word"))

    // Save the results in parquet format partitioned by firstLetter
firstLetterDF.write.mode("overwrite").partitionBy("firstLetter").parquet(docwordIndexFilename)

   // Show the first 10 rows
   firstLetterDF.show(10)

  }

  // Do not edit the main function
  def main(args: Array[String]) {
    // Set log level
    import org.apache.log4j.{Logger,Level}
    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)
    // Initialise Spark
    val spark = SparkSession.builder
      .appName("Task3b")
      .master("local[4]")
      .config("spark.sql.shuffle.partitions", 4)
      .getOrCreate()
    // Run solution code
    solution(spark)
    // Stop Spark
    spark.stop()
  }
}
