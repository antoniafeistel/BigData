import subprocess
import argparse
import sys


def generate_transactions(n, o, s, e):
    python_exec = sys.executable
    subprocess.run([python_exec, "datagen.py", "-n", n, "-o", o, s, e], check=True, cwd="../Sparkov_Data_Generation")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate transactions with specified parameters.')
    parser.add_argument('-n', type=str, help='Number of customers to generate', default='10')
    parser.add_argument('-o', type=str, help='Output folder path', default="../resources/data/test")
    parser.add_argument('-s', type=str, help='Transactions start date in the format "%m-%d-%Y"', default='01-01-2015')
    parser.add_argument('-e', type=str, help='Transactions end date in the format "%m-%d-%Y"', default='01-01-2020')
    args = parser.parse_args()

    generate_transactions(args.n, args.o, args.s, args.e)
