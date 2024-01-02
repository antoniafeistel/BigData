# Big Data Project - Fraud Detection on Credit Card Transactions
This repository contains our big data project.

## Infrastructure Requirements
- only Mac is supported
- at least [Python 3.12.0](https://www.python.org/downloads/)
- [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/) for Mac
- easiest to navigate with [PyCharm](https://www.jetbrains.com/pycharm/)
- at least [Apache Spark 3.5.0](https://spark.apache.org/downloads.html) (package type: Pre-built for Apache Hadoop 3.3 and later)

## Environment Variables
```bash
SPARK_HOME=path/to/Spark
PATH=path/to/Spark/bin
PATH=path/to/python3/version/bin
PYSPARK_DRIVER_PYTHON=python3
```

## Installation

1. Clone the repo
```bash
git clone https://github.com/antoniafeistel/BigData.git
```
2. Create a virtual environment
```bash
python3 -m venv path/to/new/virtual/environment/my_venv
```

3. Activate your virtual environment
```bash
source my_venv/bin/activate
```

4. Install requirements
```bash
pip install -r BigData/requirements.txt
```

5. Install provided Python packages
```bash
pip install -e BigData/.
```

6. Clone used submodule
```bash
git submodule update --init
```

## Architecture
![Architecture](https://github.com/antoniafeistel/BigData/blob/main/resources_readme/architecture.png)

## Scalability Model for the Streaming-Pipeline
For the streaming-pipeline, all components (Producer, Kafka cluster, Consumer) can be independently scaled. Thus, our architecture enables a high degree of parallelization and fault tolerance.
Moreover, fault tolerance is further improved by the topic partitions and replications used in the Kafka cluster.
![Kafka Cluster](https://github.com/antoniafeistel/BigData/blob/main/resources_readme/kafka_cluster.png)

## Dependency Graph
![Dependency Graph](https://github.com/antoniafeistel/BigData/blob/main/resources_readme/dependency_graph.svg)

## Configurations
