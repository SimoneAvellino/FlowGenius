FROM fluent/fluentd:v1.12-1

USER root
RUN apk --no-cache add build-base ruby-dev
RUN gem install fluent-plugin-kafka --no-document
COPY ./fluent/fluent.conf /fluentd/etc/

USER fluent