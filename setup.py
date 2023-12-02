from setuptools import setup, find_packages


"""
To make BigData a package, so that in Jupyter Notebooks, modules in this package
can be directly accessed relatively from src
"""


setup(
    name="BigData",
    version="0.0.1",
    packages=find_packages(),
)
