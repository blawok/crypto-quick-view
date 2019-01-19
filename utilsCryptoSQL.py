import sqlite3
import pandas as pd

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
