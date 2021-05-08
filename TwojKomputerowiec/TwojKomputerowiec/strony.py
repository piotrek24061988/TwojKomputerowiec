from flask import render_template, flash, url_for, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from TwojKomputerowiec import app, db, bcrypt
from TwojKomputerowiec.formularze import *
from TwojKomputerowiec.modele import *
from TwojKomputerowiec.przydatne import *
from TwojKomputerowiec.konfiguracja import Konfiguracja


@app.route('/')
@app.route('/home')
@app.route('/dom')
def stronaStartowa():
    return render_template('domowa.html')


@app.route('/news')
@app.route('/aktualnosci')
def aktualnosci():
    strona = request.args.get('page', 1, type=int)
    postyAktualnosci = Aktualnosc.query.order_by(Aktualnosc.data.desc()).paginate(page=strona, per_page=10)
    return render_template('aktualnosci.html', aktualnosci=postyAktualnosci, admin=Konfiguracja.MAIL_USERNAME)


@app.route('/nowaAktualnosc', methods=['GET', 'POST'])
@app.route('/addNews', methods=['GET', 'POST'])
@login_required
def dodanieAktualnosci():
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    formularz = FormularzNowejAktualnosci()
    if formularz.validate_on_submit():
        plik_zdjecia = None
        if formularz.zdjecie.data:
            plik_zdjecia = zachowajZdjecie(formularz.zdjecie.data, sciezka=Konfiguracja.PATH_NEWS)
        aktualnosc = Aktualnosc(tytul=formularz.tytul.data, tresc=formularz.tresc.data, zdjecie=plik_zdjecia, videoUrl=formularz.videoUrl.data)
        db.session.add(aktualnosc)
        db.session.commit()
        flash(f'Aktualizacja został dodany', 'success')
        return redirect(url_for('aktualnosci'))
    return render_template('nowaAktualnosc.html', title='Aktualizacja', form=formularz)


@app.route('/aktualnosc/<int:aktualnosc_id>')
@app.route('/news/<int:aktualnosc_id>')
def aktualnosc(aktualnosc_id):
    aktualnosc = Aktualnosc.query.get_or_404(aktualnosc_id)
    return render_template('aktualnosc.html', title=aktualnosc.tytul, aktualnosc=aktualnosc, admin=Konfiguracja.MAIL_USERNAME)


@app.route('/usunAktualnosc/<int:aktualnosc_id>', methods=['GET','POST'])
@app.route('/deleteNews/<int:aktualnosc_id>', methods=['GET', 'POST'])
@login_required
def usunAktualnosc(aktualnosc_id):
    aktualnosc = Aktualnosc.query.get_or_404(aktualnosc_id)
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    db.session.delete(aktualnosc)
    db.session.commit()
    flash(f'Aktualność została usunięta', 'success')
    return redirect(url_for('aktualnosci'))


@app.route('/aktualizujAktualnosc/<int:aktualnosc_id>', methods=['GET', 'POST'])
@app.route('/updateNews/<int:aktualnosc_id>', methods=['GET', 'POST'])
@login_required
def aktualizujAktualnosc(aktualnosc_id):
    aktualnosc = Aktualnosc.query.get_or_404(aktualnosc_id)
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    formularz = FormularzNowejAktualnosci()
    if formularz.validate_on_submit():
        aktualnosc.tytul = formularz.tytul.data
        aktualnosc.tresc = formularz.tresc.data
        if formularz.zdjecie.data:
            aktualnosc.zdjecie = zachowajZdjecie(formularz.zdjecie.data, sciezka=Konfiguracja.PATH_NEWS)
        if formularz.videoUrl.data:
            aktualnosc.videoUrl = formularz.videoUrl.data
        db.session.commit()
        flash(f'Aktualność została zaktualizowany', 'success')
        return redirect(url_for('aktualnosci'))
    elif request.method == 'GET':
        formularz.tytul.data = aktualnosc.tytul
        formularz.tresc.data = aktualnosc.tresc
        formularz.zdjecie.data = aktualnosc.zdjecie
        formularz.videoUrl.data = aktualnosc.videoUrl
    return render_template('nowaAktualnosc.html', title='Aktualizuj', form=formularz)


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
    strona = request.args.get('page', 1, type=int)
    galeria = Galeria.query.order_by(Galeria.data.desc()).paginate(page=strona, per_page=20)
    return render_template('galeria.html', galeria=galeria, admin=Konfiguracja.MAIL_USERNAME)


@app.route('/noweZdjecie', methods=['GET', 'POST'])
@app.route('/addPhoto', methods=['GET', 'POST'])
@login_required
def dodanieZdjecia():
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    formularz = FormularzNowegoZdjecia()
    if formularz.validate_on_submit():
        plik_zdjecia = None
        if formularz.zdjecie.data:
            plik_zdjecia = zachowajZdjecie(formularz.zdjecie.data, sciezka=Konfiguracja.PATH_GALLERY)
        zdjecie = Galeria(tytul=formularz.tytul.data, zdjecie=plik_zdjecia)
        db.session.add(zdjecie)
        db.session.commit()
        flash(f'Zdjęcie zostało dodane', 'success')
        return redirect(url_for('galeria'))
    return render_template('noweZdjecie.html', title='NoweZdjecie', form=formularz)


@app.route('/zdjecie/<int:zdjecie_id>')
@app.route('/photo/<int:zdjecie_id>')
def zdjecie(zdjecie_id):
    zdjecie = Galeria.query.get_or_404(zdjecie_id)
    return render_template('zdjecie.html', title=zdjecie.tytul, zdjecie=zdjecie, admin=Konfiguracja.MAIL_USERNAME)


@app.route('/usunZdjecie/<int:zdjecie_id>', methods=['GET','POST'])
@app.route('/deletePhoto/<int:zdjecie_id>', methods=['GET', 'POST'])
@login_required
def usunZdjecie(zdjecie_id):
    zdjecie = Galeria.query.get_or_404(zdjecie_id)
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    db.session.delete(zdjecie)
    db.session.commit()
    flash(f'Zdjęcie zostało usunięte', 'success')
    return redirect(url_for('galeria'))


@app.route('/aktualizujZdjecie/<int:zdjecie_id>', methods=['GET', 'POST'])
@app.route('/updatePhoto/<int:zdjecie_id>', methods=['GET', 'POST'])
@login_required
def aktualizujZdjecie(zdjecie_id):
    zdjecie = Galeria.query.get_or_404(zdjecie_id)
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    formularz = FormularzAktualizacjiZdjecia()
    if formularz.validate_on_submit():
        zdjecie.tytul = formularz.tytul.data
        if formularz.zdjecie.data:
            zdjecie.zdjecie = zachowajZdjecie(formularz.zdjecie.data, sciezka=Konfiguracja.PATH_GALLERY)
        db.session.commit()
        flash(f'Zdjęcie zostało zaktualizowane', 'success')
        return redirect(url_for('galeria'))
    elif request.method == 'GET':
        formularz.tytul.data = zdjecie.tytul
        formularz.zdjecie.data = zdjecie.zdjecie
    return render_template('noweZdjecie.html', title='Aktualizuj', form=formularz)


"""
Stub produktu sklepowego
"""
class Produkt():
    def __init__(self, nazwa, zdjecie, id):
        self.nazwa = nazwa
        self.zdjecie = zdjecie
        self.id = id


@app.route('/shop')
@app.route('/sklep')
def sklep():
    strona = request.args.get('page', 1, type=int)
    #galeria = Galeria.query.order_by(Galeria.data.desc()).paginate(page=strona, per_page=20)
    #sklep = Sklep.query.order_by(Sklep.data.desc()).paginate(page=strona, per_page=20)
    sklep = {Produkt(nazwa="produkt testowy 1", zdjecie="placeholder.png", id=1), Produkt(nazwa="produkt testowy 2", zdjecie="placeholder.png", id=2)}
    return render_template('sklep.html', sklep=sklep, admin=Konfiguracja.MAIL_USERNAME)


@app.route('/produkt/<int:produkt_id>')
@app.route('/product/<int:produkt_id>')
def produkt(produkt_id):
    #zdjecie = Galeria.query.get_or_404(zdjecie_id)
    #produkt = Sklep.query.get_or_404(produkt_id)
    produkt = Produkt("produkt testowy 1", "placeholder.png", 1)
    return render_template('produkt.html', produkt=produkt, admin=Konfiguracja.MAIL_USERNAME)


@app.route('/karta')
@app.route('/card')
def karta():
    return render_template('karta.html')


@app.route('/zamowienie')
@app.route('/order')
def zamowienie():
    return render_template('zamowienie.html')


@app.route('/nowyProdukt', methods=['GET', 'POST'])
@app.route('/newProduct', methods=['GET', 'POST'])
@login_required
def dodanieProduktu():
    return render_template('nowyProdukt.html')

@app.route('/usunProdukt/<int:produkt_id>', methods=['GET','POST'])
@app.route('/deleteProduct/<int:produkt_id>', methods=['GET', 'POST'])
@login_required
def usunProdukt(produkt_id):
    #zdjecie = Galeria.query.get_or_404(zdjecie_id)
    #produkt = Sklep.query.get_or_404(produkt_id)
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    #db.session.delete(produkt)
    #db.session.commit()
    flash(f'Produkt został usunięty', 'success')
    return redirect(url_for('sklep'))


@app.route('/aktualizujProdukt/<int:produkt_id>', methods=['GET', 'POST'])
@app.route('/updateProduct/<int:produkt_id>', methods=['GET', 'POST'])
@login_required
def aktualizujProdukt(produkt_id):
    #zdjecie = Galeria.query.get_or_404(zdjecie_id)
    #produkt = Sklep.query.get_or_404(produkt_id)
    produkt = Produkt("produkt testowy 1", "placeholder.png", 1)
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    #formularz = FormularzAktualizacjiProduktu()
    #if formularz.validate_on_submit():
    #    produkt.nazwa = produkt.nazwa.data
    #    if formularz.produkt.data:
    #        produkt.zdjecie = zachowajZdjecie(formularz.produkt.data, sciezka=Konfiguracja.PATH_SHOP)
    #    db.session.commit()
    #    flash(f'Produkt został zaktualizowany', 'success')
    #    return redirect(url_for('sklep'))
    #elif request.method == 'GET':
    #    formularz.nazwa.data = produkt.nazwa
    #    formularz.zdjecie.data = produkt.zdjecie
    formularz = {}
    return render_template('nowyProdukt.html', title='Aktualizuj', form=formularz)


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
            current_user.zdjecie = zachowajZdjecie(formularz.zdjecie.data, resize=True, sciezka=Konfiguracja.PATH_PROFILE)
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
    return render_template('post.html', title=post.tytul, post=post, admin=Konfiguracja.MAIL_USERNAME)


@app.route('/aktualizujPost/<int:post_id>', methods=['GET', 'POST'])
@app.route('/updatePost/<int:post_id>', methods=['GET', 'POST'])
@login_required
def aktualizujPost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.autor == current_user or (current_user.is_authenticated and current_user.email == Konfiguracja.MAIL_USERNAME):
        pass
    else:
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
    if post.autor == current_user or (current_user.is_authenticated and current_user.email == Konfiguracja.MAIL_USERNAME):
        pass
    else:
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


@app.route('/testowa')
@app.route('/test')
def testowa():
    return render_template('testowa.html')


@app.errorhandler(404)
def blad_404(error):
    return render_template('blad404.html'), 404


@app.errorhandler(403)
def blad_403(error):
    return render_template('blad403.html'), 403


@app.errorhandler(500)
def blad_500(error):
    return render_template('blad500.html'), 500