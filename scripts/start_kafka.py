import os
import sys
import subprocess
from dotenv import load_dotenv


def start_kafka():
    load_dotenv()
    subprocess.run("docker-compose -f zk-single-kafka-single.yml up -d", shell=True, check=True)
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
    try:
        start_kafka()
    except KeyboardInterrupt:
        sys.exit(0)
