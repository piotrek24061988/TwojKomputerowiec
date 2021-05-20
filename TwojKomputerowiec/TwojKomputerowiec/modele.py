from datetime import datetime
from TwojKomputerowiec import db, loginManager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@loginManager.user_loader
def zaladujUzytkownika(userId):
    return Uzytkownik.query.get(int(userId))


class Uzytkownik(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    zdjecie = db.Column(db.String(20), nullable=False, default='account.png')
    haslo = db.Column(db.String(60), nullable=False)
    posty = db.relationship('Post', backref='autor', lazy=True)
    zamowienia = db.relationship('Zamowienie', backref='autor', lazy=True)
    adres = db.relationship('AdresDostawy', backref='autor', lazy=True)

    def __repr__(self):
        return f"Uzytkownik('{self.email}','{self.zdjecie}')"

    def utworz_Token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def weryfikuj_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            uzytkownik_id = s.loads(token)['user_id']
        except:
            return None
        return Uzytkownik.query.get(uzytkownik_id)


class Wpis:
    id = db.Column(db.Integer, primary_key=True)
    tytul = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Wpis('{self.tytul}')"


class Post(db.Model, Wpis):
    tresc = db.Column(db.Text, nullable=False)
    uzytkownik_id = db.Column(db.Integer, db.ForeignKey('uzytkownik.id'), nullable=False)


class Aktualnosc(db.Model, Wpis):
    tresc = db.Column(db.Text, nullable=False)
    zdjecie = db.Column(db.String(20), nullable=True)
    videoUrl = db.Column(db.String(200), nullable=True)


class Galeria(db.Model, Wpis):
    zdjecie = db.Column(db.String(20), nullable=False, default='Bydgoszcz.jpg')


class Produkt(db.Model, Wpis):
    tresc = db.Column(db.Text, nullable=False)
    zdjecie = db.Column(db.String(20), nullable=True)
    ilosc = db.Column(db.Integer, nullable=True)
    cena = db.Column(db.Float, nullable=True)
    cyfrowy = db.Column(db.Boolean, default=False)
    obiektZamowienia = db.relationship('ObiektZamowienia', backref='produkt', lazy=True)


class Zamowienie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uzytkownik_id = db.Column(db.Integer, db.ForeignKey('uzytkownik.id'), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ukonczone = db.Column(db.Boolean, default=False)
    platnosc = db.Column(db.String(200), nullable=True)
    uwagi = db.Column(db.Text, nullable=False, default="Systemowy brak uwag")
    komentarzAdmina = db.Column(db.Text, nullable=False, default="Systemowy brak komentarza")
    obiektZamowienia = db.relationship('ObiektZamowienia', backref='zamowienie', lazy=True)
    adresDostawy = db.relationship('AdresDostawy', backref='zamowienie', lazy=True)


class ObiektZamowienia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produkt_id = db.Column(db.Integer, db.ForeignKey('produkt.id'), nullable=False)
    zamowienie_id = db.Column(db.Integer, db.ForeignKey('zamowienie.id'), nullable=False)
    ilosc = db.Column(db.Integer, nullable=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class AdresDostawy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uzytkownik_id = db.Column(db.Integer, db.ForeignKey('uzytkownik.id'), nullable=False)
    zamowienie_id = db.Column(db.Integer, db.ForeignKey('zamowienie.id'), nullable=False)
    adres = db.Column(db.String(200), nullable=True)
    miasto = db.Column(db.String(100), nullable=True)
    kod = db.Column(db.String(50), nullable=True)
    numer = db.Column(db.String(100), nullable=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __str__(self):
        print(adres)


