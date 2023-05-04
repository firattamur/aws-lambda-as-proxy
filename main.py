import argparse
import json
import os
import threading

from proxy import LambdaProxy


def _parse_args():
    """A simple argument parser."""

    parser = argparse.ArgumentParser(description="Lambda Proxy")
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        help="Number of iterations to run the Lambda function",
    )
    parser.add_argument(
        "--t",
        type=int,
        default=1,
        help="Number of threads to run the Lambda function",
    )

    return parser.parse_args()


def _read_function_arns(path: str = "./terraform/output/lambda_functions.json") -> list:
    """A simple function to read the Lambda function ARNs from a output json file."""

    if os.path.exists(path) is False:
        raise FileNotFoundError(
            f"Function ARNs file not found at {path}, make sure to run Terraform first and then try again."
        )

    functions_arns = []

    with open(path, "r") as f:
        outputs = json.load(f)

        for output in outputs:
            functions_arns.append({"region": output, "arn": outputs[output]["value"]})

    return functions_arns


def _worker(proxy: LambdaProxy, payload: dict, unique_ips: set, iterations: int):
    """A simple worker function to be used with the LambdaProxy class."""

    for _ in range(iterations):
        try:
            response = proxy.request(payload)
            unique_ips.add(response.get("body", ""))

            print(f"Iteration {_ + 1}: {response.get('body', '')}")

        except Exception as e:
            continue


def main():
    """A simple test function to verify that the LambdaProxy class works as expected
    and return number of unique IP addresses from the Lambda functions."""

    args = _parse_args()
    thread_count = args.t
    iteration_count = args.n

    print("Starting Lambda Proxy test with the following parameters:")
    print(f"Number of threads   : {thread_count}")
    print(f"Number of iterations: {iteration_count}")

    lambda_function_arns = _read_function_arns()
    proxy = LambdaProxy(lambda_function_arns)
    unique_ips = set()

    payload = {
        "httpMethod": "GET",
        "headers": {
            "Content-Type": "application/json",
        },
        "body": "{}",
        "url": "https://api.ipify.org?format=json",
    }

    threads = []

    for _ in range(thread_count):
        thread = threading.Thread(
            target=_worker, args=(proxy, payload, unique_ips, iteration_count)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Number of unique IP addresses: {len(unique_ips)}")


if __name__ == "__main__":
    main()
