from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, URL, Optional
from TwojKomputerowiec.modele import Uzytkownik


class FormularzRejestracji(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    haslo = PasswordField('Hasło', validators=[DataRequired()])
    haslo2 = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('haslo')])
    potwierdzenie = SubmitField('Rejestracja')

    def validate_email(self, email):
        uzytkownik = Uzytkownik.query.filter_by(email=email.data).first()
        if uzytkownik:
            raise ValidationError('Użytkownik już istnieje')


class FormularzLogowania(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    haslo = PasswordField('Hasło', validators=[DataRequired()])
    zalogowany = BooleanField('Zapamiętaj mnie')
    potwierdzenie = SubmitField('Logowanie')


class FormularzAktualizacjiProfilu(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    zdjecie = FileField('Zaktualizuj zdjęcie profilowe', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    potwierdzenie = SubmitField('Aktualizacja')

    def validate_email(self, email):
        if email.data != current_user.email:
            uzytkownik = Uzytkownik.query.filter_by(email=email.data).first()
            if uzytkownik:
                raise ValidationError('Użytkownik już istnieje')


class FormularzNowegoPostu(FlaskForm):
    tytul = StringField('Tytuł', validators=[DataRequired()])
    tresc = TextAreaField('Treść', validators=[DataRequired()])
    potwierdzenie = SubmitField('Dodaj post')


class FormularzResetuHasla(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    potwierdzenie = SubmitField('Wyślij email')

    def validate_email(self, email):
        uzytkownik = Uzytkownik.query.filter_by(email=email.data).first()
        if uzytkownik is None:
            raise ValidationError('Użytkownik nie istnieje, zarejestruj się')


class FormularzResetuHasla2(FlaskForm):
    haslo = PasswordField('Hasło', validators=[DataRequired()])
    haslo2 = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('haslo')])
    potwierdzenie = SubmitField('Zmień hasło')


class FormularzKontaktowy(FlaskForm):
    kontakt = StringField('Twoje dane kontaktowe', validators=[DataRequired()])
    temat = StringField('Tytuł', validators=[DataRequired()])
    tresc = TextAreaField('Treść', validators=[DataRequired()])
    potwierdzenie = SubmitField('Napisz')


class FormularzNowejAktualnosci(FlaskForm):
    tytul = StringField('Tytuł', validators=[DataRequired()])
    tresc = TextAreaField('Treść', validators=[DataRequired()])
    zdjecie = FileField('Dodaj zdjęcie do aktualności', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    videoUrl = StringField('Video URL:', validators=[Optional(), URL()])
    potwierdzenie = SubmitField('Dodaj informacje')