# Data Pipeline - Project Proposal

#### Manveer Sadhal
#### Oct 6, 2021

## Need
Investors in publicly traded equities need a way to research fundamentals of individual stocks and track the performance of their portfolio. The intent of this project is to create an interactive dashboard which will allow users to look up individual stocks, enter the details of their own portfolio, and track performance over time.

## Data Description
Public US stock market data will be retrieved using finance-related APIs, such as Yahoo Finance and Alpha Vantage.

An example of an individual data point would be the price of a stock at a given date and time (e.g. market close for AMZN on October 4th, 2021).

## Tools
- Data Acquisition and Storage
    - Google BigQuery
- Dashboard / User Interface
    - Google Data Studio or Heroku or Flask

## MVP Goal
Build an interactive dashboard that will allow a user to enter the ticker of a publicly traded company and retrieve fundamental data (e.g. market cap, revenue, price to earnings ratio). Also, display plots of major indices over a time interval selected by the user.