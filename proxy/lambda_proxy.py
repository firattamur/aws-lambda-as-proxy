import json

import boto3


class LambdaProxy:
    def __init__(self, function_arns: list) -> None:
        """LambdaProxy constructor.

        :return: None
        """
        self.function_arns = function_arns
        self.function_arn_index = 0

    def _get_next_function_arn(self) -> str:
        """Get next function arn from list of function arns.

        :return: str
        """
        if self.function_arn_index == len(self.function_arns):
            self.function_arn_index = 0

        function_arn = self.function_arns[self.function_arn_index]
        self.function_arn_index += 1

        return function_arn

    def _invoke(self, function_arn: str, payload: dict) -> dict:
        """Invoke lambda function.

        :param function_arn : str
        :param payload      : dict

        :return             : dict
        """
        self.client = boto3.client("lambda", region_name=function_arn["region"])

        response = self.client.invoke(
            FunctionName=function_arn["arn"],
            InvocationType="RequestResponse",
            Payload=json.dumps(payload),
        )

        return json.loads(response["Payload"].read().decode("utf-8"))

    def request(self, payload: dict) -> dict:
        """Request lambda function.

        :param payload: dict

        :return       : dict
        """
        function_arn = self._get_next_function_arn()
        return self._invoke(function_arn, payload)
