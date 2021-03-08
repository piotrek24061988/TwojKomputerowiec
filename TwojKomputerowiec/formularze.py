from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class FormularzRejestracji(FlaskForm):
    uzytkownik = StringField('Użytkownik', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    haslo = PasswordField('Hasło', validators=[DataRequired()])
    haslo2 = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('haslo')])
    potwierdzenie = SubmitField('Rejestracja')


class FormularzLogowania(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    haslo = PasswordField('Hasło', validators=[DataRequired()])
    zalogowany = BooleanField('Zapamiętaj mnie')
    potwierdzenie = SubmitField('Logowanie')