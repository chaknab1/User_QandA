# Import Required Packages
import os
import pickle
import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


#########################  Load Constituent Stock Prices data  #########################

# ------- 1. read the data file
wb_df= pd.read_csv('./data/world_bank_dataset.csv')
print(wb_df.head())

co_emissions_df= pd.read_csv('./data/co_emissions_per_capita.csv')
print(co_emissions_df.head())

stock_df= pd.read_csv('./data/all_stock_prices.csv')
print(stock_df.head())


# ------- 2. Create a SQLite Database (in-memory) -------------------
import sqlite3
print('sqlite version : ', sqlite3.sqlite_version)

# Connect to a sqlite DB (It will create it if it doesn't exist)
conn = sqlite3.connect('combo_db.sqlite')
print("Opened database successfully");

### Create a table 'stock_prices' in DB

#conn.execute('''DROP table world_bank;''')
#print("drop successfully")

conn.execute('''
CREATE TABLE IF NOT EXISTS world_bank(
                      country VARCHAR(100),
                      year INT,
                      gdp_usd DOUBLE,
                      population DOUBLE,
                      life_expectancy DOUBLE,
                      unemployment_rate DOUBLE,
                      access_to_electricity_percentage DOUBLE);''')

#2. co emissions table
conn.execute('''
CREATE TABLE IF NOT EXISTS carbon_emissions(
                      entity VARCHAR(100),
                      co2_emissions_metric_tons_per_capita DOUBLE);''')

#3. Stock table
conn.execute('''
CREATE TABLE IF NOT EXISTS stock_prices(
                      date DATE,
                      open DOUBLE,
                      high DOUBLE,
                      low DOUBLE,
                      close DOUBLE,
                      volume INT,
                      symbol VARCHAR(20));''')


conn.commit()
print("all 3 Tables created successfully")

### Show tables
cursor = conn.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
for row in cursor:
    print(row)


### Insert data into tables
conn.executemany('''
INSERT INTO world_bank (country, year, gdp_usd, population, life_expectancy, unemployment_rate, access_to_electricity_percentage) VALUES (?, ?, ?, ?, ?, ?, ?)
''', wb_df.values)
#conn.commit()
print("world_bank data inserted successfully!")

conn.executemany('''
INSERT INTO carbon_emissions (entity, co2_emissions_metric_tons_per_capita) VALUES (?, ?)
''', co_emissions_df.values)
#conn.commit()
print("carbon_emissions data inserted successfully!")


conn.executemany('''
INSERT INTO stock_prices (date, open, high, low, close, volume, symbol) VALUES (?, ?, ?, ?, ?, ?, ?)
''', stock_df.values)
conn.commit()
print("stock_prices data inserted successfully!")

# Show table content
cursor = conn.execute('''SELECT * from world_bank limit 5;''')
for row in cursor:
    print(row)

cursor = conn.execute('''SELECT * from carbon_emissions limit 5;''')
for row in cursor:
    print(row)

cursor = conn.execute('''SELECT * from stock_prices limit 5;''')
for row in cursor:
    print(row)






### Close the DB connection
conn.close()
print("DB connection closed!")
