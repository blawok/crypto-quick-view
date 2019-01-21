import sqlite3
import pandas as pd

from datetime import datetime
from sqlalchemy.types import DateTime
from coinScraper import coinScraper
from jsonScraper import cryptoInfoToDf


def appendIfNotExist(currency, fromDate, tillDate):
    """
    variables:
        currency - string value of currency name
        fromDate - date in format of YYYY-MM-DD
        tillDate - date in format of YYYY-MM-DD

    returns:
        check if certain values are in database
        scrape and insert values that are not yet in database
        does not return anything
    """
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
        # dfTemp = coinScraper(currency, fromDate, tillDate)
        dfTemp = cryptoInfoToDf(currency, fromDate, tillDate)
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
    """
    variables:
        varCurrency - string value of currency name
        varFromDate - date in format of YYYY-MM-DD
        varToDate - date in format of YYYY-MM-DD

    returns:
        execute query that selects all values from database
        for given interval and cryptocurrency
        returns dataframe created by query
    """
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
    """
    variables:
        currency - string value of currency name
        fromDate - date in format of YYYY-MM-DD
        tillDate - date in format of YYYY-MM-DD
        outputType - string that indicates which query to use

    returns:
        execute query that selects values from database
        based on chosen outputType
        returns dataframe created by query or an integer
    """
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
        conn.close()
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
        conn.close()
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
        conn.close()
        return dfMonthData



def getGroupedData():
    """
    returns:
        execute query that selects values from database
        grouped by currency
        returns dataframe created by query
    """
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
    conn.close()
    return dfGrouped



def getCurrencyNames(currency='lisk'):
    """
    variables:
        currency - string containing currency name
    returns:
        execute query
        returns dataframe created by query
    """
    # ? connect to DB
    conn = sqlite3.connect('cryptoDB.db')

    # ? create cursor (tunnel to db) and execute the query
    c = conn.cursor()

    dfNamesQuery = """
                     select
                     distinct cd.CurrencyShort
                     from cryptoDict cd
                     join cryptoStats cs
                        on cd.Currency = cs.Currency
                     where cs.Currency = '{}';
                     """.format(currency)

    c.execute(dfNamesQuery)
    shortcut = str(c.fetchone()[0])
    conn.close()
    return shortcut



def updateDataBase(currency='lisk', dataUpdate = '2018-01-01', highRate=0, lowRate=0):
    """
    variables:
        currency - string containing currency name
        dataUpdate - date to identify row to update
        highRate - value of High rate to update
        lowRate - value of Low rate to update
    returns:
        execute query
        updates DB (one row of cryptoStats)
    """
    # ? connect to DB
    conn = sqlite3.connect('cryptoDB.db')

    # ? create cursor (tunnel to db) and execute the query
    c = conn.cursor()

    updateQuery = """
                  UPDATE cryptoStats SET High = {}, Low = {}
                  where Currency = '{}'
                    and Date = '{}';
                  """.format(highRate, lowRate, currency, dataUpdate)

    c.execute(updateQuery)
    conn.commit()
    conn.close()
