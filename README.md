# HTTP-Monitoring

Availability Checker
This Python script checks the availability of a list of endpoints and logs the percentage of successful responses. It uses the requests library to send HTTP requests and the pyyaml library to read the endpoint configuration from a YAML file.

Installation
Install Python 3.6 or later on your machine if it is not already installed. You can download Python from the official website: https://www.python.org/downloads/

Install the required packages using pip by running the following command in your terminal or command prompt:
pip install requests pyyaml

Usage
Run the script with the following command: python main.py sinput.yaml

The script will run indefinitely, testing each endpoint every 15 seconds and logging the availability percentage for each domain. Press Ctrl + C to stop the script.
