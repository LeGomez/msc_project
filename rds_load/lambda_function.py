import json
import boto3
from sqlite3 import OperationalError
import psycopg2
from io import BytesIO
import pandas as pd
import os

def lambda_handler(event, context):
    host=os.environ["POSTGRES_HOST"]
    port=os.environ["POSTGRES_PORT"]
    database=os.environ["POSTGRES_DB"]
    user=os.environ["POSTGRES_USERNAME"]
    password=os.environ["POSTGRES_PASSWORD"]

    bucket = "project-business-data"


    year = 2022
    months_in_record = 5

    # The following number of iterations is hardcoded for the number of months of data we have available.
    # However it would be a simple refactor to make it scale with the number of files that exist in the bucket.

    try:
        connection = psycopg2.connect(
            user = user,
            password = password,
            host = host,
            port = port,
            database = database
        )
    except OperationalError:
        print("Check connection details and IP address used") 

    cursor = connection.cursor()

    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

    cursor.execute("CREATE SCHEMA IF NOT EXISTS business")
    cursor.execute(f"SET search_path = business")

    s3_client = boto3.client('s3', aws_access_key_id = os.environ["AWS_ACCESS_KEY"], aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"])

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS events (

                created_at    TIMESTAMP,
                id            VARCHAR(100),
                type          VARCHAR(100),
                user_id       VARCHAR(100)
            )
            ;
        """
    )
    print("events done")

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS sessions (

                created_at       TIMESTAMP,
                id               VARCHAR(100),
                url              VARCHAR(100),
                pages_visited    INT
            )
            ;
        """
    )
    print("sessions done")

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS sales (

                id            VARCHAR(100),
                created_at    TIMESTAMP,
                product_id    VARCHAR(100),
                quantity      INT,
                user_id       VARCHAR(100),
                invoice_id    VARCHAR(100)
            )
            ;
        """
    )
    print("sales done")

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS invoices (

                id            VARCHAR(100),
                created_at    TIMESTAMP,
                status        VARCHAR(100),
                paid_at       TIMESTAMP
            )
            ;
        """
    )
    print("invoices done")

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS stock (

                month         INT,
                facility      VARCHAR(100),
                product_id    INT,
                units         INT
            )
            ;
        """
    )
    print("stock done")

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS users (

                user_id       VARCHAR(100),
                address       VARCHAR(250),
                email         VARCHAR(100),
                created_at    TIMESTAMP
            )
            ;
        """
    )
    print("users done")

    for i in range(1, months_in_record+1):
        print(f'month {i}')
        tables_dict = {
            f'events_{i}_{year}.csv': 'events',
            f'sessions_{i}_{year}.csv': 'sessions',
            f'sales_{i}_{year}.csv': 'sales',
            f'invoices_{i}_{year}.csv': 'invoices',
            f'stock_{i}_{year}.csv': 'stock',
        }

        for key in tables_dict:
            print(key)
            response = s3_client.get_object(Bucket=bucket, Key=key)
            data = response['Body'].read()
            df = pd.read_csv(BytesIO(data))

            df.to_csv(
                '/tmp/output.csv',
                header=True,
                index=False
            )

            with open('/tmp/output.csv', 'r') as file:
                    cursor.copy_expert(f"COPY {tables_dict[key]} FROM STDIN WITH CSV HEADER DELIMITER AS ','", file=file)

    # Handle users table
    response = s3_client.get_object(Bucket=bucket, Key='users.csv')
    data = response['Body'].read()
    df = pd.read_csv(BytesIO(data))

    df.to_csv(
        '/tmp/output.csv',
        header=True,
        index=False
    )

    with open('/tmp/output.csv', 'r') as file:
            cursor.copy_expert(f"COPY users FROM STDIN WITH CSV HEADER DELIMITER AS ','", file=file)

    print('success')

    connection.commit()
    connection.close()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

