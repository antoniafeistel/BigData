import os
import subprocess
from dotenv import load_dotenv


def start_kafka():
    load_dotenv()
    os.system("docker-compose -f zk-single-kafka-single.yml up -d")
    subprocess.run(
        f'docker exec kafka1 kafka-topics --create --topic {os.getenv("KAFKA_TOPIC")} --bootstrap-server {os.getenv("KAFKA_BOOTSTRAP_SERVER")}',
        shell=True,
        check=True
    )
    print("Connected to Kafka message broker (see sent messages below):")
    subprocess.run(
        f'docker exec kafka1 kafka-console-consumer --topic {os.getenv("KAFKA_TOPIC")} --from-beginning --bootstrap-server {os.getenv("KAFKA_BOOTSTRAP_SERVER")}',
        shell=True,
        check=True
    )


if __name__ == "__main__":
    start_kafka()
