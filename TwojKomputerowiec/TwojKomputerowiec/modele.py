from datetime import datetime
from TwojKomputerowiec import db


class Uzytkownik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    zdjecie = db.Column(db.String(20), nullable=False, default='account.png')
    haslo = db.Column(db.String(60), nullable=False)
    posty = db.relationship('Post', backref='autor', lazy=True)

    def __repr__(self):
        return f"Uzytkownik('{self.email}','{self.zdjecie}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tytul = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tresc = db.Column(db.Text, nullable=False)
    uzytkownik_id = db.Column(db.Integer, db.ForeignKey('uzytkownik.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.tytul}','{self.data}')"