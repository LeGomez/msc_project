# Data Lake Project

This repository contains code to spin up data lake infrastructure in AWS, set up lambda functions that will pull data from twitter, run sentiment analysis, and push business data from S3 buckets over to a PostgreSQL database in AWS RDS. <br />

The infrastructure is all built using Terraform. And it's automated to build on push to main branch using GitHub Actions. <br />

## Setup

### <ins>Environment Variables and local development setup</ins>

After forking the repository, a few variables will have to be set through secrets manager.

aws_access_key -> This is the access id to access the AWS instance where the infrastructure will be built <br />
aws_secret_key -> This is the access key for the AWS account <br />
TWITTER_TOKEN -> API Token to connect to the twitter API and pull data <br />
DB_USERNAME -> The username you want the master credentials to be handed to <br />
DB_PASSWORD -> The password for the above-mentioned username <br />
POSTGRES_HOST -> The host name for the RDS instance created, this will likely be project.{account_identifier}.{region}.rds.amazonaws.com <br />
POSTGRES_DB -> This will be the default value (postgres) <br />
POSTGRES_PORT -> This will be the default value (5432) <br />

After cloning the repository, a .env file should be created containing the same credentials placed in the repo, following the .env.example file.

After this, run 'make venv' to create the virtual environment.

Now run 'make reqs' to install all requirements.

if you want to run terraform locally, you can. But you will either have to export the variables like the aws_access_key into the virtual environment, or place the credentials where the variables are defined in variables.tf. Beware not to push these to the repo for security reasons.

### <ins>Loading data</ins>

After triggering Terraform once, the infrastructure should have all been built. This means we're missing data.

In order to populate the S3 buckets with fake data run the 'make data' command, which will create a series of files with fake business data. This is the data that one of the AWS Lambda functions will use to create tables in the data warehouse.

You can also run 'make twitter_data && make sentiment_analysis' to run the twitter data extraction and sentiment analysis scripts.

### <ins>Executing Terraform Commands Locally </ins>

This implementation was designed to run Terraform exclusively through GH Actions.

It is possible, however, to run it locally for testing purposes. These steps are required: <br />

- Run 'make venv/activate' command to enter the virtual environment <br />

- Change working directory to the ./terraform folder <br />

- Execute the following command in the terminal for each of the required environment variables: 'export <variable_name>=<variable_value>' <br />

- Now you can run terraform init, plan, and apply.
