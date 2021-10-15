# Stock Market Data Pipeline

Manveer Sadhal

## Abstract
The goal of this project was to make an end-to-end data storage and processing pipeline. 15 years of US stock market data from 2,000 of today's largest companies was retrieved using the Yahoo Finance API. The data was then transformed in Pandas dataframes with minor cleaning in order to prepare for ingestion into a SQL database. Approximately 5.5 million rows of data were collected and stored.

With the deep repository of stock market data established, a web application was developed using Streamlit to allow a user to enter a ticker symbol and retrieve general company info as well as market close history and financial metrics. The app was deployed to the web using Heroku.

## Design
Stock market data is useful to both retail and institutional investors to make informed decisions. In order to provide updated information, a data pipeline was developed to ensure that the end user would be able to access up-to-date and accurate information through a web application. Data downloading, cleaning, and appending to the existing data set has been completely automated.

## Data
### Yahoo Finance API
Data was retrieved from the Yahoo Finance API via the yfinance Python library. 15 years of stock market data from the top 2,000 companies by market cap were retrieved, totaling approximately 5.5 million rows of data.


## Algorithms
### Cleaning
Data retrieved from the Yahoo Finance API required transformation into long format so that it could be inserted into the SQL database and queried by the web application as intended. Minor cleaning was also performed using Pandas.

### Visualization
Plotly was used to create an interactive plot in the final web application.

### Automation
A Python script was written to automatically run each evening after market close to retrieve new data, transform as required, and insert into the database for use by the web application. The script has been scheduled to run as a Cron job.

## Tools
- Data Retrieval
    - Yahoo Finance API via yfinance library
- Data Cleaning/Transformation
    - Pandas and NumPy
- Data Visualization
    - Plotly
- Data Storage
    - SQLAlchemy for database connection
    - Pandas to update database
- Web App Development
    - Streamlit
- Web App Deployment
    - Heroku

## Communication
A summary of the data pipeline will be communicated during a 5-minute slide presentation.

The web app hosted by Heroku can be accessed [here](https://warm-reef-29600.herokuapp.com/).
