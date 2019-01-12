from app import app
from flask import render_template, Flask, Markup, flash, redirect, request
from flask_table import Table, Col
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

from scraper import cryptoInfoToDf
from sqlCrypto import executeSqlCrypto


class InfoForm(FlaskForm):
    currency = StringField("What currency?")
    fromDate = StringField("From when?")
    tillDate = StringField("Until when?")
    submit = SubmitField('Submit')

@app.route('/forms', methods=['GET','POST'])
def print_forms():
    currency = False
    fromDate = False
    tillDate = False

    form = InfoForm()

    if form.validate_on_submit():
        currency = form.currency.data
        form.currency.data = ''
        fromDate = form.fromDate.data
        form.fromDate.data = ''
        tillDate = form.tillDate.data
        form.tillDate.data = ''

    return render_template('forms.html', form=form, currency=currency,
                           fromDate=fromDate, tillDate=tillDate)


@app.route('/')
@app.route('/form')
def print_form():
    return render_template('form.html')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



@app.route("/cryptoSummary/")
@app.route("/cryptoSummary")
def summary():
    currency = request.args.get('currency')
    fromDate = request.args.get('fromDate')
    tillDate = request.args.get('tillDate')

    if currency != None and fromDate != None and tillDate != None:
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
    sns.regplot(x=df["Volume"], y=df["Market Cap"], ax=ax[0])
    sns.boxplot(x=df["Volume"], y= None, ax=ax[1])
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('cryptoSummary.html', currency=currency, fromDate=fromDate, tillDate=tillDate, df=df, plot_url=plot_url)



@app.route('/cryptoCharts/')
@app.route('/cryptoCharts')
def charts():

    df = executeSqlCrypto()
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
    df = executeSqlCrypto()
    return render_template('cryptoTables.html',
                           tables=df.to_html(classes=["table table-bordered table-hover"]))
