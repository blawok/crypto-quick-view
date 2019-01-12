import pandas as pd
import sqlite3
from scraper import cryptoInfoToDf
from sqlalchemy.types import DateTime

def insertCrypto(varCurrency = 'LSK', varFromDate = '13-07-2018',
                    varToDate = '1-08-2018'):
    df = cryptoInfoToDf(varCurrency, varFromDate, varToDate)

    # ? casting timestamp column to date
    df['Date'] = pd.to_datetime(df['Date']).apply(lambda x: x.date())
    df['Currency'] = "{}".format(varCurrency)

    conn = sqlite3.connect('cryptoDB.db')
    df.to_sql("cryptoStats", conn, if_exists="append")
    pd.read_sql_query("select * from cryptoStats;", conn)

    conn.commit()
    conn.close()

# insertCrypto()
# * CREATE TABLE cryptoStats ("index" INTEGER, createdDate DEFAULT (datetime('now')), Date DATE, "Open*" REAL, High REAL, Low REAL, "Close**" REAL, Volume INTEGER, "Market Cap" INTEGER, "Currency" TEXT);
