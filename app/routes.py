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

from scraper import cryptoInfoToDf
from sqlCrypto import executeSqlCrypto
from forms import InfoForm
from graphCreate import createBoxPlot


@app.route('/', methods=['GET', 'POST'])
@app.route('/forms', methods=['GET', 'POST'])
def submit():
    form = InfoForm()

    if form.validate_on_submit():
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
        currency = 'LSK'
        fromDate = '2018-07-15'
        tillDate = '2018-07-20'
        df = executeSqlCrypto(varCurrency = '{}'.format(currency),
                              varFromDate = '{}'.format(fromDate),
                              varToDate = '{}'.format(tillDate))

    img = io.BytesIO()
    sns.set(style="darkgrid")
    fig, ax =  plt.subplots(1,2, figsize=(11,6))
    sns.regplot(x=df["Market Cap"], y=df["Low"], ax=ax[0])
    sns.boxplot(x=df["Market Cap"], ax=ax[1])
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    img1 = io.BytesIO()
    sns.set(style="darkgrid")
    fig, ax =  plt.subplots(1, figsize=(11,6))
    sns.distplot(df['Market Cap'], color="m")
    fig.savefig(img1, format='png')
    img1.seek(0)
    plot_url1 = base64.b64encode(img1.getvalue()).decode()


    bar = createBoxPlot(df, 'Date', 'Market Cap', 'bar')
    scatter = createBoxPlot(df, 'Date', 'Market Cap', 'scatter')

    return render_template('cryptoSummary.html', currency=currency,
                           fromDate=fromDate, tillDate=tillDate, df=df,
                           plot_url=plot_url, plot_url1=plot_url1, bar=bar,
                           scatter=scatter)



@app.route('/cryptoCharts/')
@app.route('/cryptoCharts')
def charts():
    if ('currency' in session and 'fromDate' in session and
        'tillDate' in session):
        currency = session['currency']
        fromDate = session['fromDate']
        tillDate = session['tillDate']
        df = executeSqlCrypto(varCurrency = '{}'.format(currency),
                              varFromDate = '{}'.format(fromDate),
                              varToDate = '{}'.format(tillDate))
    else:
        currency = 'LSK'
        fromDate = '2018-07-15'
        tillDate = '2018-07-20'
        df = executeSqlCrypto(varCurrency = '{}'.format(currency),
                              varFromDate = '{}'.format(fromDate),
                              varToDate = '{}'.format(tillDate))
    # df = executeSqlCrypto()
    labels =  list(df["Date"])
    valuesLine = list(df["High"])
    valuesBar = list(df["Volume"])

    return render_template('cryptoCharts.html',
                           titleLine='Lisk Daily Price in USD',
                           titleBar='Lisk Daily Volume',
                           df=df, maxLine=50, maxBar=100000000,
                           labels=labels, valuesBar=valuesBar, valuesLine=valuesLine)



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
        currency = 'LSK'
        fromDate = '2018-07-15'
        tillDate = '2018-07-20'
        df = executeSqlCrypto(varCurrency = '{}'.format(currency),
                              varFromDate = '{}'.format(fromDate),
                              varToDate = '{}'.format(tillDate))
    return render_template('cryptoTables.html',
                           tables=df.to_html(classes=["table table-bordered table-hover"]))



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
