from kafka import KafkaConsumer

# Create a Kafka consumer instance
consumer = KafkaConsumer(
    "emur",
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',  # Start consuming from the earliest message
    group_id=None,  # Use a unique group_id to avoid consumer group coordination
    enable_auto_commit=False,  # Disable auto commit to have full control over offsets
    value_deserializer=lambda x: x.decode('utf-8')  # Decode message value from bytes to string
)

# Start consuming messages
for message in consumer:
    print(f"Received message: {message.value}")