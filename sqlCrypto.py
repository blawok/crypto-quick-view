import sqlite3
import pandas as pd
from datetime import datetime

def executeSqlCrypto(varCurrency = 'LSK', varFromDate = '2018-07-13',
                     varToDate = '2018-08-1'):
    conn = sqlite3.connect('cryptoDB.db')

    # ? create cursor (tunnel to db)
    c = conn.cursor()

    # fromDate = datetime.strptime(varFromDate, '%d-%m-%Y').strftime('%Y-%m-%d')
    # toDate = datetime.strptime(varToDate, '%d-%m-%Y').strftime('%Y-%m-%d')

    query = """
            select *
            from cryptoStats
            where Currency = "{a}"
                and Date between "{b}" and "{c}";
            """.format(a = varCurrency,
                       b = varFromDate,
                       c = varToDate)

    df = pd.read_sql_query(query, conn)

    # ? execute the commend and iteterate through results using iterator
    # for row in c.execute('SELECT * FROM cryptoStats'):
    #     print(row)

    # c.execute("SELECT * FROM cryptoStats")

    # ? print results of execute
    # print(c.fetchone())
    # print(c.fetchall())

    # # ? get all results,assign them to the list,fecthall() returns empty list if no results
    # listOfResults=c.fetchall()
    # for item in listOfResults:
    #     print(item)

    conn.close()
    return df

# print(executeSqlCrypto())
