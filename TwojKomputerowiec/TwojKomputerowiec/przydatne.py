import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from TwojKomputerowiec import mail, app


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


def zachowajZdjecieAktualnosci(zdjecie):
    """
    Funkcja przyjmuje plik załadowany z formularza jako zdjecie aktualnosci.
    Zapisuje go w katalogu ze zdjęciami aktualnosci pod zmienioną nazwą i zwraca tą nazwę.

    :param zdjecie: plik, ktory zostal zaladowany przez formularz jako zdjecie aktualnosci
    :return: nazwa zdjecia ktora zostaje zaladowana do folderu ze zdjeciami aktualnosci
    """
    losowyHex = secrets.token_hex(8)
    _, rozszerzenie = os.path.splitext(zdjecie.filename)
    zdjecieNazwa = losowyHex + rozszerzenie
    sciezkaZdjecia = os.path.join(app.root_path, 'static/media/aktualnosci', zdjecieNazwa)
    zdjecie.save(sciezkaZdjecia)

    return zdjecieNazwa


def zachowajZdjecieGalerii(zdjecie):
    """
    Funkcja przyjmuje plik załadowany z formularza jako zdjecie galerii.
    Zapisuje go w katalogu ze zdjęciami galerii pod zmienioną nazwą i zwraca tą nazwę.

    :param zdjecie: plik, ktory zostal zaladowany przez formularz jako zdjecie galerii
    :return: nazwa zdjecia ktora zostaje zaladowana do folderu ze zdjeciami galerii
    """
    losowyHex = secrets.token_hex(8)
    _, rozszerzenie = os.path.splitext(zdjecie.filename)
    zdjecieNazwa = losowyHex + rozszerzenie
    sciezkaZdjecia = os.path.join(app.root_path, 'static/media/galeria', zdjecieNazwa)
    zdjecie.save(sciezkaZdjecia)

    return zdjecieNazwa


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
    msg = Message("Twój komputerowiec: " + temat, sender='noreplay@demo.com', recipients=['piotrek24061988@gmail.com'])
    msg.body = "Twój komputerowiec:\n\n" + tresc + "\n\n" + "kontakt: " + kontakt
    mail.send(msg)
