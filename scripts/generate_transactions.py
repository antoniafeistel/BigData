import subprocess
import argparse
import sys
import os
import shutil
import csv
from datetime import datetime


def is_csv_header_only(file_path):
    with open(file_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        # jump over header
        next(csv_reader)
        return all(row == [] for row in csv_reader)


def get_non_empty_transactions(source_folder, destination_folder, num_batch=None):
    if num_batch is not None:
        destination_folder = os.path.join(destination_folder, f"batch_{num_batch}")
    os.makedirs(destination_folder)

    for file_name in os.listdir(source_folder):
        source_path = os.path.join(source_folder, file_name)

        if 'adults' in file_name.lower() and not is_csv_header_only(source_path):
            destination_path = os.path.join(destination_folder, file_name)
            shutil.move(source_path, destination_path)
        else:
            os.remove(source_path)


def generate_transactions(n, o, s, e):
    python_exec = sys.executable
    subprocess.run([python_exec, "datagen.py", "-n", n, "-o", o, s, e], check=True, cwd="../Sparkov_Data_Generation")


def generate_transaction_test_data_stream(n, temp_folder, s, e, timestamp):
    test_folder = "../resources/data/test"
    batch = 0
    try:
        while True:
            generate_transactions(n, temp_folder, s, e)
            test_folder_dir = os.path.join(test_folder, timestamp)
            get_non_empty_transactions(temp_folder, test_folder_dir, batch)
            batch += 1
    except KeyboardInterrupt:
        shutil.rmtree(temp_folder)
        sys.exit(0)


def generate_raw_transaction_train_data(n, temp_folder, s, e, timestamp):
    raw_train_folder = "../resources/data/train/raw"
    generate_transactions(n, temp_folder, s, e)
    raw_train_folder_dir = os.path.join(raw_train_folder, timestamp)
    get_non_empty_transactions(temp_folder, raw_train_folder_dir)
    shutil.rmtree(temp_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate transactions with specified parameters.')
    parser.add_argument('-n', type=str, help='Number of customers to generate', default='10')
    parser.add_argument('-s', type=str, help='Transactions start date in the format "%m-%d-%Y"', default='01-01-2015')
    parser.add_argument('-e', type=str, help='Transactions end date in the format "%m-%d-%Y"', default='01-01-2020')
    parser.add_argument('-m', type=str, help='Mode of data generation: "stream" (test data stream) or "train" (raw training data)', default='stream')
    args = parser.parse_args()

    temp_folder = "../resources/data/temp"
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    if args.m == "stream":
        generate_transaction_test_data_stream(args.n, temp_folder, args.s, args.e, timestamp)
    elif args.m == "train":
        generate_raw_transaction_train_data(args.n, temp_folder, args.s, args.e, timestamp)
