import os
import subprocess
from dotenv import load_dotenv


def start_kafka():
    load_dotenv()
    subprocess.run(f"docker-compose -f {os.getenv("KAFKA_DOCKER_COMPOSE")} up -d", shell=True, check=True)
    subprocess.run(
        f'docker exec kafka1 kafka-topics --create --topic {os.getenv("KAFKA_TOPIC")} --partitions {os.getenv("NUM_PARTITIONS")} --replication-factor {os.getenv("REPLICATION_FACTOR")} --bootstrap-server {os.getenv("KAFKA_BOOTSTRAP_SERVERS")}',
        shell=True, check=True)


if __name__ == "__main__":
    start_kafka()
