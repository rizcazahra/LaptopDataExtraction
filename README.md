# LaptopDataExtraction

This Jupyter Notebook is designed to scrape pagination data (20 pages) from the "Laptops Direct" website (https://www.laptopsdirect.co.uk). We will extract information about laptops, including the name, price, and description of each laptop product.

The script uses Python and several libraries for web scraping, including requests, BeautifulSoup, and pandas. The data is extracted, processed, and then saved into a PostgreSQL database using the 'psycopg2' library and 'SQLAlchemy' for further analysis.

The data is cleaned during the scraping process using various techniques such as `strip()` and `replace()`. These methods are employed to ensure that the extracted data is formatted properly and free from unnecessary characters or whitespace.
