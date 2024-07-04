import org.apache.spark.sql._
import org.apache.spark.sql.types._
import org.apache.spark.SparkContext

object Main {
  def solution(sc: SparkContext) {
    // Load each line of the input data
    val bankdataLines = sc.textFile("Data/bank.csv")
    // Split each line of the input data into an array of strings
    val bankdata = bankdataLines.map(_.split(";"))

    // Group balance into 3 categories and report the number of people in each category

    def categorizeBalance(balance:Int) : String = {
      balance match {
        case balance if balance <= 500 => "Low"
        case balance if (balance > 500) && (balance <= 1500) => "Medium"
        case balance if balance > 1500 => "High"
        }
    }

    val balanceCategory = bankdata.map(row => categorizeBalance(row(5).toInt))
    val categoryCount = balanceCategory.map(category => (category, 1)).reduceByKey(_ + _)

    // Write the results to "Task_1c-out" in text file format  
    categoryCount.saveAsTextFile("Task_1c-out")
  }

  // Do not edit the main function
  def main(args: Array[String]) {
    // Set log level
    import org.apache.log4j.{Logger,Level}
    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)
    // Initialise Spark
    val spark = SparkSession.builder
      .appName("Task1c")
      .master("local[4]")
      .config("spark.hadoop.validateOutputSpecs", "false")
      .config("spark.default.parallelism", 1)
      .getOrCreate()
    // Run solution code
    solution(spark.sparkContext)
    // Stop Spark
    spark.stop()
  }
}
