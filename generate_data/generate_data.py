import pandas as pd
import random
from faker import Faker
from datetime import datetime
from helpers import upload_file

number_of_entries = 25000

link_options = [
    '/home',
    '/myaccount',
    '/summerpromo',
    '/2022-summer-promo'
]

utm_source_options = [
    'facebook',
    'instagram',
    'third-party',
    'tiktok',
    'twitter',
    'reddit',
    'direct-sales',
    ''
]

event_types = [
    'page_view',
    'click',
    'order_completed',
    'suspended'
]

invoice_statuses = [
    'pending',
    'paid',
    'paid',
    'paid',
    'unpaid',
    'free'
]

utm_campaign_options = []

Faker.seed(0)
fake = Faker('en_GB')

sessions = []
events = []
sales = []
invoices = []

for i in range(1, 6):
    sessions = []
    events = []
    for entry in range(number_of_entries):

        start_date = datetime.strptime(f'{i}/1/2022', '%m/%d/%Y')
        end_date = datetime.strptime(f'{i + 1}/1/2022', '%m/%d/%Y')

        sessions_created_at = fake.date_time_between(start_date, end_date)
        session_id = fake.ean(length=13)
        session_url = 'www.woof.com' + random.choice(link_options) + '?utm_source=' + random.choice(utm_source_options)
        session_pages_visited = fake.random_int(0, 10)
        sessions.append([sessions_created_at, session_id, session_url, session_pages_visited])

        event_created_at = fake.date_time_between(start_date, end_date)
        event_id = fake.ean(length=13)
        event_type = random.choice(event_types)
        event_user_id = fake.ean(length=8)
        events.append([event_created_at, event_id, event_type, event_user_id])

        sales_id = fake.ean(length=13)
        sales_created_at = fake.date_time_between(start_date, end_date)
        invoices_created_at = sales_created_at
        sales_product_id = fake.random_int(1, 25)
        sales_quantity = fake.random_int(1, 5)
        sales_user_id = fake.ean(length=8)
        invoices_user_id = sales_user_id
        sales_invoice_id = fake.ean(length=13)
        invoice_id = sales_invoice_id
        sales.append([sales_id, sales_created_at, sales_product_id, sales_quantity, sales_user_id, sales_invoice_id])

        invoices_status = random.choice(invoice_statuses)
        invoices_paid_at = fake.date_time_between(invoices_created_at, end_date)
        invoices.append([invoice_id, invoices_created_at, invoices_status, invoices_paid_at])


        print(f'Month {i} - {entry}/{number_of_entries}')

    sessions_df = pd.DataFrame(sessions, columns=['created_at', 'id', 'url', 'pages_visited'])

    sessions_df.to_csv(
        f'sessions_{i}_2022.csv',
        header=True,
        index=False
    )

    upload_file(f'sessions_{i}_2022.csv', 'project-business-data')

    events_df = pd.DataFrame(events, columns=['created_at', 'id', 'type', 'user_id'])

    events_df.to_csv(
        f'events_{i}_2022.csv',
        header=True,
        index=False
    )

    upload_file(f'events_{i}_2022.csv', 'project-business-data')

    sales_df = pd.DataFrame(sales, columns=['id', 'created_at', 'product_id', 'quantity', 'user_id', 'invoice_id'])

    sales_df.to_csv(
        f'sales_{i}_2022.csv',
        header=True,
        index=False
    )
    
    upload_file(f'sales_{i}_2022.csv', 'project-business-data')

    invoices_df = pd.DataFrame(invoices, columns=['id', 'created_at', 'status', 'paid_at'])

    invoices_df.to_csv(
        f'invoices_{i}_2022.csv',
        header=True,
        index=False
    )

    upload_file(f'invoices_{i}_2022.csv', 'project-business-data')


# User data
users = []

start_date = datetime.strptime(f'1/1/2018', '%m/%d/%Y')
end_date = datetime.strptime(f'1/1/2022', '%m/%d/%Y')

number_of_entries = 30000
for i in range(number_of_entries):

    user_id = fake.ean(length=8)
    address = fake.address()
    email = f"{fake.first_name()}__{fake.last_name()}@{fake.domain_name()}"
    created_at = fake.date_time_between(start_date, end_date)
    users.append([user_id, address, email, created_at])

    print(f'{i}/{number_of_entries}')

users_df = pd.DataFrame(users, columns=['id', 'created_at', 'status', 'paid_at'])

users_df.to_csv(
    'users.csv',
    header=True,
    index=False
)

upload_file(f'users.csv', 'project-business-data')

distribution_centers = [
    'Midlands', 
    'Devon',
    'Glasgow'
]

for i in range(1, 6):
    stock = []  
    for n in range(1, 25):
        for center in distribution_centers:
            facility = center
            product_id = n
            units = fake.random_int(500, 30000)
            stock.append([i, facility, product_id, units])
    stock = pd.DataFrame(stock, columns=['month', 'facility', 'product_id', 'units'])
    stock.to_csv(
        f'stock_{i}_2022.csv',
        header=True,
        index=False
    )
    upload_file(f'stock_{i}_2022.csv', 'project-business-data')
