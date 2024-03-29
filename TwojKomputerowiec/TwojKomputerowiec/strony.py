from flask import render_template, flash, url_for, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from TwojKomputerowiec import app, db, bcrypt, imagekit
from TwojKomputerowiec.formularze import *
from TwojKomputerowiec.modele import *
from TwojKomputerowiec.przydatne import *
from TwojKomputerowiec.konfiguracja import Konfiguracja
import string, random
import cloudinary, cloudinary.uploader, cloudinary.api


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
    return render_template('nowaAktualnosc.html', title='Dodanie aktualności', form=formularz)


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
    return render_template('noweZdjecie.html', title='Nowe zdjecie', form=formularz)


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


@app.route('/shop')
@app.route('/sklep')
def sklep():
    strona = request.args.get('page', 1, type=int)
    sklep = Produkt.query.order_by(Produkt.data.desc()).paginate(page=strona, per_page=10)
    zamowienie = {'iloscProduktow': 0, 'lacznaCena': 0, 'obiektZamowienia': []}
    #obsluga zalogowanego uzytkownika
    if current_user.is_authenticated:
        uzytkownik = Uzytkownik.query.filter_by(email=current_user.email).first()
        if uzytkownik:
            for zamowienieUzytkownika in uzytkownik.zamowienia:
                if zamowienieUzytkownika.ukonczone == False:
                    zamowienie = zamowienieUzytkownika
    #obsluga niezalogowanego uzytkownika za pomoca ciasteczek
    else:
        zamowienie = przetworzCiasteczkaZamowienia(request)
    return render_template('sklep.html', sklep=sklep, admin=Konfiguracja.MAIL_USERNAME, zamowienie=zamowienie)


@app.route('/produkt/<int:produkt_id>')
@app.route('/product/<int:produkt_id>')
def produkt(produkt_id):
    produkt = Produkt.query.get_or_404(produkt_id)
    opis = "to jest testowy opis produtu sporządzony dla celów testowych tego co znajduje się w sklepie, " \
           "który docelowo zostanie zamieniony na pełnowartościowy opis produktu sklepowego"
    return render_template('produkt.html', produkt=produkt, admin=Konfiguracja.MAIL_USERNAME)


@app.route('/dodajDoKosza/<int:produkt_id>', methods=['GET', 'POST'])
@app.route('/addToBin/<int:produkt_id>', methods=['GET', 'POST'])
def dodajDoKosza(produkt_id):
    if current_user.is_authenticated:
        uzytkownik = Uzytkownik.query.filter_by(email=current_user.email).first()
        if uzytkownik:
            zamowienie = get_or_create(session=db.session, model=Zamowienie, uzytkownik_id=uzytkownik.id, ukonczone=False)
            obiektZamowienia = get_or_create(session=db.session, model=ObiektZamowienia, zamowienie_id=zamowienie.id, produkt_id=produkt_id)
            produkt = get_or_create(session=db.session, model=Produkt, id=produkt_id)
            if not obiektZamowienia.ilosc:
                obiektZamowienia.ilosc = 0
            if produkt.ilosc != 0:
                obiektZamowienia.ilosc = obiektZamowienia.ilosc + 1
                produkt.ilosc = produkt.ilosc - 1
                db.session.commit()
                flash(f'Produkt został dodany', 'success')
            else:
                flash(f'Produkt nie został dodany - brak w magazynie', 'danger')
        else:
            flash(f'Produkt nie został dodany - problem z kontem użytkownika', 'danger')
    else:
        print('Produkt nie został dodany - zaloguj się')
    return redirect(url_for('sklep'))


@app.route('/zwiekszKosz/<int:produkt_id>', methods=['GET', 'POST'])
@app.route('/binIncrement/<int:produkt_id>', methods=['GET', 'POST'])
def zwiekszKosz(produkt_id):
    if current_user.is_authenticated:
        uzytkownik = Uzytkownik.query.filter_by(email=current_user.email).first()
        if uzytkownik:
            zamowienie = get_or_create(session=db.session, model=Zamowienie, uzytkownik_id=uzytkownik.id, ukonczone=False)
            obiektZamowienia = get_or_create(session=db.session, model=ObiektZamowienia, zamowienie_id=zamowienie.id, produkt_id=produkt_id)
            produkt = get_or_create(session=db.session, model=Produkt, id=produkt_id)
            if not obiektZamowienia.ilosc:
                obiektZamowienia.ilosc = 0
            if produkt.ilosc != 0:
                obiektZamowienia.ilosc = obiektZamowienia.ilosc + 1
                produkt.ilosc = produkt.ilosc - 1
                db.session.commit()
                flash(f'Kosz został zwiekszony', 'success')
            else:
                flash(f'Kosz nie został zwiekszony - brak w magazynie', 'danger')
        else:
            flash(f'Kosz nie został zwiekszony - problem z kontem użytkownika', 'danger')
    else:
        print('Kosz nie został zwiekszony - zaloguj się')
    return redirect(url_for('karta'))


@app.route('/zmniejszKosz/<int:produkt_id>', methods=['GET', 'POST'])
@app.route('/binDecrement/<int:produkt_id>', methods=['GET', 'POST'])
def zmniejszKosz(produkt_id):
    if current_user.is_authenticated:
        uzytkownik = Uzytkownik.query.filter_by(email=current_user.email).first()
        if uzytkownik:
            zamowienie = get_or_create(session=db.session, model=Zamowienie, uzytkownik_id=uzytkownik.id, ukonczone=False)
            obiektZamowienia = get_or_create(session=db.session, model=ObiektZamowienia, zamowienie_id=zamowienie.id, produkt_id=produkt_id)
            produkt = get_or_create(session=db.session, model=Produkt, id=produkt_id)
            if not obiektZamowienia.ilosc:
                obiektZamowienia.ilosc = 0
            if obiektZamowienia.ilosc != 0:
                obiektZamowienia.ilosc = obiektZamowienia.ilosc - 1
                produkt.ilosc = produkt.ilosc + 1
                db.session.commit()
                flash(f'Kosz został zmniejszony', 'success')
            else:
                flash(f'Kosz nie został zmniejszony - brak w koszu', 'danger')
            if obiektZamowienia.ilosc == 0:
                db.session.delete(obiektZamowienia)
                db.session.commit()
        else:
            flash(f'Kosz nie został zmniejszony - problem z kontem użytkownika', 'danger')
    else:
        print('Kosz nie został zmniejszony - zaloguj się')
    return redirect(url_for('karta'))


@app.route('/karta')
@app.route('/card')
def karta():
    zamowienie = {'iloscProduktow': 0, 'lacznaCena': 0, 'obiektZamowienia': []}
    #obsluga zalogowanego uzytkownika
    if current_user.is_authenticated:
        uzytkownik = Uzytkownik.query.filter_by(email=current_user.email).first()
        if uzytkownik:
            zamowienie = get_or_create(session=db.session, model=Zamowienie, uzytkownik_id=uzytkownik.id, ukonczone=False)
            return render_template('karta.html', zamowienie=zamowienie)
    #obsluga niezalogowanego uzytkownika za pomoca ciasteczek
    else:
        zamowienie = przetworzCiasteczkaZamowienia(request)
    return render_template('karta.html', zamowienie=zamowienie)


@app.route('/zamowienie', methods=['GET', 'POST'])
@app.route('/order', methods=['GET', 'POST'])
def zamowienie():
    zamowienie = {'iloscProduktow': 0, 'lacznaCena': 0, 'obiektZamowienia': []}
    formularz = FormularzPotwierdzeniaZamowienia()
    #obsluga zalogowanego uzytkownika
    if current_user.is_authenticated:
        uzytkownik = Uzytkownik.query.filter_by(email=current_user.email).first()
        if uzytkownik:
            zamowienie = get_or_create(session=db.session, model=Zamowienie, uzytkownik_id=uzytkownik.id, ukonczone=False)
            adresDostawy = get_or_create(session=db.session, model=AdresDostawy, uzytkownik_id=uzytkownik.id, zamowienie_id=zamowienie.id)
            if request.method == 'POST':
                if zamowienie.tylkoCyfrowe:
                    formularz.numer.data = formularz.adres.data = formularz.kod.data = formularz.miasto.data = 'cyfrowe'
                if formularz.validate_on_submit() and zamowienie.lacznaCena:
                    adresDostawy.miasto = formularz.miasto.data
                    adresDostawy.kod = formularz.kod.data
                    adresDostawy.adres = formularz.adres.data
                    adresDostawy.numer = formularz.numer.data
                    if formularz.uwagi.data:
                        zamowienie.uwagi = formularz.uwagi.data
                    zamowienie.platnosc = formularz.platnosc.data
                    zamowienie.ukonczone = True
                    emailZamowienia(uzytkownik.email, zamowienie)
                    db.session.commit()
                    flash(f'Zamówienie zostało złożone', 'success')
                    return redirect(url_for('sklep'))
                else:
                    flash(f'Zamówienie nie zostało złożone - wypełnij brakujące dane', 'danger')
                    return redirect(url_for('zamowienie'))
            elif request.method == 'GET':
                formularz.miasto.data = adresDostawy.miasto
                formularz.kod.data = adresDostawy.kod
                formularz.adres.data = adresDostawy.adres
                formularz.numer.data = adresDostawy.numer
            return render_template('zamowienie.html', zamowienie=zamowienie, form=formularz)
    #obsluga niezalogowanego uzytkownika za pomoca ciasteczek
    else:
        zamowienie = przetworzCiasteczkaZamowienia(request)
    return render_template('zamowienie.html', zamowienie=zamowienie, form=formularz)


@app.route('/procesujZamowienie/<int:order_id>', methods=['POST'])
@app.route('/processOrder/<int:order_id>', methods=['POST'])
def procesujZamowienie(order_id):
    #obsluga zalogowanego uzytkownika
    zamowienie = None
    adresDostawy = None
    brakWBazie = False
    if current_user.is_authenticated:
        uzytkownik = Uzytkownik.query.filter_by(email=current_user.email).first()
        if uzytkownik:
            zamowienie = Zamowienie.query.get_or_404(order_id)
            adresDostawy = get_or_create(session=db.session, model=AdresDostawy, uzytkownik_id=uzytkownik.id, zamowienie_id=zamowienie.id)
    #obsluga niezalogowanego uzytkownika za pomoca ciasteczek
    else:
        zamowienieCiasteczka = przetworzCiasteczkaZamowienia(request)
        print('CIASTECZKA:', zamowienieCiasteczka)
        #utworz sztucznego niezalogowanego uzytkownika
        uzytkownik = get_or_create(session=db.session, model=Uzytkownik, email= 'cookiesUser' + ''.join(random.choice(string.ascii_letters) for i in range(10)),
        haslo=''.join(random.choice(string.ascii_letters) for i in range(10)))
        zamowienie = get_or_create(session=db.session, model=Zamowienie, uzytkownik_id=uzytkownik.id, ukonczone=False)
        adresDostawy = get_or_create(session=db.session, model=AdresDostawy, uzytkownik_id=uzytkownik.id, zamowienie_id=zamowienie.id)
        for obiektZamowieniaCiasteczka in zamowienieCiasteczka['obiektZamowienia']:
            produkt = Produkt.query.get_or_404(obiektZamowieniaCiasteczka['produkt'].id)
            if produkt and produkt.ilosc > obiektZamowieniaCiasteczka['ilosc']:
                obiektZamowienia = get_or_create(session=db.session, model=ObiektZamowienia, zamowienie_id=zamowienie.id,
                ilosc=obiektZamowieniaCiasteczka['ilosc'], produkt_id=obiektZamowieniaCiasteczka['produkt'].id)
                produkt.ilosc = produkt.ilosc - obiektZamowieniaCiasteczka['ilosc']
                db.session.commit()
            else:
                brakWBazie = True
    #czesc wspolna obslugi zalogowanego i niezalogowanego uzytkownika
    if zamowienie and zamowienie.tylkoCyfrowe and current_user.is_authenticated:
        adresDostawy.numer = adresDostawy.adres = adresDostawy.kod = adresDostawy.miasto = 'cyfrowe'
    if not brakWBazie and zamowienie and zamowienie.lacznaCena:
        if 'form_data' in request.json:
            dane_zamowienia = request.json['form_data']
            if 'platnosc' in dane_zamowienia and dane_zamowienia['platnosc']:
                zamowienie.platnosc = dane_zamowienia['platnosc']
            if 'adres' in dane_zamowienia and dane_zamowienia['adres']:
                adresDostawy.adres = dane_zamowienia['adres']
            if 'miasto' in dane_zamowienia and dane_zamowienia['miasto']:
                adresDostawy.miasto = dane_zamowienia['miasto']
            if 'kod' in dane_zamowienia and dane_zamowienia['kod']:
                adresDostawy.kod = dane_zamowienia['kod']
            if 'numer' in dane_zamowienia and dane_zamowienia['numer']:
                adresDostawy.numer = dane_zamowienia['numer']
            if 'uwagi' in dane_zamowienia and dane_zamowienia['uwagi']:
                zamowienie.uwagi = dane_zamowienia['uwagi']
        if zamowienie.platnosc and adresDostawy.adres and adresDostawy.miasto and adresDostawy.kod and adresDostawy.numer:
            zamowienie.ukonczone = True
            emailZamowienia(uzytkownik.email, zamowienie)
            db.session.commit()
            flash(f'Zamówienie zostało złożone', 'success');
            print('Zamówienie zostało złożone')
            return redirect(url_for('sklep'))
        else:
            #jesli zamowienie nie zostalo ukonczone dla goscia to posporzataj
            if not current_user.is_authenticated:
                usunDaneZamowienia(zamowienie)
    flash(f'Zamówienie nie zostało złożone - wypełnij brakujące dane', 'danger')
    print('Zamówienie nie zostało złożone - wypełnij brakujące dane')
    return redirect(url_for('zamowienie'))


@app.route('/nowyProdukt', methods=['GET', 'POST'])
@app.route('/newProduct', methods=['GET', 'POST'])
@login_required
def dodanieProduktu():
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    formularz = FormularzNowegoProduktu()
    if formularz.validate_on_submit():
        plik_zdjecia = None
        if formularz.zdjecie.data:
            plik_zdjecia = zachowajZdjecie(formularz.zdjecie.data, sciezka=Konfiguracja.PATH_SHOP)
        produkt = Produkt(tytul=formularz.nazwa.data, tresc=formularz.tresc.data, zdjecie=plik_zdjecia, ilosc=formularz.ilosc.data,
                          cena=formularz.cena.data, cyfrowy=formularz.cyfrowy.data)
        db.session.add(produkt)
        db.session.commit()
        flash(f'Produkt został dodany', 'success')
        return redirect(url_for('sklep'))
    return render_template('nowyProdukt.html', title='Nowy produkt', form=formularz)


@app.route('/usunProdukt/<int:produkt_id>', methods=['GET','POST'])
@app.route('/deleteProduct/<int:produkt_id>', methods=['GET', 'POST'])
@login_required
def usunProdukt(produkt_id):
    produkt = Produkt.query.get_or_404(produkt_id)
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    db.session.delete(produkt)
    db.session.commit()
    flash(f'Produkt został usunięty', 'success')
    return redirect(url_for('sklep'))


@app.route('/aktualizujProdukt/<int:produkt_id>', methods=['GET', 'POST'])
@app.route('/updateProduct/<int:produkt_id>', methods=['GET', 'POST'])
@login_required
def aktualizujProdukt(produkt_id):
    produkt = Produkt.query.get_or_404(produkt_id)
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    formularz = FormularzAktualizacjiProduktu()
    if formularz.validate_on_submit():
        produkt.tytul = formularz.nazwa.data
        produkt.tresc = formularz.tresc.data
        produkt.ilosc = formularz.ilosc.data
        produkt.cena = formularz.cena.data
        produkt.cyfrowy = formularz.cyfrowy.data
        if formularz.zdjecie.data:
            produkt.zdjecie = zachowajZdjecie(formularz.zdjecie.data, sciezka=Konfiguracja.PATH_SHOP)
        db.session.commit()
        flash(f'Produkt został zaktualizowany', 'success')
        return redirect(url_for('sklep'))
    elif request.method == 'GET':
        formularz.nazwa.data = produkt.tytul
        formularz.tresc.data = produkt.tresc
        formularz.zdjecie.data = produkt.zdjecie
        formularz.ilosc.data = produkt.ilosc
        formularz.cena.data = produkt.cena
        formularz.cyfrowy.data = produkt.cyfrowy
    return render_template('nowyProdukt.html', title='Aktualizuj', form=formularz)


@app.route('/historiaZamowien')
@app.route('/ordersHistory')
@login_required
def historiaZamowien():
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    strona = request.args.get('page', 1, type=int)
    zamowienia = Zamowienie.query.order_by(Zamowienie.data.desc()).paginate(page=strona, per_page=20)
    return render_template('historiaZamowien.html', zamowienia=zamowienia, admin=Konfiguracja.MAIL_USERNAME)


@app.route('/historiaZamowienia/<int:zamowienie_id>')
@app.route('/orderHistory/<int:zamowienie_id>')
def historiaZamowienia(zamowienie_id):
    zamowienie = Zamowienie.query.get_or_404(zamowienie_id)
    return render_template('historiaZamowienia.html', zamowienie=zamowienie, admin=Konfiguracja.MAIL_USERNAME)


#Sprzata dane zamowienia takie jak powiazane
#produkty i adresy oraz przywraca na stan sklepu
#produkty dla nieukonczonego zamowienia
def usunDaneZamowienia(zamowienie):
    for obiekt in zamowienie.obiektZamowienia:
        #jesli kasowane nieukonczone zamowienie to jego produkty
        #wracaja na stan sklepu
        if not zamowienie.ukonczone:
            produkt = Produkt.query.get_or_404(obiekt.produkt_id)
            produkt.ilosc += obiekt.ilosc
        db.session.delete(obiekt)
    for adres in zamowienie.adresDostawy:
        db.session.delete(adres)
    db.session.delete(zamowienie)
    db.session.commit()


@app.route('/usunZamowienie/<int:zamowienie_id>', methods=['GET','POST'])
@app.route('/deleteOrder/<int:zamowienie_id>', methods=['GET', 'POST'])
@login_required
def usunZamowienie(zamowienie_id):
    zamowienie = Zamowienie.query.get_or_404(zamowienie_id)
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    usunDaneZamowienia(zamowienie)
    flash(f'Zamowienie zostało usunięte', 'success')
    return redirect(url_for('historiaZamowien'))


@app.route('/aktualizujZamowienie/<int:zamowienie_id>', methods=['GET', 'POST'])
@app.route('/updateOrder/<int:zamowienie_id>', methods=['GET', 'POST'])
@login_required
def aktualizujZamowienie(zamowienie_id):
    zamowienie = Zamowienie.query.get_or_404(zamowienie_id)
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    formularz = FormularzAktualizacjiZamowienia()
    if formularz.validate_on_submit():
        zamowienie.komentarzAdmina = formularz.komentarzAdmina.data
        zamowienie.ukonczone = formularz.ukonczone.data
        db.session.commit()
        flash(f'Zamowienie zostało zaktualizowane', 'success')
        return redirect(url_for('historiaZamowien'))
    elif request.method == 'GET':
        formularz.komentarzAdmina.data = zamowienie.komentarzAdmina
        formularz.ukonczone.data = zamowienie.ukonczone
    return render_template('aktualizujZamowienie.html', title='Aktualizuj', form=formularz)


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


@app.route('/pliki')
@app.route('/files')
def pliki():
    images = []
    try:
        result = cloudinary.Search().expression('folder:twojkomputerowiec AND resource_type:image').with_field('context').execute()
    except:
        result = None
    if result:
        for resource in result['resources']:
            url = resource.get("url")
            id = resource.get("public_id")
            id = id.replace(Konfiguracja.STORAGE_FOLDER + '/', '')
            title = None
            if resource.get("context"):
                title = resource.get("context").get('caption')
            images.append({'url': url, 'title': title, 'id': id})
    videos = []
    try:
        result = cloudinary.Search().expression('folder:twojkomputerowiec AND resource_type:video').with_field('context').execute()
    except:
        result = None
    if result:
        for resource in result['resources']:
            url = resource.get("url")
            id = resource.get("public_id")
            id = id.replace(Konfiguracja.STORAGE_FOLDER + '/', '')
            title = None
            if resource.get("context"):
                title = resource.get("context").get('caption')
            videos.append({'url': url, 'title': title, 'id': id})
    files = []
    try:
        result = cloudinary.Search().expression('folder:twojkomputerowiec AND resource_type:raw').with_field('context').execute()
    except:
        result = None
    if result:
        for resource in result['resources']:
            url = resource.get("url")
            id = resource.get("public_id")
            id = id.replace(Konfiguracja.STORAGE_FOLDER + '/', '')
            title = None
            if resource.get("context"):
                title = resource.get("context").get('caption')
            files.append({'url': url, 'title': title, 'id': id})
    return render_template('pliki.html', images=images, videos=videos, files=files, admin=Konfiguracja.MAIL_USERNAME)


@app.route('/usunPlik/<string:plik_id>/<string:type>')
@app.route('/deleteFile/<string:plik_id>/<string:type>')
def usunPlik(plik_id, type):
    niepowodzenie = False
    try:
        plik_id = Konfiguracja.STORAGE_FOLDER + '/' + plik_id
        cloudinary.api.delete_resources([plik_id], resource_type=type)
    except:
        niepowodzenie = "serwer rzucił wyjątek"
    if not niepowodzenie:
        flash(f'plik został usunięty', 'success')
    else:
        flash(f'plik nie został usunięty: ' + niepowodzenie, 'danger')
    return redirect(url_for('pliki'))


@app.route('/nowyPlik', methods=['GET', 'POST'])
@app.route('/addFile', methods=['GET', 'POST'])
@login_required
def dodaniePliku():
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    formularz = FormularzNowegoPliku()
    if formularz.validate_on_submit():
        niepowodzenie = False
        if formularz.plik.data:
            try:
                cloudinary.uploader.upload(formularz.plik.data, folder=Konfiguracja.STORAGE_FOLDER, resource_type=formularz.rodzaj.data,
                                            context="alt=" + formularz.opis.data + "|caption=" + formularz.tytul.data)
            except:
                niepowodzenie = "serwer rzucił wyjątek"
        else:
            niepowodzenie = "niekompletny formularz"
        if not niepowodzenie:
            flash(f'plik został dodany', 'success')
        else:
            flash(f'plik nie został dodany: ' + niepowodzenie, 'danger')
        return redirect(url_for('pliki'))
    return render_template('nowyPlik.html', title='Nowy plik', form=formularz)


@app.route('/pliki2')
@app.route('/files2')
def pliki2():
    images = []
    try:
        results = imagekit.list_files({
            "path": "/" + Konfiguracja.STORAGE2_FOLDER + "/",
            "skip": 0,
            "limit": 10,
            "fileType": "image"
        })
    except:
        results = None
    if results:
        if not results['error']:
            for result in results['response']:
                url = result.get('url')
                tags = result.get('tags')
                id = result.get('fileId')
                if tags and len(tags) > 1:
                    title = tags[-1]
                else:
                    title = None
                images.append({'url': url, 'title': title, 'id': id})
    videos = []
    try:
        results = imagekit.list_files({
            "path": "/" + Konfiguracja.STORAGE2_FOLDER + "/",
            "skip": 0,
            "limit": 10,
            "fileType": "non-image",
            "tags": "video",
        })
    except:
        results = None
    if results:
        if not results['error']:
            for result in results['response']:
                url = result.get('url')
                tags = result.get('tags')
                id = result.get('fileId')
                if tags and len(tags) > 1:
                    title = tags[-1]
                else:
                    title = None
                videos.append({'url': url, 'title': title, 'id': id})
    files = []
    try:
        results = imagekit.list_files({
            "path": "/" + Konfiguracja.STORAGE2_FOLDER + "/",
            "skip": 0,
            "limit": 10,
            "fileType": "non-image",
            "tags": "raw",
        })
    except:
        results = None
    if results:
        if not results['error']:
            for result in results['response']:
                url = result.get('url')
                tags = result.get('tags')
                id = result.get('fileId')
                if tags and len(tags) > 1:
                    title = tags[-1]
                else:
                    title = None
                files.append({'url': url, 'title': title, 'id': id})
    return render_template('pliki.html', images=images, videos=videos, files=files, admin=Konfiguracja.MAIL_USERNAME)


@app.route('/usunPlik2/<string:plik_id>')
@app.route('/deleteFile2/<string:plik_id>')
def usunPlik2(plik_id):
    niepowodzenie = False
    try:
        imagekit.delete_file(plik_id)
    except:
        niepowodzenie = "serwer rzucił wyjątek"
    if not niepowodzenie:
        flash(f'plik został usunięty', 'success')
    else:
        flash(f'plik nie został usunięty: ' + niepowodzenie, 'danger')
    return redirect(url_for('pliki2'))


@app.route('/nowyPlik2', methods=['GET', 'POST'])
@app.route('/addFile2', methods=['GET', 'POST'])
@login_required
def dodaniePliku2():
    if Konfiguracja.MAIL_USERNAME != current_user.email:
        abort(403)
    formularz = FormularzNowegoPliku()
    if formularz.validate_on_submit():
        niepowodzenie = False
        if formularz.plik.data:
            try:
                imagekit.upload_file(
                    file=formularz.plik.data,
                    file_name=formularz.plik.data.filename,
                    options={
                        "folder": Konfiguracja.STORAGE2_FOLDER,
                        "tags": [formularz.rodzaj.data, formularz.tytul.data],
                        "is_private_file": False,
                        "use_unique_file_name": True,
                        "response_fields": ["tags"],
                    }
                )
            except:
                niepowodzenie = "serwer rzucił wyjątek"
        else:
            niepowodzenie = "niekompletny formularz"
        if not niepowodzenie:
            flash(f'plik został dodany', 'success')
        else:
            flash(f'plik nie został dodany: ' + niepowodzenie, 'danger')
        return redirect(url_for('pliki2'))
    return render_template('nowyPlik.html', title='Nowy plik', form=formularz)


@app.route('/aspice')
def aspice():
    return render_template('aspice.html')


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