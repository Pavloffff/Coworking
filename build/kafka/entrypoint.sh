#!/bin/bash
set -e

sed -i "s|zookeeper.connect=localhost:2181|zookeeper.connect=${ZOOKEEPER_SERVERS}|g" ./config/server.properties && \
echo -e "\ndelete.topic.enable=true" >> ./config/server.properties && \
echo "message.max.bytes=${MSG_MAX_BYTES}" >> ./config/server.properties && \
echo "replica.fetch.max.bytes=${REPLICA_FETCH_MAX_BYTES}" >> ./config/server.properties &&\

echo "inter.broker.listener.name = INTERNAL" >> ./config/server.properties
echo "listener.security.protocol.map=EXTERNAL:PLAINTEXT,INTERNAL:PLAINTEXT" >> ./config/server.properties
echo "log.message.timestamp.type=LogAppendTime" >> ./config/server.properties
echo "auto.create.topics.enable=false" >> ./config/server.properties

if [ -n "${KAFKA_EXTERNAL_PORT}" ]; then
sed -i "s|#listeners=PLAINTEXT://:9092|listeners=INTERNAL://0.0.0.0:${KAFKA_INTERNAL_PORT},EXTERNAL://0.0.0.0:${KAFKA_EXTERNAL_PORT} |g" ./config/server.properties && \
sed -i "s|#advertised.listeners=PLAINTEXT://your.host.name:9092|advertised.listeners=INTERNAL://${KAFKA_INTERNAL_ADDRESS}:${KAFKA_INTERNAL_PORT}, EXTERNAL://${KAFKA_EXTERNAL_ADDRESS}:${KAFKA_EXTERNAL_PORT}|g" ./config/server.properties
else
sed -i "s|#listeners=PLAINTEXT://:9092|listeners=INTERNAL://0.0.0.0:${KAFKA_INTERNAL_PORT}|g" ./config/server.properties && \
sed -i "s|#advertised.listeners=PLAINTEXT://your.host.name:9092|advertised.listeners=INTERNAL://${KAFKA_INTERNAL_ADDRESS}:${KAFKA_INTERNAL_PORT}|g" ./config/server.properties
fi

export KAFKA_OPTS;
exec wait-for-it.sh --hosts=${ZOOKEEPER_SERVERS} -t ${ZOOKEEPER_WAIT_TIME} -s -- bin/kafka-server-start.sh config/server.properties
