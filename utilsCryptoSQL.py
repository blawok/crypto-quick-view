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

# getFromDatabase('lisk', '2017-12-25', '2018-01-05', 'min')
