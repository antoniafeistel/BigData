from pyspark.sql import SparkSession
from confluent_kafka import Producer
import fastavro
import json

import config


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def produce_avro_to_kafka(avro_file_path, kafka_topic, bootstrap_servers):
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
    }

    producer = Producer(producer_config)

    with open(avro_file_path, mode='rb') as avro_file:
        avro_reader = fastavro.reader(avro_file)
        for record in avro_reader:
            # Convert each CSV row to JSON
            message_value = json.dumps(record)
            print(f"message this is: {message_value}")

            # Produce message to Kafka
            producer.produce(kafka_topic, value=message_value, callback=delivery_report)

    producer.flush()


spark = SparkSession.builder.master(config.SPARK_MASTER).getOrCreate()

produce_avro_to_kafka(config.AVRO_FILE_PATH, config.KAFKA_TOPIC, config.KAFKA_BOOTSTRAP_SERVERS)
