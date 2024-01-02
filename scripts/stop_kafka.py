import subprocess
import os
from dotenv import load_dotenv


def stop_kafka():
    load_dotenv()
    subprocess.run(f"docker-compose -f {os.getenv("KAFKA_DOCKER_COMPOSE")} stop", shell=True, check=True)
    subprocess.run(f"docker-compose -f {os.getenv("KAFKA_DOCKER_COMPOSE")} down", shell=True, check=True)


if __name__ == "__main__":
    stop_kafka()
