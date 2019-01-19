import sqlite3
import pandas as pd

from datetime import datetime
from sqlalchemy.types import DateTime
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



def executeSqlCrypto(varCurrency = 'lisk', varFromDate = '2018-01-01',
                     varToDate = '2018-12-31'):
    conn = sqlite3.connect('cryptoDB.db')

    # ? create cursor (tunnel to db)
    c = conn.cursor()

    query = """
            select *
            from cryptoStats
            where Currency = "{a}"
                and Date between "{b}" and "{c}"
            order by Date desc;
            """.format(a = varCurrency,
                       b = varFromDate,
                       c = varToDate)

    df = pd.read_sql_query(query, conn)

    conn.close()
    return df



def getFromDatabase(currency, fromDate, tillDate, outputType):

    # ? connect to DB
    conn = sqlite3.connect('cryptoDB.db')

    # ? create cursor (tunnel to db) and execute the query
    c = conn.cursor()

    if outputType == 'max':
        queryMax = """
                select
                max(High)
                from cryptoStats
                where Currency = '{0}'
                    and Date between '{1}' and '{2}'
                group by Currency;
                """.format(currency, fromDate, tillDate)


        c.execute(queryMax)
        maxHigh = float(c.fetchone()[0])
        return maxHigh

    elif outputType == 'min':
        queryMin = """
                select
                min(Low)
                from cryptoStats
                where Currency = '{0}'
                    and Date between '{1}' and '{2}'
                group by Currency;
                """.format(currency, fromDate, tillDate)

        c.execute(queryMin)
        minLow = float(c.fetchone()[0])
        return minLow

    elif outputType == 'monthData':
        monthQuery = """
                    select
                    Currency,
                    strftime('%m', Date) as Month,
                    strftime('%Y', Date) as Year,
                    max(Close) maxClose,
                    min(Close) minClose
                    from cryptoStats
                    where Currency = '{}'
                    group by Year, Month;
                     """.format(currency)
        c.execute(monthQuery)
        dfMonthData = pd.read_sql_query(monthQuery, conn)
        return dfMonthData



def getGroupedData():

    # ? connect to DB
    conn = sqlite3.connect('cryptoDB.db')

    # ? create cursor (tunnel to db) and execute the query
    c = conn.cursor()

    dfGroupedQuery = """
                     select
                     Currency,
                     max(Close) maxClose,
                     min(Close) minClose,
                     min(Date) minDate,
                     max(Date) maxDate
                     from cryptoStats
                     group by Currency;
                     """
    c.execute(dfGroupedQuery)
    dfGrouped = pd.read_sql_query(dfGroupedQuery, conn)
    return dfGrouped
