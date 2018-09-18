from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='DhelmGfeedClient',
    version='1.0.0',
    packages=find_packages(),
    url='',
    license='Apache License 2.0',
    author='Pallav Nandi Chaudhuri',
    author_email='developer@kncsolutions.in',
    description='',
    install_requires=[
        "autobahn[twisted]>=18.9.2"
    ],
)
