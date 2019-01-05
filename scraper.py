from cryptocmd import CmcScraper
import pandas as pd

def cryptoInfoToDf (varCurrency = 'LSK', varFromDate = '13-02-2018',
                    varToDate = '1-03-2018'):

    # ? initialise scraper
    scraper = CmcScraper('{}'.format(varCurrency),
                         '{}'.format(varFromDate), '{}'.format(varToDate))

    # ? initialise dataframe for the data
    df = scraper.get_dataframe()
    return df

# cryptoInfoToDf()
# df = cryptoInfoToDf(varCurrency = 'LTC')
# print(df)
