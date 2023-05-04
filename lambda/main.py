import http.client
import json
from typing import Dict
from urllib.parse import urlparse


def handler(event: Dict, context: Dict) -> Dict:
    """Lambda function handler

    Args:
        event (dict)    : Event data
        context (dict)  : Runtime information

    Returns:
        dict: Response data
    """

    method = event.get("httpMethod", "GET")
    headers = event.get("headers", {})
    body = event.get("body", "")

    url = event.get("url", "")
    parsed_url = urlparse(url)

    conn = http.client.HTTPSConnection(parsed_url.netloc)

    try:
        conn.request(method, parsed_url.path, body, headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        response_headers = dict(response.getheaders())

    except Exception as e:
        response = http.client.HTTPResponse(conn.sock)
        response.status = 500
        data = json.dumps({"error": str(e)})
        response_headers = {"Content-Type": "application/json"}

    finally:
        conn.close()

    return {
        "statusCode": response.status,
        "headers": response_headers,
        "body": data,
    }
