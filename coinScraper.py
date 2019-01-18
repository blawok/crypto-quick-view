from cmc import coinmarketcap
from datetime import datetime
import pandas as pd

def coinScraper(varCurrency = 'lisk', varFromDate = '2018-01-01',
                varToDate = '2018-12-31'):

    df = coinmarketcap.getDataFor(varCurrency, varFromDate, varToDate,
                                  fields = ['Open','High','Low','Close',
                                            'Volume','Market Cap'])

    df.reset_index(inplace=True, drop=False)
    df.columns = [''.join(col) for col in df.columns.values]
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap']

    return df

# print(coinScraper())
