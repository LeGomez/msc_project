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

resource "aws_s3_bucket_acl" "project_buckets" {
    count = length("${var.bucket_names}")
    bucket = "${var.bucket_names[count.index]}"
    acl = "${var.acl_value}"
}

resource "aws_lambda_function" "pull_data_from_twitter" {
  filename="lambda_files/twitter_extract.zip"
  function_name = "project-pull-data-from-twitter"
  role = aws_iam_role.iam_for_lambda
  handler = "index.test"
  source_code_hash = filebase64sha256("lambda_files/twitter_extract.zip")
  runtime = "Python3.9"
  layers = [ 
    "aws_lambda_layer_version.tweepy.arn", 
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p39-pandas:5",
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p39-numpy:5"
  ]
  memory_size = 512
  ephemeral_storage {
    size = 512
  }
  environment {
    variables = {
      twitter_token = "${var.TWITTER_TOKEN}"
    }
  }

  
}

resource "aws_lambda_layer_version" "tweepy" {
  filename = "modules/tweepy.zip"
  layer_name = "tweepy"
  compatible_runtimes = [ "python3.9" ]
}

