import org.apache.spark._
import org.apache.spark.SparkContext._
import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import scala.xml.{XML,NodeSeq}

object PageRank1 {
    def main(args: Array[String]) {
	val startTime=System.currentTimeMillis
      val inputFile = "hdfs://ec2-52-90-60-96.compute-1.amazonaws.com:9000/user/zhoulin/input/"
      val outputFile = "hdfs://ec2-52-90-60-96.compute-1.amazonaws.com:9000/user/zhoulin/pagerank-EX1"
      val iters = if (args.length > 1) args(1).toInt else 15
      val conf = new SparkConf()
      conf.setAppName("pureSparkpageRank")
      conf.setMaster("spark://ec2-52-90-60-96.compute-1.amazonaws.com:7077")
      // conf.setMaster("spark://ec2-54-165-164-35.compute-1.amazonaws.com:7077")
      conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
      // Create a Scala Spark Context.
      val sc = new SparkContext(conf)
      // Load input data.
      val input = sc.textFile(inputFile)
      
      //*** Parse the Wikipedia page data into a graph***
      
      // Split up into columns.
      var page = input.map(line => {
        val parts = line.split("\t")
        val (title, neighbour_titles) = (parts(0), parts(3).replace("\\n", "\n"))
        // Convert string to xml
        val links =
          if (neighbour_titles == "\\N") {
            NodeSeq.Empty
          } else {
            try {
              XML.loadString(neighbour_titles) \\ "link" \ "target"
            } catch {
              case e: org.xml.sax.SAXParseException =>
                System.err.println("Article \"" + title + "\" has malformed XML in neighbour_titles:\n" + neighbour_titles)
              NodeSeq.Empty
            }
          } 
        val outEdges = links.map(link => new String(link.text)).toArray
        val id = new String(title)    
        (id, outEdges)
      }).cache
      var ranks = page.mapValues(v => 1.0)
      for (i <- 1 to iters) {
        val contributes = page.join(ranks).values.flatMap{ case (urls, rank) =>
          val size = urls.size
          urls.map(url => (url, rank / size))
          }  
        ranks = contributes.reduceByKey(_+_).mapValues (0.15 + 0.85 * _)
      }
      val output = ranks.takeOrdered(100)(Ordering[Double].reverse.on(x => x._2))
      sc.parallelize(output).saveAsTextFile(outputFile)
	val time=(System.currentTimeMillis-startTime)/1000.0	
     ranks.collect().foreach(tup => println(tup._1 + " has rank: " + tup._2 + "."))
      sc.stop()
	println("completed 15 iterations in %f seconds: %f seconds per iteration".format(time, time/15))
    }  
}
