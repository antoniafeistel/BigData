import sys
import subprocess


def stop_kafka():
    subprocess.run("docker-compose -f zk-single-kafka-single.yml stop", shell=True, check=True)
    subprocess.run("docker-compose -f zk-single-kafka-single.yml down", shell=True, check=True)


if __name__ == "__main__":
    try:
        stop_kafka()
    except KeyboardInterrupt:
        sys.exit(0)
