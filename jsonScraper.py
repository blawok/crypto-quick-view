from cryptocmd import CmcScraper
import pandas as pd
import json
import datetime

def cryptoInfoToDf (varCurrency = 'lisk', varFromDate = '2018-01-01',
                    varToDate = '2018-12-31'):
# def cryptoInfoToDf (varCurrency = 'lisk', varFromDate = '04-01-2017',
#                     varToDate = '16-01-2017'):
    """
    variables:
        varCurrency - string value of currency shortcut
        varFromDate - date in format of YYYY-MM-DD
        varToDate - date in format of YYYY-MM-DD

    returns:
        dataframe of cryptocurrency data
        created by connecting to Coinmarketcap.com
    """
    cryptoDict = {
                    'lisk': 'LSK',
                    'bitcoin': 'BTC',
                    'ripple': 'XRP',
                    'ethereum': 'ETH',
                    'litecoin': 'LTC'
    }

    cryptoName = cryptoDict[varCurrency]

    fromDate = datetime.datetime.strptime(varFromDate, '%Y-%m-%d').strftime('%d-%m-%Y')
    toDate = datetime.datetime.strptime(varToDate, '%Y-%m-%d').strftime('%d-%m-%Y')

    # cryptoDict = {
    #               'LSK':'lisk',
    #               'BTC':'bitcoin',
    #               'XRP':'ripple',
    #               'ETH':'ethereum',
    #               'LTC':'litecoin'
    #              }

    # ? initialise scraper
    scraper = CmcScraper(cryptoName, fromDate, toDate)

    # ? initialise dataframe for the data
    headers, data = scraper.get_data()
    df = pd.DataFrame(data, columns = headers)

    df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y")
    df['Currency'] = '{}'.format(varCurrency)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap', 'Currency']

    return df

# df = cryptoInfoToDf()
# # df = cryptoInfoToDf(varCurrency = 'LTC')
# print(df)

# # df = cryptoInfoToDf ("XRP", "05-10-2017", "15-10-2017")
# df = cryptoInfoToDf ("ripple", "2017-10-05", "2017-10-15")

# print(df)
