import os


def stop_kafka():
    os.system("docker-compose -f zk-single-kafka-single.yml stop")
    os.system("docker-compose -f zk-single-kafka-single.yml down")


if __name__ == "__main__":
    stop_kafka()
