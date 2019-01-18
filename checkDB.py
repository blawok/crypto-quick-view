import sqlite3
from datetime import datetime
import pandas as pd
from coinScraper import coinScraper


def appendIfNotExist(currency, fromDate, tillDate):

    def days_between(d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)

    query = """
            select
            count(distinct Date)
            from cryptoStats
            where Currency = '{0}'
                and Date between '{1}' and '{2}';
            """.format(currency, fromDate, tillDate)

    # ? connect to DB
    conn = sqlite3.connect('cryptoDB.db')

    # ? create cursor (tunnel to db) and execute the query
    c = conn.cursor()
    c.execute(query)

    numberOfDistinctDates = int(c.fetchone()[0])
    # ? number of days between dates
    numberOfDays = days_between(tillDate, fromDate) + 1

    if (numberOfDays != numberOfDistinctDates):
        dfTemp = coinScraper(currency, fromDate, tillDate)

        # ? casting timestamp column to date
        dfTemp['Date'] = pd.to_datetime(dfTemp['Date']).apply(lambda x: x.date())
        dfTemp['Currency'] = "{}".format(currency)

        # ? inserting df to db
        dfTemp.to_sql("cryptoStatsUser", conn, if_exists="append")
        tempQuery = """
                    create temp table cryptoStatsTemp as
                        select
                            csu.Date,
                            csu.Open,
                            csu.High,
                            csu.Low,
                            csu.Close,
                            csu.Volume,
                            csu."Market Cap",
                            csu.Currency
                        from cryptoStatsUser csu
                        left join cryptoStats cs
                            on cs.Currency = csu.Currency and cs.Date = csu.Date
                        where cs.Currency is null;
                    """
        c.execute(tempQuery)
        insertQuery = """
                      insert into cryptoStats
                      (Date, Open, High, Low, Close, Volume, "Market Cap", Currency)
                      select *
                      from cryptoStatsTemp;
                      """
        c.execute(insertQuery)
        conn.commit()
        conn.close()

# checkIfExists('lisk', '2017-12-25', '2018-01-05')
