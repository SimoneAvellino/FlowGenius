FROM python:3.7

# Install the required Python packages
RUN pip install kafka-python

# Copy the Python script into the container
COPY ./kafka_consumer/consumer.py /kafka_consumer/consumer.py

# Execute the Python script during container startup
CMD ["python", "/kafka_consumer/consumer.py"]