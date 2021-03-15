import secrets, os
from PIL import Image
from flask import render_template, flash, url_for, redirect, request
from TwojKomputerowiec import app, db, bcrypt
from TwojKomputerowiec.formularze import FormularzRejestracji, FormularzLogowania, FormularzAktualizacjiProfilu, FormularzNowegoPostu
from TwojKomputerowiec.modele import Uzytkownik, Post
from flask_login import login_user, current_user, logout_user, login_required


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

@app.route('/blogZawodowy')
@app.route('/itBlog')
def blogZawodowo():
    postyBazy = Post.query.all()
    return render_template('itBlog.html', posts=postyBazy)

@app.route('/blogPrywatnie')
@app.route('/privateBlog')
def blogPrywatnie():
    return render_template('prywatnyBlog.html')


@app.route('/rejestracja', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def rejestracja():
    if current_user.is_authenticated:
        return redirect(url_for('stronaStartowa'))
    formularz = FormularzRejestracji()
    if formularz.validate_on_submit():
        hash_haslo = bcrypt.generate_password_hash(formularz.haslo.data)
        uzytkownik = Uzytkownik(email=formularz.email.data, haslo=hash_haslo)
        db.session.add(uzytkownik)
        db.session.commit()
        flash(f'Konto utworzone dla { formularz.email.data }', 'success')
        return redirect(url_for('logowanie'))
    return render_template('rejestracja.html', title='Rejestracja', form=formularz)


@app.route('/logowanie', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def logowanie():
    if current_user.is_authenticated:
        return redirect(url_for('stronaStartowa'))
    formularz = FormularzLogowania()
    if formularz.validate_on_submit():
        uzytkownik = Uzytkownik.query.filter_by(email=formularz.email.data).first()
        if uzytkownik and bcrypt.check_password_hash(uzytkownik.haslo, formularz.haslo.data):
            login_user(uzytkownik, remember=formularz.potwierdzenie.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('stronaStartowa'))
        else:
            flash(f'nie zalogowano', 'danger')
    return render_template('logowanie.html', title='Logowanie', form=formularz)


@app.route('/wylogowanie')
@app.route('/logout')
def wylogowanie():
    logout_user()
    return redirect(url_for('stronaStartowa'))


def zachowajZdjecie(zdjecie):
    """
    Funkcja przyjmuje plik załadowany z formularza jako nowe zdjecie profilowe.
    Zapisuje go w katalogu ze zdjęciami profilowymi pod zmienioną nazwą i zwraca tą nazwę.

    :param zdjecie: plik, ktory zostal zaladowany przez formularz jako nowe zdjecie profilowe
    :return: nazwa zdjecia ktora zostaje zaladowana do folderu ze zdjeciami profilowymi
    """
    losowyHex = secrets.token_hex(8)
    _, rozszerzenie = os.path.splitext(zdjecie.filename)
    zdjecieNazwa = losowyHex + rozszerzenie
    sciezkaZdjecia = os.path.join(app.root_path, 'static/media/profil', zdjecieNazwa)

    rozmiar = (125, 125)
    zdjecieDoZapisu = Image.open(zdjecie)
    zdjecieDoZapisu.thumbnail(rozmiar)

    zdjecieDoZapisu.save(sciezkaZdjecia)
    return zdjecieNazwa


@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    formularz = FormularzAktualizacjiProfilu()
    if formularz.validate_on_submit():
        if formularz.zdjecie.data:
            plik_zdjecia = zachowajZdjecie(formularz.zdjecie.data)
            current_user.zdjecie = plik_zdjecia
        current_user.email = formularz.email.data
        db.session.commit()
        flash(f'Profil zaktualizowany', 'success')
        return redirect(url_for('profil'))
    elif request.method == 'GET':
        formularz.email.data = current_user.email
    zdjecie = url_for('static', filename='media/profil/' + current_user.zdjecie)
    return render_template('profil.html', title='Profil', zdjecie=zdjecie, form=formularz)


@app.route('/nowyPost', methods=['GET', 'POST'])
@app.route('/newPost', methods=['GET', 'POST'])
@login_required
def dodaniePosta():
    formularz = FormularzNowegoPostu()
    if formularz.validate_on_submit():
        post = Post(tytul=formularz.tytul.data, tresc=formularz.tresc.data, autor=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Post został dodany', 'success')
        return redirect(url_for('blogZawodowo'))
    return render_template('nowyPost.html', title='Nowy Post', form=formularz)