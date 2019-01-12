from app import app
from flask import render_template, Flask, Markup, flash, redirect, request
from flask_table import Table, Col

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

from scraper import cryptoInfoToDf
from sqlCrypto import executeSqlCrypto
from forms import LoginForm


@app.route('/')
@app.route('/form')
def print_form():
    return render_template('form.html')


@app.route("/cryptoSummary/")
@app.route("/cryptoSummary")
def summary():

    currency = request.args.get('currency')
    fromDate = request.args.get('fromDate')
    tillDate = request.args.get('tillDate')

    df = executeSqlCrypto()

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
