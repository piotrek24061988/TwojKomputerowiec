from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restful import Api
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from TwojKomputerowiec.konfiguracja import Konfiguracja
import os
CLOUDINARY_URL = "cloudinary://" + Konfiguracja.STORAGE_KEY + ":" + Konfiguracja.STORAGE_SEC + "@" + Konfiguracja.STORAGE_NAME
if Konfiguracja.STORAGE_PROXY:
    CLOUDINARY_URL = CLOUDINARY_URL + "?api_proxy=" + Konfiguracja.STORAGE_PROXY

os.environ["CLOUDINARY_URL"] = CLOUDINARY_URL


app = Flask(__name__, template_folder=Konfiguracja.TEMPLATE_FOLDER)
app.config.from_object(Konfiguracja)

loginManager = LoginManager(app)
loginManager.login_view = Konfiguracja.LOGIN_PATH
loginManager.login_message_category = 'danger'
loginManager.login_message = Konfiguracja.LOGIN_MSG

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
mail = Mail(app)
api = Api(app)
admin = Admin(app, name='', index_view=AdminIndexView(name='Admin'))


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and Konfiguracja.MAIL_USERNAME == current_user.email

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('logowanie'))

import cloudinary
if Konfiguracja.STORAGE_PROXY:
    cloudinary.config(cloud_name=Konfiguracja.STORAGE_NAME, api_key=Konfiguracja.STORAGE_KEY, api_secret=Konfiguracja.STORAGE_SEC, api_proxy=Konfiguracja.STORAGE_PROXY)
else:
    cloudinary.config(cloud_name=Konfiguracja.STORAGE_NAME, api_key=Konfiguracja.STORAGE_KEY, api_secret=Konfiguracja.STORAGE_SEC)
from TwojKomputerowiec import strony, restApi