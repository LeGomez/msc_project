terraform {
  required_providers {
      aws = {
          source = "hashicorp/aws"
          version= "~> 4.23"
      }
  }
}

provider "aws" {
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  region = "${var.region}"
}

resource "aws_s3_bucket" "project_buckets" {
  count = length("${var.bucket_names}")
  bucket = "${var.bucket_names[count.index]}"
}
resource "aws_s3_bucket_acl" "project_buckets_acl" {
  count = length("${var.bucket_names}")
  bucket = "${var.bucket_names[count.index]}"
  acl = "private"
}

data "archive_file" "twitter_extract" {
    type = "zip"
    output_path = "${path.module}/lambda_files/twitter_extract.zip"
    source_dir = "${path.module}/twitter_extract"
}

data "archive_file" "sentiment_analysis" {
    type = "zip"
    output_path = "${path.module}/lambda_files/sentiment_analysis.zip"
    source_dir = "${path.module}/sentiment_analysis"
}


resource "aws_lambda_layer_version" "tweepy" {
  filename = "modules/tweepy.zip"
  layer_name = "tweepy"
  compatible_runtimes = [ "python3.9" ]
}

resource "aws_lambda_function" "pull_data_from_twitter" {
  depends_on = [data.archive_file.twitter_extract]
  filename="lambda_files/twitter_extract.zip"
  function_name = "pull-data-from-twitter"
  role = aws_iam_role.iam_for_lambda.arn
  handler = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("lambda_files/twitter_extract.zip")
  runtime = "python3.9"
  layers = [ 
    aws_lambda_layer_version.tweepy.arn, 
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p39-pandas:5",
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p39-numpy:5"
  ]
  memory_size = 512
  timeout = 60
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
  depends_on = [data.archive_file.sentiment_analysis]
  filename="lambda_files/sentiment_analysis.zip"
  function_name = "twitter_sentiment_analysis"
  role = aws_iam_role.iam_for_lambda.arn
  handler = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("lambda_files/sentiment_analysis.zip")
  runtime = "python3.8"
  layers = [ 
    aws_lambda_layer_version.tweepy.arn, 
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p38-nltk:4",
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p38-pandas:5"
  ]
  memory_size = 512
  timeout = 60
  ephemeral_storage {
    size = 512
  }
  
}


