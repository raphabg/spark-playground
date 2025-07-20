#!/bin/bash
set -e

case "$SPARK_ROLE" in
  master)
    echo "Starting Spark Master..."
    ${SPARK_HOME}/sbin/start-master.sh -h ${SPARK_MASTER_HOST} -p ${SPARK_MASTER_PORT} 
    echo "Spark Master started. Streaming logs to stdout..." 
    tail -f ${SPARK_HOME}/logs/*master*.out
    ;;

  worker)
    #!/bin/sh
    echo "Starting Spark Worker..."
    ${SPARK_HOME}/sbin/start-worker.sh spark://${SPARK_MASTER_HOST}:${SPARK_MASTER_PORT} \
      --cores ${SPARK_WORKER_CORES} --memory ${SPARK_WORKER_MEMORY} 
    echo "Spark Worker started. Streaming logs to stdout..."
    tail -f ${SPARK_HOME}/logs/*worker*.out
    ;;

  history)
    echo "Starting Spark History Server..."
    ${SPARK_HOME}/sbin/start-history-server.sh ${SPARK_HISTORY_OPTS} 
    echo "Spark History Server started. Streaming logs to stdout..."
    tail -f ${SPARK_HOME}/logs/*history*.out
    ;;

  *)
    echo "Unknown SPARK_ROLE: $SPARK_ROLE. Running default command: $@"
    exec "$@"
    ;;
esac
