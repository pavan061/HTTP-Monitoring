import argparse  # module for parsing command-line arguments
import json  # module for working with JSON data
import logging  # module for logging messages
import sys  # module for interacting with the interpreter
import time  # module for working with time values
import yaml  # module for parsing YAML data
import requests  # module for making HTTP requests

# configure logging to include timestamps and severity levels
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def load_config_file(config_file):
    """
    Load a YAML configuration file from disk and return its contents as a Python object.

    :param config_file: path to the YAML file to load
    :return: a dictionary containing the configuration data
    """
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        logging.error(f"Could not find file '{config_file}'")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to load config file: {e}")
        sys.exit(1)

def test_endpoint(endpoint):
    """
    Make an HTTP request to a specified endpoint and return whether the request was successful and how long it took.

    :param endpoint: a dictionary containing the URL, HTTP method, headers, and body to send in the request
    :return: a tuple containing a boolean indicating whether the request was successful and an integer indicating how long it took in milliseconds
    """
    method = endpoint.get('method', 'GET')
    url = endpoint['url']
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', '')

    try:
        start_time = time.time()
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=body, timeout=10)
        else:
            logging.error(f"Invalid HTTP method: {method}")
            return False, 0

        end_time = time.time()
        response_time_ms = (end_time - start_time) * 1000
        if response.ok and response_time_ms < 500:
            return True, response_time_ms
        else:
            return False, response_time_ms
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return False, 0

def get_domain(url):
    """
    Extract the domain name from a URL.

    :param url: the URL to extract the domain name from
    :return: the domain name
    """
    return url.split('//')[-1].split('/')[0]

def get_availability_percentages(stats):
    """
    Calculate the percentage of successful requests for each domain in a dictionary of request statistics.

    :param stats: a dictionary containing request statistics, where each key is a domain name and each value is another dictionary containing the counts of successful and failed requests
    :return: a dictionary containing the availability percentage for each domain
    """
    availability_percentages = {}
    for domain, status_counts in stats.items():
        total_requests = sum(status_counts.values())
        up_requests = status_counts.get('up', 0)
        availability_percentages[domain] = round(up_requests / total_requests * 100)
    return availability_percentages

def log_availability_percentages(stats):
    """
    Calculates and logs the availability percentages for each domain in the given stats dictionary.
    The availability percentage for a domain is calculated as the percentage of requests to that domain that returned
    a successful response (HTTP status code in the 2xx range).

    Args:
        stats (dict): A dictionary containing statistics about the endpoints tested, organized by domain.

    Returns:
        None
    """
    availability_percentages = get_availability_percentages(stats)
    for domain, percentage in availability_percentages.items():
        logging.info(f"{domain} has {percentage}% availability percentage")

def main(config_file):
    """
    The main function of the script. Loads the configuration file, tests the endpoints at the specified intervals, and
    logs availability statistics.

    Args:
        config_file (str): The path to the YAML configuration file.

    Returns:
        None
    """
    config = load_config_file(config_file)
    stats = {}

    while True:
        for endpoint in config:
            if 'url' not in endpoint:
                continue
            name = endpoint.get('name', endpoint['url'])
            url = endpoint['url']
            domain = get_domain(url)

            is_up, response_time_ms = test_endpoint(endpoint)

            if domain not in stats:
                stats[domain] = {'up': 0, 'down': 0}

            if is_up:
                stats[domain]['up'] += 1
                logging.info(f"{name} is UP ({response_time_ms:.2f}ms)")
            else:
                stats[domain]['down'] += 1
                logging.warning(f"{name} is DOWN ({response_time_ms:.2f}ms)")

        log_availability_percentages(stats)
        time.sleep(15)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='path to YAML config file')
    args = parser.parse_args()

    main(args.config_file)
