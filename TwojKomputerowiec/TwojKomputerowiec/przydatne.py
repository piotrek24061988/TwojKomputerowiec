import os
import secrets
import json
from PIL import Image
from flask import url_for, render_template
from flask_mail import Message
from TwojKomputerowiec import mail, app, db, Konfiguracja
from TwojKomputerowiec.modele import *


def zachowajZdjecie(zdjecie, resize=False, sciezka='static/media/losowe'):
    """
    Funkcja przyjmuje plik załadowany z formularza jako nowe zdjecie profilowe.
    Zapisuje go w katalogu ze zdjęciami profilowymi pod zmienioną nazwą i zwraca tą nazwę.

    :param zdjecie: plik, ktory zostal zaladowany przez formularz jako nowe zdjecie profilowe
    :return: nazwa zdjecia ktora zostaje zaladowana do folderu ze zdjeciami profilowymi
    """
    losowyHex = secrets.token_hex(8)
    _, rozszerzenie = os.path.splitext(zdjecie.filename)
    zdjecieNazwa = losowyHex + rozszerzenie
    sciezkaZdjecia = os.path.join(app.root_path, sciezka, zdjecieNazwa)

    if resize:
        rozmiar = (125, 125)
        zdjecieDoZapisu = Image.open(zdjecie)
        zdjecieDoZapisu.thumbnail(rozmiar)

        zdjecieDoZapisu.save(sciezkaZdjecia)
    else:
        zdjecie.save(sciezkaZdjecia)
    return zdjecieNazwa


def przetworzCiasteczkaZamowienia(request):
    """
    Funkcja przetwarza ciasteczka przeglądarki internetowej w poszukiwaniu danych
    zamówienia niezalogowanego klienta. Funkcja stara się sparsować ciasteczka i
    na ich podstawie utworzyć oiekt zamówienia.
    :param request: Request http przetrzymujący ciasteczka przeglądarki
    :return: obiekt zamowienia niezalogowanego klineta.
    """
    zamowienie = {'iloscProduktow': 0, 'lacznaCena': 0, 'obiektZamowienia': []}
    try:
        karta = json.loads(request.cookies.get('cart'))
        for produkt in karta:
            produktWBazie = get_or_create(session=db.session, model=Produkt, id=produkt)
            if produktWBazie.ilosc > 0:
                zamowienie['iloscProduktow'] += karta[produkt]['quantity']
                zamowienie['lacznaCena'] += karta[produkt]['quantity'] * produktWBazie.cena
            obiekt = {
                'produkt': produktWBazie,
                'ilosc': karta[produkt]['quantity'],
                'calkowitaCena': karta[produkt]['quantity'] * produktWBazie.cena,
            }
            zamowienie['obiektZamowienia'].append(obiekt)
    except:
        zamowienie = {'iloscProduktow': 0, 'lacznaCena': 0, 'obiektZamowienia': []}
    return zamowienie


def emailResetuHasla(uzytkownik):
    """
    Wyślij email do zarejestrowanego użytkownika, który zapomniał swoje hasło.
    Użytkownik otrzyma na maila link do strony, gdzie będzie mógł utworzyć nowe hasło.
    :param uzytkownik: który jest zarejestrowany i zapomniał swoje hasło.
    """
    token = uzytkownik.utworz_Token()
    msg = Message('Wniosek Resetu Hasła', sender='noreplay@demo.com', recipients=[uzytkownik.email])
    msg.body = f""" Żeby zresetować hasło odwiedź poniższy link:
    {url_for('noweHaslo', token=token, _external=True)}

    Regards https://piotrek24061988.pythonanywhere.com
    """
    mail.send(msg)


def emailKontaktowy(kontakt, temat, tresc):
    """
    Wyślij email kontaktowy do administratora strony.
    :param kontakt, temat, tresc - maila
    """
    msg = Message("Twój komputerowiec: " + temat, sender='noreplay@demo.com', recipients=[Konfiguracja.MAIL_USERNAME])
    msg.body = "Twój komputerowiec:\n\n" + tresc + "\n\n" + "kontakt: " + kontakt
    mail.send(msg)


def emailZamowienia(emailZamawiajacego, zamowienie):
    """
    Wyślij email kontaktowy do administratora strony.
    :param kontakt, temat, tresc - maila
    """
    msg = Message("Twój komputerowiec: ZAMÓWIENIE", sender='emailZamawiajacego', recipients=[Konfiguracja.MAIL_USERNAME, emailZamawiajacego])
    msg.body = "ZAMÓWIENIE NR: " + str(zamowienie.id)
    msg.html = render_template('mailZamowienia.html', zamowienie=zamowienie, admin=Konfiguracja.MAIL_USERNAME)
    mail.send(msg)
