terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}

provider "aws" {
  alias  = "us_west_2"
  region = "us-west-2"
}

provider "aws" {
  alias  = "eu_central_1"
  region = "eu-central-1"
}

resource "aws_lambda_function" "lambda_proxy_us_east_1" {
  provider = aws.us_east_1

  function_name = "lambda_proxy_us_east_1"
  handler       = "main.handler"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.9"

  filename = "lambda/lambda.zip"
}

resource "aws_lambda_function" "lambda_proxy_us_west_2" {
  provider = aws.us_west_2

  function_name = "lambda_proxy_us_west_2"
  handler       = "main.handler"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.9"

  filename = "lambda/lambda.zip"
}

resource "aws_lambda_function" "lambda_proxy_eu_central_1" {
  provider = aws.eu_central_1

  function_name = "lambda_proxy_eu_central_1"
  handler       = "main.handler"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.9"

  filename = "lambda/lambda.zip"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}


output "us-east-1" {
  value = aws_lambda_function.lambda_proxy_us_east_1.arn
}

output "us-west-2" {
  value = aws_lambda_function.lambda_proxy_us_west_2.arn
}

output "eu-central-1" {
  value = aws_lambda_function.lambda_proxy_eu_central_1.arn
}
