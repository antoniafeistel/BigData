# Online Fraud Detection on Credit Card Transactions
This repository contains our project for the course "Big Data and Advanced Database System Concepts" at [Hochschule Karlsruhe](https://www.h-ka.de/) in the winter term 23/24.

We use a [Synthetic Credit Card Transaction Generator](https://github.com/namebrandon/Sparkov_Data_Generation/tree/b5eb45c89d36f2aa4ef16044a42945bed8b96d93) to generate synthetic credit card transactions that contain a label indicating fraud.
Based on these data we build two pipelines.
One for an offline training of a Random Forest Classifier, the other for an online fraud detection based on the previously trained Random Forest Classifier.

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

## Functionality

## Pre-trained Random Forest Classifier
We offer a [pre-trained Random Forest Classifier](https://github.com/antoniafeistel/BigData/tree/main/resources/models/pretrained/02_01_2024_18_33_00) to be used in the streaming-pipeline for online fraud detection.

To use it, set DATA_VERSION = "02_01_2024_18_33_00" in the [.env-file](https://github.com/antoniafeistel/BigData/blob/main/scripts/.env).

Training details:
- Random Forest Classifier based on 128 decision trees
- Spark configuration for training: 2 Workers with each 5 CPUs and 8 GB memory
- 43,253,806 synthetic credit card transactions from 10,000 different customers used for training
- 14.07 GB raw .csv-data with a training time (including data transformation) of 18 minutes or 1.12 GB transformed .parquet-data with a training time of 15 minutes
