import pandas as pd
import sqlite3
from scraper import cryptoInfoToDf
from coinScraper import coinScraper
from sqlalchemy.types import DateTime

def insertCrypto(varCurrency = 'lisk', varFromDate = '2018-01-01',
                 varToDate = '2018-12-31'):
    df = coinScraper(varCurrency, varFromDate, varToDate)

    # ? casting timestamp column to date
    df['Date'] = pd.to_datetime(df['Date']).apply(lambda x: x.date())
    df['Currency'] = "{}".format(varCurrency)

    # ? connecting to db
    conn = sqlite3.connect('cryptoDB.db')
    # ? inserting df to db
    df.to_sql("cryptoStats", conn, if_exists="append")
    pd.read_sql_query("select * from cryptoStats;", conn)

    conn.commit()
    conn.close()

insertCrypto()
# * CREATE TABLE cryptoStats ("index" INTEGER, createdDate DEFAULT (datetime('now')), Date DATE, "Open*" REAL, High REAL, Low REAL, "Close**" REAL, Volume INTEGER, "Market Cap" INTEGER, "Currency" TEXT);
# * CREATE TABLE cryptoStats ("index" INTEGER, createdDate DEFAULT (datetime('now')), Date DATE, Open REAL, High REAL, Low REAL, Close REAL, Volume REAL, "Market Cap" REAL, Currency TEXT);

# list of cryptocurrencies:
# def insertAllCrypto():
#     cryptoList = ['BTC', 'ETH', 'BCH', 'LTC', 'MIOTA', 'XMR', 'ETC', 'DOGE', 'LSK']
#     for item in cryptoList:
#         insertCrypto('{}'.format(item))

"""
if (currencyStats between date1 and date2 not in DB):
    insertData
    select
else:
    select
"""
