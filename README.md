# Python Proxy Service using AWS Lambdas

A simple Python application that demonstrates how to use AWS Lambdas as a proxy service to forward HTTP requests to remote servers. This application is intended to be used as a simple proxy service for various web applications such as web crawlers, web scrapers, etc.

## Requirements

- Python 3.10
- AWS Credentials (Access Key ID and Secret Access Key) in `~/.aws/credentials` file
- Terraform 1.4.6

## Setup

1. Create a new Python virtual environment and install the required dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. To create lambda functions, run the following command:

   ```bash
   ./infra_setup.sh
   ```

This will create 3 lambda functions in different AWS regions (us-east-1, us-east-2, us-west-1). The lambda functions are defined in Terraform configuration files in `/terraform` directory. The lambda functions are implemented with code in `/lambda/main.py`. The lambda functions simply forward the HTTP request to the specified URL and return the response.

3. To test the lambda functions, run the following command:

   ```bash
   python main.py --n number_iterations --t number_threads
   ```

This will send a GET request to the lambda function to learn ip address of the server. The lambda function will then forward the request to the specified URL and return the response. The `--n` and `--t` arguments are optional. The default values are `n=1` and `t=1`. Increasing the number of iterations and threads will increase the load on the lambda functions and increase the chance of getting different IP addresses.

4. To destroy the lambda functions, run the following command:

   ```bash
   ./infra_destroy.sh
   ```

## License

This project is licensed under the MIT License.
