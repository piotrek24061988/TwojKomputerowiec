from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from TwojKomputerowiec.konfiguracja import Konfiguracja

app = Flask(__name__, template_folder=Konfiguracja.TEMPLATE_FOLDER)
app.config.from_object(Konfiguracja)

loginManager = LoginManager(app)
loginManager.login_view = Konfiguracja.LOGIN_PATH
loginManager.login_message_category = 'info'
loginManager.login_message = Konfiguracja.LOGIN_MSG

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

from TwojKomputerowiec import strony