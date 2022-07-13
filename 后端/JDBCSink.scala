package com.spark.test

import java.sql
import java.sql._

import org.apache.spark.sql.types.StructType
import org.apache.spark.sql.{ForeachWriter, Row}

/**
  * 处理从StructuredStreaming中向mysql中写入数据
  */
class JDBCSink(url: String, username: String, password: String) extends ForeachWriter[Row] {

  var statement: Statement = _
  var resultSet: ResultSet = _
  var connection: Connection = _

  override def open(partitionId: Long, version: Long): Boolean = {
    connection = DriverManager.getConnection(url, username, password)
    statement = connection.createStatement()
    return true
  }

  override def process(value: Row): Unit = {
    val c1 = value.getAs[String](0).replaceAll("[\\[\\]]", "")
    val c2 = value.getAs[Long](1)
    val table = value.getAs[String](2)
    val fieldNames: scala.Array[String] = value.schema.fieldNames
    val f1 = fieldNames(0)
    val f2 = fieldNames(1)
    val querySql = s"select 1 from $table where $f1 = '$c1'"

    val updateSql = s"update $table set $f2 = $c2 where $f1 = '$c1'"

    val insertSql = s"insert into $table($f1,$f2) values('$c1',$c2)"

    try {

      //查看连接是否成功
      var resultSet = statement.executeQuery(querySql)
      if (resultSet.next()) {
        statement.executeUpdate(updateSql)
      } else {
        statement.execute(insertSql)
      }
    } catch {
      case ex: SQLException => {
        println(ex)
      }
      case ex: Exception => {
        println("Exception")
      }
      case ex: RuntimeException => {
        println("RuntimeException")
      }
      case ex: Throwable => {
        println("Throwable")
      }
    }
  }

  override def close(errorOrNull: Throwable): Unit = {
    //    if(resultSet.wasNull()){
    //      resultSet.close()
    //    }
    if (statement != null) {
      statement.close()
    }
    if (connection != null) {
      connection.close()
    }
  }

}