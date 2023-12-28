import subprocess
import argparse
import sys
import os
import shutil
import csv


def is_csv_header_only(file_path):
    with open(file_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        # jump over header
        next(csv_reader)
        return all(row == [] for row in csv_reader)


def get_non_empty_transactions(source_folder, destination_folder):
    for file_name in os.listdir(source_folder):
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)

        if 'adults' in file_name.lower() and not is_csv_header_only(source_path):
            shutil.move(source_path, destination_path)
        else:
            os.remove(source_path)


def generate_transactions(n, o, s, e):
    python_exec = sys.executable
    subprocess.run([python_exec, "datagen.py", "-n", n, "-o", o, s, e], check=True, cwd="../Sparkov_Data_Generation")


if __name__ == "__main__":
    test_temp_folder = "../resources/data/test_temp"

    parser = argparse.ArgumentParser(description='Generate transactions with specified parameters.')
    parser.add_argument('-n', type=str, help='Number of customers to generate', default='10')
    parser.add_argument('-o', type=str, help='Output folder path', default=test_temp_folder)
    parser.add_argument('-s', type=str, help='Transactions start date in the format "%m-%d-%Y"', default='01-01-2015')
    parser.add_argument('-e', type=str, help='Transactions end date in the format "%m-%d-%Y"', default='01-01-2020')
    args = parser.parse_args()

    while True:
        generate_transactions(args.n, args.o, args.s, args.e)
        get_non_empty_transactions(test_temp_folder, "../resources/data/test")