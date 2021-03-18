from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__, template_folder='Szablony')
app.config['SECRET_KEY'] = '5f1d14fab76c410b921a0dca67965c60'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///strona.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'piotrek24061988@gmail.com'
app.config['MAIL_PASSWORD'] = 'dajffmmwfatdotkc'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'logowanie'
loginManager.login_message_category = 'info'
loginManager.login_message = 'Zaloguj się aby uzyskać dostęp'
mail = Mail(app)

from TwojKomputerowiec import strony