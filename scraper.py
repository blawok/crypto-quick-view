from cryptocmd import CmcScraper
import pandas as pd
# from utilsSQL import getCurrencyNames2

def cryptoInfoToDf (varCurrency = 'LSK', varFromDate = '13-02-2018',
                    varToDate = '1-03-2018'):

    """
    variables:
        varCurrency - string value of currency shortcut
        varFromDate - date in format of YYYY-MM-DD
        varToDate - date in format of YYYY-MM-DD

    returns:
        dataframe of cryptocurrency data
        created by connecting to Coinmarketcap.com
    """
    # ? initialise scraper
    scraper = CmcScraper('{}'.format(varCurrency),
                         '{}'.format(varFromDate), '{}'.format(varToDate))

    # ? initialise dataframe for the data
    df = scraper.get_dataframe()
    cryptoDict = {'LSK':'lisk',
                  'BTC':'bitcoin',
                  'XRP':'ripple',
                  'ETH':'ethereum',
                  'LTC':'litecoin'
    }
    df['Currency'] = cryptoDict[varCurrency]
    return df

# cryptoInfoToDf()
# df = cryptoInfoToDf(varCurrency = 'LTC')
# print(df)
