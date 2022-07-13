/opt/module/zookeeper-3.4.10/bin/zkServer.sh start
ssh root@slave1 "/opt/module/zookeeper-3.4.10/bin/zkServer.sh start"
ssh root@slave2 "/opt/module/zookeeper-3.4.10/bin/zkServer.sh start"
/opt/module/hadoop-2.7.3/sbin/hadoop-daemon.sh start datanode
ssh root@slave1 "/opt/module/hadoop-2.7.3/sbin/start-dfs.sh"
ssh root@slave1 "/opt/module/hadoop-2.7.3/sbin/start-yarn.sh"
/opt/module/hadoop-2.7.3/sbin/mr-jobhistory-daemon.sh start historyserver
ssh root@slave1 "/opt/module/hadoop-2.7.3/sbin/mr-jobhistory-daemon.sh start historyserver"
ssh root@slave2 "/opt/module/hadoop-2.7.3/sbin/mr-jobhistory-daemon.sh start historyserver"
/opt/module/hadoop-2.7.3/sbin/hadoop-daemon.sh start journalnode
ssh root@slave1 "/opt/module/hadoop-2.7.3/sbin/hadoop-daemon.sh start journalnode"
ssh root@slave2 "/opt/module/hadoop-2.7.3/sbin/hadoop-daemon.sh start journalnode"
ssh root@slave1 "/opt/module/hbase-1.2.4/bin/start-hbase.sh"
/opt/module/kafka_2.11-0.10.0.0/bin/kafka-server-start.sh -daemon /opt/module/kafka_2.11-0.10.0.0/config/server.properties
ssh root@slave1 "/opt/module/kafka_2.11-0.10.0.0/bin/kafka-server-start.sh -daemon /opt/module/kafka_2.11-0.10.0.0/config/server.properties"
ssh root@slave2 "/opt/module/kafka_2.11-0.10.0.0/bin/kafka-server-start.sh -daemon /opt/module/kafka_2.11-0.10.0.0/config/server.properties"
cd /opt/module/apache-flume-1.7.0-bin && bash flume-kfk-start.sh>kafka.log 2>&1 &
ssh root@slave1 "cd /opt/module/apache-flume-1.7.0-bin && bash flume-kfk-start.sh>kafka.log 2>&1 &" > /dev/null 2>&1 &
ssh root@slave2 "cd /opt/module/apache-flume-1.7.0-bin && bash flume-kfk-start.sh>kafka.log 2>&1 &" > /dev/null 2>&1 &
ssh root@slave1 "/opt/data/weblog-shell.sh" > /dev/null 2>&1 &
ssh root@slave2 "/opt/data/weblog-shell.sh" > /dev/null 2>&1 &
/opt/module/kafka_2.11-0.10.0.0/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic weblogs --from-beginning