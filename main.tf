terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.23"
    }
  }
}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.region
}

resource "aws_s3_bucket" "project_buckets" {
  count  = length("${var.bucket_names}")
  bucket = var.bucket_names[count.index]
}
resource "aws_s3_bucket_acl" "project_buckets_acl" {
  count  = length("${var.bucket_names}")
  bucket = var.bucket_names[count.index]
  acl    = "private"
}

data "archive_file" "twitter_extract" {
  type        = "zip"
  output_path = "${path.module}/lambda_files/twitter_extract.zip"
  source_dir  = "${path.module}/twitter_extract"
}

data "archive_file" "sentiment_analysis" {
  type        = "zip"
  output_path = "${path.module}/lambda_files/sentiment_analysis.zip"
  source_dir  = "${path.module}/sentiment_analysis"
}

data "archive_file" "load_to_rds" {
  type        = "zip"
  output_path = "${path.module}/lambda_files/load_to_rds.zip"
  source_dir  = "${path.module}/rds_load"
}

resource "aws_lambda_layer_version" "tweepy" {
  filename            = "modules/tweepy.zip"
  layer_name          = "tweepy"
  compatible_runtimes = ["python3.9"]
}

resource "aws_lambda_function" "pull_data_from_twitter" {
  depends_on       = [data.archive_file.twitter_extract]
  filename         = "lambda_files/twitter_extract.zip"
  function_name    = "pull-data-from-twitter"
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("lambda_files/twitter_extract.zip")
  runtime          = "python3.9"
  layers = [
    aws_lambda_layer_version.tweepy.arn,
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p39-pandas:5",
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p39-numpy:5"
  ]
  memory_size = 512
  timeout     = 60
  ephemeral_storage {
    size = 512
  }
  environment {
    variables = {
      TWITTER_TOKEN = "${var.TWITTER_TOKEN}"
    }
  }
}

resource "aws_lambda_function" "twitter_sentiment_analysis" {
  depends_on       = [data.archive_file.sentiment_analysis]
  filename         = "lambda_files/sentiment_analysis.zip"
  function_name    = "twitter_sentiment_analysis"
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("lambda_files/sentiment_analysis.zip")
  runtime          = "python3.8"
  layers = [
    aws_lambda_layer_version.tweepy.arn,
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p38-nltk:4",
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p38-pandas:5"
  ]
  memory_size = 512
  timeout     = 60
  ephemeral_storage {
    size = 512
  }

}

resource "aws_lambda_function" "load_data_from_s3_in_rds" {
  depends_on       = [data.archive_file.load_to_rds]
  filename         = "lambda_files/load_to_rds.zip"
  function_name    = "load_data_from_s3_in_rds"
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("lambda_files/load_to_rds.zip")
  runtime          = "python3.8"
  layers = [
    aws_lambda_layer_version.tweepy.arn,
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p38-pandas:5",
    "arn:aws:lambda:eu-west-1:898466741470:layer:psycopg2-py38:1"
  ]
  memory_size = 512
  timeout     = 100
  ephemeral_storage {
    size = 512
  }

  environment {
    variables = {
      POSTGRES_HOST     = "${var.POSTGRES_HOST}"
      POSTGRES_PORT     = "${var.POSTGRES_PORT}"
      POSTGRES_DB       = "${var.POSTGRES_DB}"
      POSTGRES_USERNAME = "${var.db_username}"
      POSTGRES_PASSWORD = "${var.db_password}"
    }
  }

}


resource "aws_cloudwatch_event_rule" "every_day_at_8" {
  name                = "every-day-at-8"
  description         = "Fires every day at 8 am"
  schedule_expression = "cron(0 8 * * ? *)"
}

resource "aws_cloudwatch_event_rule" "every_day_at_9" {
  name                = "every-day-at-9"
  description         = "Fires every day at 9 am"
  schedule_expression = "cron(0 9 * * ? *)"
}

resource "aws_cloudwatch_event_target" "pull_data_from_twitter_at_8" {
  rule      = aws_cloudwatch_event_rule.every_day_at_8.name
  target_id = "pull_data_from_twitter"
  arn       = aws_lambda_function.pull_data_from_twitter.arn
}
resource "aws_lambda_permission" "allow_cloudwatch_to_call_pull_data_from_twitter" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pull_data_from_twitter.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_day_at_8.arn
}

resource "aws_cloudwatch_event_target" "run_sentiment_analysis_at_9" {
  rule      = aws_cloudwatch_event_rule.every_day_at_9.name
  target_id = "twitter_sentiment_analysis"
  arn       = aws_lambda_function.twitter_sentiment_analysis.arn
}
resource "aws_lambda_permission" "allow_cloudwatch_to_call_twitter_sentiment_analysis" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.twitter_sentiment_analysis.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_day_at_9.arn
}

resource "aws_cloudwatch_event_target" "run_rds_load_at_9" {
  rule      = aws_cloudwatch_event_rule.every_day_at_9.name
  target_id = "load_data_from_s3_in_rds"
  arn       = aws_lambda_function.load_data_from_s3_in_rds.arn
}
resource "aws_lambda_permission" "allow_cloudwatch_to_call_load_data_from_s3_in_rds" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.load_data_from_s3_in_rds.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_day_at_9.arn
}

