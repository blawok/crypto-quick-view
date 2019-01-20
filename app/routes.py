from app import app
from flask import (render_template, Flask, Markup, flash, redirect, request,
                   session, redirect, url_for)
from flask_table import Table, Col
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import plotly
import plotly.graph_objs as go
import json
import sqlite3

from utilsSQL import (executeSqlCrypto, appendIfNotExist, getFromDatabase,
                      getGroupedData, getCurrencyNames, updateDataBase)
from coinScraper import coinScraper
from forms import InfoForm
from graphCreate import createPlot, createPlotMultiple



@app.route('/', methods=['GET', 'POST'])
@app.route('/forms/', methods=['GET', 'POST'])
@app.route('/forms', methods=['GET', 'POST'])
def submit():
    form = InfoForm()

    if form.validate_on_submit():
        appendIfNotExist(form.currency.data, form.fromDate.data, form.tillDate.data)

        session['currency'] = form.currency.data
        session['fromDate'] = form.fromDate.data
        session['tillDate'] = form.tillDate.data

        return redirect(url_for('summary'))

    return render_template('forms.html', form=form)



@app.route("/cryptoSummary/")
@app.route("/cryptoSummary")
def summary():
    if ('currency' in session and 'fromDate' in session and
        'tillDate' in session):
        currency = session['currency']
        fromDate = session['fromDate']
        tillDate = session['tillDate']
        df = executeSqlCrypto(varCurrency = '{}'.format(currency),
                              varFromDate = '{}'.format(fromDate),
                              varToDate = '{}'.format(tillDate))
    else:
        currency = 'lisk'
        fromDate = '2018-07-15'
        tillDate = '2018-07-20'
        df = executeSqlCrypto(varCurrency = '{}'.format(currency),
                              varFromDate = '{}'.format(fromDate),
                              varToDate = '{}'.format(tillDate))

    maxHigh = getFromDatabase(currency,fromDate,tillDate,'max')
    minLow = getFromDatabase(currency,fromDate,tillDate,'min')
    shortcut = getCurrencyNames(currency)

    img = io.BytesIO()
    sns.set(style="darkgrid")
    fig, ax =  plt.subplots(1, figsize=(11,6))
    sns.distplot(df['Market Cap'], color="m")
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    bar = createPlot(df, 'Date', 'Volume', 'bar')
    scatter = createPlot(df, 'Date', 'Market Cap', 'scatter')
    scatter2 = createPlot(df, 'Date', 'Close', 'scatter')
    scatterMulti = createPlotMultiple(df, 'Date', 'Open', 'Close', 'scatter')

    return render_template('cryptoSummary.html', currency=currency,
                           fromDate=fromDate, tillDate=tillDate, df=df,
                           plot_url=plot_url, bar=bar, scatter=scatter,
                           scatter2=scatter2, maxHigh=maxHigh, minLow=minLow,
                           scatterMulti=scatterMulti, shortcut=shortcut)



@app.route("/cryptoTables/")
@app.route("/cryptoTables")
def tables():
    if ('currency' in session and 'fromDate' in session and
        'tillDate' in session):
        currency = session['currency']
        fromDate = session['fromDate']
        tillDate = session['tillDate']
        df = executeSqlCrypto(varCurrency = '{}'.format(currency),
                              varFromDate = '{}'.format(fromDate),
                              varToDate = '{}'.format(tillDate))
    else:
        currency = 'lisk'
        fromDate = '2018-07-15'
        tillDate = '2018-07-20'
        df = executeSqlCrypto(varCurrency = '{}'.format(currency),
                              varFromDate = '{}'.format(fromDate),
                              varToDate = '{}'.format(tillDate))

    dfGrouped = getGroupedData()
    dfMonthData = getFromDatabase(currency,fromDate,tillDate,'monthData')
    return render_template('cryptoTables.html',
                           tables=df.loc[:, 'Date':].to_html(classes=["table table-bordered table-hover"]),
                           tableGrouped = dfGrouped.to_html(classes=["table table-bordered table-hover"]),
                           tableMonth = dfMonthData.to_html(classes=["table table-bordered table-hover"]))



@app.route('/updateDB/', methods=['GET', 'POST'])
@app.route('/updateDB', methods=['GET', 'POST'])
def submitUpdate():
    form = InfoForm()
    updateDataBase(form.currencyUpdate.data,
                   form.dateUpdate.data,
                   form.highUpdate.data,
                   form.lowUpdate.data)

    return render_template('updateDB.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
