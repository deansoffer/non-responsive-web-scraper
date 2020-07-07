from setuptools import setup, find_packages

requirements = []
with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='search_engines',
    version='1.0',
    description='Search Engines Scraper',
    author='DS',
    license='MIT',
    packages=find_packages(),
    install_requires=requirements
)
