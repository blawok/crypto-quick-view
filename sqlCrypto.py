import sqlite3
import pandas as pd

def executeSqlCrypto():
    conn = sqlite3.connect('cryptoDB.db')

    # ? create cursor - tunnel to db
    c = conn.cursor()

    df = pd.read_sql_query("select * from cryptoStats;", conn)
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

# executeSqlCrypto()