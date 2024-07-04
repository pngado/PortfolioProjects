import org.apache.spark.sql._
import org.apache.spark.sql.types._
import org.apache.spark.SparkContext

object Main {
  def solution(sc: SparkContext, x: String, y: String) {
    // Load each line of the input data
    val twitterLines = sc.textFile("Data/twitter.tsv")
    // Split each line of the input data into an array of strings
    val twitterdata = twitterLines.map(_.split("\t"))

    println("Months: x = " + x + ", y = " + y)

    val tweetsX = twitterdata.filter(r => r(1) == x).map(r => (r(3), r(2).toInt))
    val tweetsY = twitterdata.filter(r => r(1) == y).map(r => (r(3), r(2).toInt))
    val joined = tweetsX.join(tweetsY)
    val result = joined.reduce((a, b) => if(a._2._2 - a._2._1 > b._2._2 - b._2._1) a else b)

    val (hashtagName, (countX, countY)) = result
    println(s"hashtagName: $hashtagName, countX: $countX, countY: $countY")
  }

  // Do not edit the main function
  def main(args: Array[String]) {
    // Set log level
    import org.apache.log4j.{Logger,Level}
    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)
    // Check command line arguments
    if(args.length != 2) {
      println("Expected two command line arguments: <month x> and <month y>")
    }
    // Initialise Spark
    val spark = SparkSession.builder
      .appName("Task2c")
      .master("local[4]")
      .config("spark.hadoop.validateOutputSpecs", "false")
      .config("spark.default.parallelism", 1)
      .getOrCreate()
    // Run solution code
    solution(spark.sparkContext, args(0), args(1))
    // Stop Spark
    spark.stop()
  }
}
