package com.spark.test

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.{LongType, StringType}

/**
  * 结构化流从kafka中读取数据存储到关系型数据库mysql
  * 目前结构化流对kafka的要求版本0.10及以上
  */
object StructuredStreamingKafka {

  case class Weblog(datatime: String,
                    userid: String,
                    searchname: String,
                    retorder: String,
                    cliorder: String,
                    cliurl: String)

  def main(args: Array[String]): Unit = {
    System.setProperty("hadoop.home.dir", "E:\\BaiduYunDownload\\新闻推荐系统\\hadoop-2.7.4");
    val spark = SparkSession.builder()
      .master("local[*]")
      .appName("streaming").getOrCreate()

    val df = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "192.168.20.101:9092") //从哪台服务器接收
      .option("subscribe", "weblogs")
      .load()
    import spark.implicits._
    val lines = df.selectExpr("CAST(value AS STRING)").as[String]

    val weblog = lines.map(_.split(","))
      .map(x => Weblog(x(0), x(1), x(2), x(3), x(4), x(5)))

    val titleCount = weblog
      .groupBy("searchname").count().toDF("titleName", "count")
      .withColumn("table", lit("webCount"))
    val timeInterval = weblog
      .groupBy("datatime").count().toDF("timeInterval", "count")
      .withColumn("table", lit("timeCount"))

    val rankRate = weblog
      .select("cliorder")
      //.withColumn("retorder", $"retorder".cast(StringType))
      .withColumn("retorder", monotonically_increasing_id().cast(LongType))
      .withColumn("cliorder", $"cliorder".cast(StringType))
      .withColumn("table", lit("rankRate"))

    val url = "jdbc:mysql://192.168.20.103:3306/test"
    val username = "root"
    val password = "123456"
    val writer = new JDBCSink(url, username, password)
    val query1 = titleCount.writeStream
      .foreach(writer)
      .outputMode("update")
      .trigger(Trigger.ProcessingTime("1 second"))
      .start()
    val query2 = timeInterval.writeStream
      .foreach(writer)
      .outputMode("update")
      .trigger(Trigger.ProcessingTime("1 second"))
      .start()
    val query3 = rankRate.writeStream
      .foreach(writer)
      .outputMode("update")
      .trigger(Trigger.ProcessingTime("1 second"))
      .start()

    spark.streams.awaitAnyTermination()

  }
}