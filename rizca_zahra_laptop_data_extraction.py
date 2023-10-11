# Import necessary libraries
import requests
import urllib.parse
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import os

# Define the URL to scrape
url = 'https://www.laptopsdirect.co.uk/ct/laptops-and-netbooks/laptops?'

# Send a GET request to the URL
response = requests.get(url)

# Check the HTTP status code
status_code = response.status_code
status_code

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all elements with the class 'OfferBox'
results = soup.find_all('div', {'class': 'OfferBox'})

# Count the number of results
num_results = len(results)
num_results

# Pagination - Scrape 20 pages
# For each page, we will extract these 4 columns:
# 1. Name
# 2. Price
# 3. Product Link
# 4. Product Details

product_name = []
product_price = []
relative_url = []
product_details = []

for i in range(1, 21):
    # website in variable
    website = 'https://www.laptopsdirect.co.uk/ct/laptops-and-netbooks/laptops?' + str(i)

    # request
    response = requests.get(website)

    # soup object
    soup = BeautifulSoup(response.content, 'html.parser')

    # results
    results = soup.find_all('div', {'class': 'OfferBox'})

    # provide the root element inside a variable
    root_url = 'https://www.laptopsdirect.co.uk'

    # loop through results
    for result in results:
        # name
        try:
            product_name.append(result.find('a', {'class': 'offerboxtitle'}).get_text())
        except:
            product_name.append('n/a')

        # price
        try:
            product_price.append(result.find('span', {'class': 'offerprice'}).get_text().strip().replace('\n', ''))
        except:
            product_price.append('n/a')

        # relative url
        try:
            relative_url.append(result.find('a', {'class': 'offerboxtitle'}).get('href'))
        except:
            relative_url.append('n/a')

        # product detail
        try:
            product_details.append(result.find('div', {'class': 'productInfo'}).get_text().strip().replace('\n', ', '))
        except:
            product_details.append('n/a')

# Combine relative URLs with the root URL
url_combined = []

for link in relative_url:
    url_combined.append(urllib.parse.urljoin(root_url, link))

# Create a Pandas DataFrame to store the data
product_overview = pd.DataFrame({'Name': product_name, 'Price': product_price, 'Link': url_combined, 'Details': product_details})

# Define the PostgreSQL connection details
pg_user = os.environ.get("PG_USER")
pg_pass = os.environ.get("PG_PASS")
pg_host = "localhost"
pg_port = "5432"  
pg_db = "laptop_data"

# Define the table name
table_name = "laptop_data"  

# Define the database URL
db_url = f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"

# Create an SQLAlchemy engine
engine = create_engine(db_url)

# Connect to the database
con = engine.connect()

# Create the table using the DataFrame's 'to_sql' method
product_overview.to_sql(table_name, con, if_exists='replace', index=False)

# Close the database connection
con.close()
