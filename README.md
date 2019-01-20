![b8debf44-f85b-4642-9432-3efd80b7c367](https://user-images.githubusercontent.com/41793223/51441307-7ef0db00-1cd0-11e9-9263-c7c8d15d817d.png)

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com) 

# cryptoQuickView
Python (Flask) university project of creating cryptocurrency dashboard web app.\
The whole logic of this app is that you select (or use default values) a cryptocurrency and period of time, and it will show you a dashboard and some tables of that cryptocurrency.

## Installation

Clone repository (https://github.com/blawok/cryptoQuickView.git) to your desire directory (mine is GIT/) and then

```bash
cd GIT/cryptoQuickView
pip install -r requirements
```

## Usage

```bash
flask run
```
open http://127.0.0.1:5000/.

You should see this now in your browser:

![formsc](https://user-images.githubusercontent.com/41793223/51444189-cbe6a880-1cf4-11e9-859c-18fa3482a48e.PNG)

Now choose desired cryptocurrency from the list and type desired dates in YYYY-MM-DD format and click "Go".\
There are some default values if you don't know what to choose :)

## Summary page

Next page should look something like this:\
(scroll down for additional graphs or click the "View details" button to go to Tables page)

![summary](https://user-images.githubusercontent.com/41793223/51430799-6c1ecd80-1c20-11e9-80b1-e8edda7ce578.jpg)

On the panels in the head of the page you can see choosen cryptocurrency, maximum an minimum of currency rate from chosen period.
First graph is a Plotly (so you can play with it) graph showing open and close rates for given period. Second graph shows volume values and the third one market capitalization of a currency.
The last one shows distribution of market capitalization for a given period.

## Tables page

After clicking on the "View details" button or choosing "Tables" from the list on the left side, 
you should be redirected to Tables page where you can browse data from the Database:

![tables](https://user-images.githubusercontent.com/41793223/51430857-1e569500-1c21-11e9-8a06-bce71b7064a7.jpg)

First table shows grouped data for all currencies and all time from the Database.
Second one (on the right) is a table of grouped by month and year data for chosen currency (all time).
The last one is a huge table of all values from the Database for chosen currency and period.

## Update page

If you click on the _Update_ object on the left you should see:

![updateform](https://user-images.githubusercontent.com/41793223/51444196-02bcbe80-1cf5-11e9-97da-f69d50a9d3aa.PNG)

If your imagination goes beyond normal human being one then you can update any row you want in the _cryptoStats_ table :)
## Database overview

Sqlite3 database is being used in this project and structure of this database is quite straightforward.

![erdiagram](https://user-images.githubusercontent.com/41793223/51440405-fd487f80-1cc6-11e9-93fa-9327bdf104e8.jpg)

The main table that the whole app depends on is _cryptoStats_. Data in that table is inserted by using scraper https://github.com/Alescontrela/coinmarketcap-history which uses https://coinmarketcap.com/ API. This table's content covers all basic daily information about cryptocurrencies. _Index_ is its primary key, but its foreign keys are _Date_ and _Currency_ which correspond to two following tables. The database update process requires existence of two additional tables: _cryptoStatsUser_ which is basically a copy of _cryptoStats_ but has only data that was searched by user but was not in the Database, second table _cryptoStatsTemp_ is a temporary table that is only created if user's query required data that was not in the Database (its whole content is inserted into _cryptoStats_, I showed it here only for the overview of the structure). The last table in the Database is _cryptoDict_ that is kind of a dictionary which keys are cryptocurrencies names and items are their's shortcuts (which by many people are considered real names).

## Functions overview

Each function that is used in the app (except of the ones in _routes.py_) has its own docstring, like the one below:

![docstring](https://user-images.githubusercontent.com/41793223/51441083-2e787e00-1cce-11e9-8771-8c621e846bab.PNG)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
