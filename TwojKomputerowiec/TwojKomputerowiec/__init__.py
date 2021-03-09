from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='Szablony')
app.config['SECRET_KEY'] = '5f1d14fab76c410b921a0dca67965c60'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///strona.db'
db = SQLAlchemy(app)

from TwojKomputerowiec import strony