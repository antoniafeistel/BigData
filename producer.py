from pyspark.sql import SparkSession
from confluent_kafka import Producer, avro
from confluent_kafka.avro import AvroProducer
import csv
import json

import config


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def produce_csv_to_kafka(csv_file_path, kafka_topic, bootstrap_servers):
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
    }

    producer = Producer(producer_config)

    with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            row['field2'] = int(row['field2'])
            # Convert each CSV row to JSON
            message_value = json.dumps(row)

            # Produce message to Kafka
            producer.produce(kafka_topic, value=message_value, callback=delivery_report)

    producer.flush()


spark = SparkSession.builder.master(config.SPARK_MASTER).getOrCreate()

produce_csv_to_kafka(config.CSV_FILE_PATH, config.KAFKA_TOPIC, config.KAFKA_BOOTSTRAP_SERVERS)
