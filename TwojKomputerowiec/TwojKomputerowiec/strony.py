from flask import render_template, flash, url_for, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from TwojKomputerowiec import app, db, bcrypt
from TwojKomputerowiec.formularze import FormularzRejestracji, FormularzLogowania, FormularzAktualizacjiProfilu, \
                                         FormularzNowegoPostu, FormularzResetuHasla, FormularzResetuHasla2, \
                                         FormularzKontaktowy
from TwojKomputerowiec.modele import Uzytkownik, Post
from TwojKomputerowiec.przydatne import zachowajZdjecie, emailResetuHasla, emailKontaktowy


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


@app.route('/contact', methods=['GET', 'POST'])
@app.route('/kontakt', methods=['GET', 'POST'])
def kontakt():
    formularz = FormularzKontaktowy()
    if formularz.validate_on_submit():
        emailKontaktowy(kontakt=formularz.kontakt.data, temat=formularz.temat.data, tresc=formularz.tresc.data)
        flash(f'Wiadomość wysłana', 'success')
        return redirect(url_for('stronaStartowa'))
    return render_template('kontakt.html', form=formularz)


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
    strona = request.args.get('page', 1, type=int)
    postyBloga = Post.query.order_by(Post.data.desc()).paginate(page=strona, per_page=10)
    return render_template('itBlog.html', posts=postyBloga)


@app.route('/blogPrywatnie/<string:uzytkownik>')
@app.route('/privateBlog/<string:uzytkownik>')
def blogPrywatnie(uzytkownik):
    strona = request.args.get('page', 1, type=int)
    tworcaPosta = Uzytkownik.query.filter_by(email=uzytkownik).first_or_404()
    postyBloga = Post.query.filter_by(autor=tworcaPosta).order_by(Post.data.desc()).paginate(page=strona, per_page=10)
    return render_template('prywatnyBlog.html', posts=postyBloga, uzytkownik=tworcaPosta)


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


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.tytul, post=post)


@app.route('/aktualizujPost/<int:post_id>', methods=['GET', 'POST'])
@app.route('/updatePost/<int:post_id>', methods=['GET', 'POST'])
@login_required
def aktualizujPost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.autor != current_user:
        abort(403)
    formularz = FormularzNowegoPostu()
    if formularz.validate_on_submit():
        post.tytul = formularz.tytul.data
        post.tresc = formularz.tresc.data
        db.session.commit()
        flash(f'Post został zaktualizowany', 'success')
        return redirect(url_for('blogZawodowo'))
    elif request.method == 'GET':
        formularz.tytul.data = post.tytul
        formularz.tresc.data = post.tresc
    return render_template('nowyPost.html', title='Aktualizuj Post', form=formularz)


@app.route('/usunPost/<int:post_id>', methods=['GET','POST'])
@app.route('/deletePost/<int:post_id>', methods=['GET', 'POST'])
@login_required
def usunPost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.autor != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post został usunięty', 'success')
    return redirect(url_for('blogZawodowo'))


@app.route('/resetujHaslo', methods=['GET', 'POST'])
@app.route('/passwordReset', methods=['GET', 'POST'])
def wnioskujResetHasla():
    if current_user.is_authenticated:
        return redirect(url_for('stronaStartowa'))
    formularz = FormularzResetuHasla()
    if formularz.validate_on_submit():
        uzytkownik = Uzytkownik.query.filter_by(email=formularz.email.data).first()
        emailResetuHasla(uzytkownik=uzytkownik)
        flash(f'Email z instrukcją resetu hasła wysłany', 'success')
        return redirect(url_for('logowanie'))
    return render_template('wniosekResetuHasla.html', title='Zresetuj Haslo', form=formularz)


@app.route('/noweHaslo/<token>', methods=['GET', 'POST'])
@app.route('/newPassword/<token>', methods=['GET', 'POST'])
def noweHaslo(token):
    if current_user.is_authenticated:
        return redirect(url_for('stronaStartowa'))
    uzytkownik = Uzytkownik.weryfikuj_token(token)
    if uzytkownik is None:
        flash(f'Nieprawidłowy token', 'danger')
        return redirect(url_for('wnioskujResetHasla'))
    formularz = FormularzResetuHasla2()
    if formularz.validate_on_submit():
        hash_haslo = bcrypt.generate_password_hash(formularz.haslo.data)
        uzytkownik.haslo = hash_haslo
        db.session.commit()
        flash(f'Hasło zmienione', 'success')
        return redirect(url_for('logowanie'))
    return render_template('utworzenieNowegoHasla.html', title='Utwórz nowe hasło', form=formularz)


@app.errorhandler(404)
def blad_404(error):
    return render_template('blad404.html'), 404


@app.errorhandler(403)
def blad_403(error):
    return render_template('blad403.html'), 403


@app.errorhandler(500)
def blad_500(error):
    return render_template('blad500.html'), 500