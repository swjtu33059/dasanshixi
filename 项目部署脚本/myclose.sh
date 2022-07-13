ps aux | grep weblogs.jar | grep -v grep | awk '{print $2}' | xargs kill -9
ssh root@slave1 "ps aux | grep weblogs.jar | grep -v grep | awk '{print \$2}' | xargs kill -9"
ssh root@slave2 "ps aux | grep weblogs.jar | grep -v grep | awk '{print \$2}' | xargs kill -9"
ps aux | grep Application | grep -v grep | awk '{print $2}' | xargs kill -9
ssh root@slave1 "ps aux | grep Application | grep -v grep | awk '{print \$2}' | xargs kill -9"
ssh root@slave2 "ps aux | grep Application | grep -v grep | awk '{print \$2}' | xargs kill -9"
/opt/module/kafka_2.11-0.10.0.0/bin/kafka-server-stop.sh
ssh root@slave1 "/opt/module/kafka_2.11-0.10.0.0/bin/kafka-server-stop.sh"
ssh root@slave2 "/opt/module/kafka_2.11-0.10.0.0/bin/kafka-server-stop.sh"
ssh root@slave1 "/opt/module/hbase-1.2.4/bin/stop-hbase.sh"
/opt/module/hadoop-2.7.3/sbin/hadoop-daemon.sh stop journalnode
ssh root@slave1 "/opt/module/hadoop-2.7.3/sbin/hadoop-daemon.sh stop journalnode"
ssh root@slave2 "/opt/module/hadoop-2.7.3/sbin/hadoop-daemon.sh stop journalnode"
/opt/module/hadoop-2.7.3/sbin/mr-jobhistory-daemon.sh stop historyserver
ssh root@slave1 "/opt/module/hadoop-2.7.3/sbin/mr-jobhistory-daemon.sh stop historyserver"
ssh root@slave2 "/opt/module/hadoop-2.7.3/sbin/mr-jobhistory-daemon.sh stop historyserver"
/opt/module/hadoop-2.7.3/sbin/hadoop-daemon.sh stop datanode
ssh root@slave1 "/opt/module/hadoop-2.7.3/sbin/stop-dfs.sh"
ssh root@slave1 "/opt/module/hadoop-2.7.3/sbin/stop-yarn.sh"
/opt/module/zookeeper-3.4.10/bin/zkServer.sh stop
ssh root@slave1 "/opt/module/zookeeper-3.4.10/bin/zkServer.sh stop"
ssh root@slave2 "/opt/module/zookeeper-3.4.10/bin/zkServer.sh stop"
