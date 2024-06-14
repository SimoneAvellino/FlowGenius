#!/bin/bash

# Check if Kafka is running
while ! nc -z localhost 9092; do
  sleep 1
done

# Create Kafka topics
echo "Creating Kafka topics..."
/bin/kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic emur
/bin/kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic simone
echo "Kafka topics created."