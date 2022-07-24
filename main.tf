terraform {
  required_providers {
      aws = {
          source = "hashicorp/aws"
          version= "~> 4.23"
      }
  }
}

provider "aws" {
  profile = "default"
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  region = "${var.region}"
}

module "s3" {
    source = "/s3"
}