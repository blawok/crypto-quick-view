# cryptoQuickView
Python (Flask) university project of creating cryptocurrency dashboard web app.\
In which you can select a cryptocurrency and period of time, and it will show you a dashboard and some tables of that currency

## Installation

Clone repository to your desire directory (mine is /GIT/) and then

```bash
pip install -r requirements
```

## Usage

```bash
cd GIT/cryptoQuickView
```
```bash
flask run
```
open http://127.0.0.1:5000/.

You should see this now in your browser:

![forms](https://user-images.githubusercontent.com/41793223/51430743-ab98ea00-1c1f-11e9-8185-13068a66cc85.jpg)

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

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
