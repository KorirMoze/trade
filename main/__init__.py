from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'M'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
Api_key = '404b1595-9e73-4a5d-86ec-e837f2917b10'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
from main import routes
