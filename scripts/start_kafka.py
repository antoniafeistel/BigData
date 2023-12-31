import os
import subprocess
from dotenv import load_dotenv


def start_kafka():
    load_dotenv()
    subprocess.run("docker-compose -f zk-multiple-kafka-multiple.yml up -d", shell=True, check=True)
    subprocess.run(
        f'docker exec kafka1 kafka-topics --create --topic {os.getenv("KAFKA_TOPIC")} --partitions 2 --replication-factor 2 --bootstrap-server {os.getenv("KAFKA_BOOTSTRAP_SERVERS")}',
        shell=True,
        check=True
    )


if __name__ == "__main__":
    start_kafka()
