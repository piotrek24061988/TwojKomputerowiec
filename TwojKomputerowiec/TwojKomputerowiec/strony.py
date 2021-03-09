from flask import render_template, flash, url_for, redirect
from TwojKomputerowiec import app
from TwojKomputerowiec.formularze import FormularzRejestracji, FormularzLogowania
from TwojKomputerowiec.modele import Uzytkownik, Post


posty = [
    {
        'autor': 'Piotr Górecki',
        'tytul': 'Strona w przygotowaniu',
        'tresc': 'Trwa przygotowanie strony firmowej',
        'data': '05.03.2021'
    },
    {
        'autor': 'Piotr Górecki',
        'tytul': 'Firma w przygotowaniu',
        'tresc': 'Trwa przygotowanie koncecji firmy',
        'data': '05.03.2021'
    }
]

@app.route('/')
@app.route('/home')
@app.route('/dom')
def stronaStartowa():
    return render_template('domowa.html')


@app.route('/news')
@app.route('/aktualnosci')
def aktualnosci():
    return render_template('aktualnosci.html', posts=posty)


@app.route('/contact')
@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')


@app.route('/about')
@app.route('/oMnie')
def oMnie():
    return render_template('oMnie.html')

@app.route('/gallery')
@app.route('/galeria')
def galeria():
    return render_template('galeria.html')


@app.route('/rejestracja', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def rejestracja():
    formularz = FormularzRejestracji()
    if formularz.validate_on_submit():
        flash(f'Konto utworzone dla { formularz.email.data }', 'success')
        return redirect(url_for('stronaStartowa'))
    return render_template('rejestracja.html', title='Rejestracja', form=formularz)


@app.route('/logowanie', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def logowanie():
    formularz = FormularzLogowania()
    if formularz.validate_on_submit():
        if formularz.email.data == 'piotrek24061988@gmail.com':
            flash(f'zalogowano { formularz.email.data }', 'success')
            return redirect(url_for('stronaStartowa'))
        else:
            flash(f'nie zalogowano', 'danger')
    return render_template('logowanie.html', title='Logowanie', form=formularz)