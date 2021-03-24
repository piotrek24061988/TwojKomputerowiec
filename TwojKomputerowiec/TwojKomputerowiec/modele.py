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


class Wpis():
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


class Zdjecie(db.Model, Wpis):
    zdjecie = db.Column(db.String(20), nullable=True)