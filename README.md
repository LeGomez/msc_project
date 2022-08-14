# Data Lake Project

This repository contains code to spin up data lake infrastructure in AWS, set up lambda functions that will pull data from twitter, run sentiment analysis, and push business data from S3 buckets over to a PostgreSQL database in AWS RDS.

The infrastructure is all built using Terraform. And it's automated to build on push to main branch using GitHub Actions.

## Setup

### Environment Variables and local development setup

After forking the repository, a few variables will have to be set through secrets manager.

aws_access_key -> This is the access id to access the AWS instance where the infrastructure will be built
aws_secret_key -> This is the access key for the AWS account
TWITTER_TOKEN -> API Token to connect to the twitter API and pull data
DB_USERNAME -> The username you want the master credentials to be handed to
DB_PASSWORD -> The password for the above-mentioned username
POSTGRES_HOST -> The host name for the RDS instance created, this will likely be project.{account_identifier}.{region}.rds.amazonaws.com
POSTGRES_DB -> This will be the default value (postgres)
POSTGRES_PORT -> This will be the default value (5432)

After cloning the repository, a .env file should be created containing the same credentials placed in the repo, following the .env.example file.

After this, run 'make venv' to create the virtual environment.

Now run 'make reqs' to install all requirements.

if you want to run terraform locally, you can. But you will either have to export the variables like the aws_access_key into the virtual environment, or place the credentials where the variables are defined in variables.tf. Beware not to push these to the repo for security reasons.

### Loading data

After triggering Terraform once, the infrastructure should have all been built. This means we're missing data.

In order to populate the S3 buckets with fake data run the 'make data' command, which will create a series of files with fake business data. This is the data that one of the AWS Lambda functions will use to create tables in the data warehouse.

You can also run 'make twitter_data && make sentiment_analysis' to run the twitter data extraction and sentiment analysis scripts.

