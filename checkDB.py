import sqlite3
from datetime import datetime
from insertCrypto import insertCrypto

def checkIfExists(currency, fromDate, tillDate):

    def days_between(d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)

    query = """
            select
            count(distinct Date)
            from cryptoStats
            where Currency = '{0}'
                and Date between '{1}' and '{2}'
            """.format(currency, fromDate, tillDate)

    # ? connect to DB
    conn = sqlite3.connect('cryptoDB.db')

    # ? create cursor (tunnel to db)
    c = conn.cursor()

    c.execute(query)
    numberOfDistinctDates = int(c.fetchone()[0])
    numberOfDays = days_between(tillDate, fromDate) + 1
    print(numberOfDays == numberOfDistinctDates)
    if (numberOfDays != numberOfDistinctDates):
        # insertCrypto(currency, fromDate, tillDate)

    """
    df = (select * from DB)
    dfTemp = df(interval with missing values)
    query = (select dfTemp.*
             from DB
             right join dfTemp
                on (DB.Currency = dfTemp.Currency and DB.Date = dfTemp.Date)
             where DB.Currency is null;
    """

checkIfExists('lisk', '2018-01-01', '2018-01-10')
