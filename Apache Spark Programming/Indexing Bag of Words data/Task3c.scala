import org.apache.spark.sql._
import org.apache.spark.sql.types._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions._

object Main {
  def solution(spark: SparkSession, docIds: Seq[String]) {
    import spark.implicits._

    println("Query words:")    
    for(docId <- docIds) {
      println(docId)      
    }
    val docwordIndexFilename = "Data/docword_index.parquet"

    // Load the previously created DataFrame stored in parquet format 
    val docwordDF = spark.read.parquet(docwordIndexFilename)

    // Cache docwordDF to prevent loading the parquet file into memory multiple times
    docwordDF.cache()

    // Find the word with maximum occurences in each of the specified documents
    for (docId <- docIds) {
      val maxCountDF = docwordDF.filter($"docId" === docId).groupBy($"docId").agg(max($"count").alias("count"))
      val resultDF = maxCountDF.join(docwordDF, Seq("docId", "count"), "inner").select("docId", "word", "count").first()
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
      .appName("Task3c")
      .master("local[4]")
      .config("spark.sql.shuffle.partitions", 4)
      .getOrCreate()
    // Run solution code
    solution(spark, args)
    // Stop Spark
    spark.stop()
  }
}
