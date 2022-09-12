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

