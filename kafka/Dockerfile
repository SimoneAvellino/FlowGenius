FROM confluentinc/cp-kafka:latest

RUN /etc/confluent/docker/run
USER root
COPY ./kafka/init-kafka-topics.sh /init-kafka-topics.sh
RUN chmod +x /init-kafka-topics.sh

# Execute the script during container startup
CMD ["/init-kafka-topics.sh"]